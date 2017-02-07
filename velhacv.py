import numpy as np
import cv2
import tictactoe as tic
import time

CARD_COLOR_UP = np.array([255,255,255],dtype="uint8")
CARD_COLOR_LOW = np.array([150,150,150],dtype="uint8")
FONTE = cv2.FONT_HERSHEY_SIMPLEX
global choose_user, player, computer
KERNEL = np.ones((3,3),np.uint8)
choose_user = True
game = True
init = False
last_time = 0

def findBiggestContour(mask):
    temp_bigger = []
    img1, cont, hier = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(cont) == 0:
        return False
    for cnt in cont:
        temp_bigger.append(cv2.contourArea(cnt))
    greatest = max(temp_bigger)
    index_big = temp_bigger.index(greatest)
    key = 0
    for cnt in cont:
        if key == index_big:
            return cnt
            break
        key += 1

def getField(coord, frame):
    crop_img = frame[coord[0]:coord[1], coord[2]:coord[3]]
    return crop_img


def getContoursHSV(img):
    mask = cv2.inRange(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), CARD_COLOR_LOW, CARD_COLOR_UP)
    if len(mask) > 0:
        dilation = cv2.dilate(mask,KERNEL,iterations = 2)
        cnt = findBiggestContour(dilation)
        return cnt
    else:
        return False

def compareContourHSV(cnt):
    global player, computer
    if cnt is False:
        return False
    patternX = cv2.cvtColor(cv2.imread('X.png'), cv2.COLOR_BGR2GRAY)
    patternX = findBiggestContour(patternX)
    resX = cv2.matchShapes(patternX, cnt, 1, 0.0)
    patternO = cv2.cvtColor(cv2.imread('O.png'), cv2.COLOR_BGR2GRAY)
    patternO = findBiggestContour(patternO)
    resO = cv2.matchShapes(patternO, cnt, 1, 0.0)
    if resX < 0.9 or resO < 0.9:
        if resX < resO:
            player = 1
            computer = 2
            return player
        elif resX != 0 and resO != 0:
            player = 2
            computer = 1
            return player
    else:
        return False

def getPlayer(points, frame):
    global choose_user, init, last_time, player
    hW,wW = frame.shape[0:2]
    cv2.line(frame,(0,hW-25),(wW,hW-25),(35,35,155),25)
    cv2.putText(frame, "Jogador, escolha uma jogada.",(150, hW-20), FONTE, 0.7,(0,255,0),2,cv2.LINE_AA)
    field_key = 0
    gameboard = np.array(tic.game[0]+tic.game[1]+tic.game[2])
    indexs = np.where(gameboard == 0)[0]
    for field in points:
        cropped = getField(field, frame)
        cnt = getContoursHSV(cropped)
        value = compareContourHSV(cnt)
        old_played = np.where(indexs== field_key)[0]
        if value != False and init == False and len(old_played) == 1:
            print "Achou nova jogada! Aguarde 3 segundos."
            last_time = int(time.time())
            init = True
        if value != False and int(time.time()) - last_time > 3 and init == True and len(old_played) == 1:
            print "Jogada player:", field_key
            tic.writePosition(field_key, value)
            init = False
            choose_user = False
            return tic.verifyWinner(value)
        field_key += 1
    return False

write_comp = False
cap = cv2.VideoCapture(1)
while(game):
    fields = []
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    frame = cv2.flip(frame,0)
    hW,wW = frame.shape[0:2]
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cnt = findBiggestContour(cv2.Canny(frame_gray, 100,200))
    x,y,h,w = cv2.boundingRect(cnt)
    #cv2.rectangle(frame,(x,y),(x+h,y+w),(0,255,0),2)
    column = w/3
    line = h/3
    points = []
    key = 0


    for num_column in range(0,4):
        for num_line in range(0,4):
            points.append(((num_line*line)+x,(num_column*column)+y))


    for number in range(0, 11):
        if number != 3 and number != 7:
            field = [points[number][1], points[number+5][1], points[number][0],points[number+5][0]]
            fields.append(field)


    for field in fields:
        cv2.circle(frame, (field[2], field[0]), 3, (0,0,255), -1)


    if choose_user == True:
        result = getPlayer(fields, frame)
        if  result == True:
            print "O jogador venceu!"
            break
        elif result == "EMPATE":
            print "Houve empate!"
            break


    elif choose_user == False:
        tic.inteligence(computer)
        result = tic.verifyWinner(computer)
        print tic.game[0]
        print tic.game[1]
        print tic.game[2]
        if  result == True:
            print "O computador venceu!"
            break
        elif result == "EMPATE":
            print "Houve empate!"
            break
        write_comp = True
        choose_user = True

    if write_comp == True:
        if computer == 1:
            text = "X"
        else:
            text = "O"
        gameboard = np.array(tic.game[0]+tic.game[1]+tic.game[2])
        indexs = np.where(gameboard==computer)[0]
        for index in indexs:
            coord = (fields[index][2]+50, fields[index][0]+100)
            cv2.putText(frame, text,coord, FONTE, 3,(50,0,255),2,cv2.LINE_AA)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow('Exemplo',frame)

cap.release()
cv2.destroyAllWindows()

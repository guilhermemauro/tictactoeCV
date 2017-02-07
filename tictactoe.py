import operators as op
import random
from datetime import datetime

#create the game board
game = [[0,0,0],[0,0,0],[0,0,0]]
win = False

#this function writes in board the mark
def writePosition(position, player):
    if position < 3:
        if int(game[0][position]) is 0:
            game[0][position] = player
        else:
            print "Essa casa ja esta preenchida!"
            getPlayerMark(player)
    if position > 2 and position < 6:
        if int(game[1][position - 3]) is 0:
            game[1][position - 3] = player
        else:
            print "Essa casa ja esta preenchida!"
            getPlayerMark(player)
    if position > 5 and position < 9:
        if int(game[2][position - 6]) is 0:
            game[2][position - 6] = player
        else:
            print "Essa casa ja esta preenchida!"
            getPlayerMark(player)

#this function get the position mark of the player
def getPlayerMark(player):
    position = int(raw_input('Qual posicao escolhe? (0-8)'))
    print "Voce escolheu a posicao %d." % position
    writePosition(position, player)
    print game[0]
    print game[1]
    print game[2]

def verifyWinner(player):
    index = 0
    for number in game[0]+game[1]+game[2]:
        if number == 0:
            index += 1
    if index == 0:
        return "EMPATE"
    #check lines
    for line in [0,1,2]:
        points = 0
        for house in game[line]:
            if int(house) == player:
                points += 1
            if points == 3:
                return True
    #check columns
    for column in [0, 1, 2]:
        points = 0
        for line in [0,1,2]:
            if int(game[line][column]) == player:
                points += 1
            if points == 3:
                return True
    #check diagonals
    points = 0
    for line in [0,1,2]:
        if int(game[line][line]) == player:
            points += 1
        if points == 3:
            return True
    points = 0
    for line in [2,1,0]:
        if int(game[line][2-line]) == player:
            points += 1
        if points == 3:
            return True

    return False

def inteligence(player):
    objects = []

    #check lines, make a object for each line
    for line in [0,1,2]:
        blank = 0
        other = 0
        play = 0
        for column in [0,1,2]:
            field = int(game[line][column])
            if field is 0:
                blank += 1
            elif field is player:
                play += 1
            else:
                other += 1
        objects.append(op.elements(other, blank, play))

    #check columns, make a object for each column
    for line in [0,1,2]:
        blank = 0
        other = 0
        play = 0
        for column in [0,1,2]:
            field = int(game[column][line])
            if field is 0:
                blank += 1
            elif field is player:
                play += 1
            else:
                other += 1
        objects.append(op.elements(other, blank, play))

    #check diagonals, make a object for each diagonal
    blank = 0
    other = 0
    play = 0
    for line in [2,1,0]:
        field = game[line][2-line]
        if field is 0:
            blank += 1
        elif field is player:
            play += 1
        else:
            other += 1
    objects.append(op.elements(other, blank, play))

    blank = 0
    other = 0
    play = 0
    for line in [0,1,2]:
        field = game[line][line]
        if field is 0:
            blank += 1
        elif field is player:
            play += 1
        else:
            other += 1
    objects.append(op.elements(other, blank, play))

#check if there is a chance of the computer wins and complete sequence
    for obj in objects:
        if obj.iGoWins() is True:
            position = objects.index(obj)
            #mark lines
            if position <= 2:
                writePosition(game[position].index(0)+(position*3), player)
                return 0
            #mark columns
            elif position > 2 and position < 6:
                column = position - 3
                for line in [0,1,2]:
                    if game[line][column] == 0:
                        writePosition(((line*3)+column), player)
                        return ((line*3)+column)
            #mark diagonals
            elif position > 5:
                if position == 6:
                    for line in [2,1,0]:
                        if game[line][2-line] == 0:
                            writePosition(((line*3)+(2-line)), player)
                            return ((line*3)+(2-line))
                if position == 7:
                    for line in [0,1,2]:
                        if game[line][line] == 0:
                            writePosition(((line*3)+line), player)
                            return ((line*3)+line)
    #check if there is a chance of the Player wins and block it
    for obj in objects:
        if obj.otherGoWins() is True:
            position = objects.index(obj)
            #block lines
            if position <= 2:
                writePosition(game[position].index(0)+(position*3), player)
                return 0
            #block columns
            elif position > 2 and position < 6:
                column = position - 3
                for line in [0,1,2]:
                    if game[line][column] == 0:
                        writePosition(((line*3)+column), player)
                        return ((line*3)+column)
            #block diagonals
            elif position > 5:
                if position == 6:
                    for line in [2,1,0]:
                        if game[line][2-line] == 0:
                            writePosition(((line*3)+(2-line)), player)
                            return ((line*3)+(2-line))
                if position == 7:
                    for line in [0,1,2]:
                        if game[line][line] == 0:
                            writePosition(((line*3)+line), player)
                            return ((line*3)+line)
    #check what houses are blank and choose one randomly, but first, select the middle field if is blank
    possibilities = []
    index = 0
    for number in game[0]+game[1]+game[2]:
        if number == 0:
            if index == 4:
                writePosition(4, player)
                return 4
            possibilities.append(index)
        index += 1
    random.seed(datetime.now())
    position = random.choice(possibilities)
    writePosition(position, player)
    return position

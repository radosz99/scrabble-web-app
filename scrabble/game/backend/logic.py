import random

def prepare_board():
    board=[]
    f = open('resources/board.csv', "r")
    bb = [line.strip().lower() for line in f]
    for x in range(len(bb)):
        line = bb[x].split(";")
        upper_line = [y.upper() for y in line]
        board.append(upper_line)
    return board
        
def make_move(move, board):
    letters = move.split(";")
    sum=0
    if(len(letters)==7):
        bonus=50
    else:
        bonus=0
    multiplier=1

    for letter in letters:
        details=letter.split(":")
        char = details[2]
        if(board[int(details[0])][int(details[1])]==''):
            board[int(details[0])][int(details[1])]=char.upper()
            sum_letter,multiplier_word = get_field_value(char,int(details[0]),int(details[1]))
            sum=sum+sum_letter
            multiplier=int(multiplier*multiplier_word)
    return board,sum*multiplier+bonus

def random_string(letters):
    string=''
    while(len(string)!=7 and len(letters)!=0):
        index=random.randint(0,len(letters)-1)
        char = letters[index]
        string=string+char
        letters.remove(char)
    return string,letters


def get_field_value(char, x,y):
    word_multiplier=1
    letter_multiplier=1
    letter_value = get_char_value(char.lower())
    if(((x==1 or x==13)and (y==1 or y==13)) or ((x==2 or x==12) and (y==2 or y==12)) or ((x==3  or x==11) and (y==3 or y==11)) or ((x==4 or x==10) and (y==4 or y==10))):
        word_multiplier=2
    if(((x==0 or x==14) and (y==0 or y==7 or y==14)) or (x==7 and (y==0 or y==14))):
        word_multiplier=3
    if(((x==5 or x==9) and (y==1 or y==5 or y==9 or y==13)) or ((x==1 or x==13) and (y==5 or y==9))):
        letter_multiplier=3
    if(((x==0 or x==7 or x==14) and (y==3 or y==11)) or ((x==3 or x==11) and (y==0 or y==7 or y==14))
        or((x==2 or x==6 or x==8 or x==12) and (y==6 or y==8)) or((y==2 or y==6 or y==8 or y==12) and (x==6 or x==8))):
        letter_multiplier=2
    if(x==7 and y==7):
        letter_multiplier=1
        word_multiplier=1

    return letter_multiplier*letter_value, word_multiplier

def get_char_value(char):
    if(char=='a' or char=='e' or char=='i' or char=='n' or char=='o' or char=='r' or char=='s' or char=='w' or char=='z'):
        return 1
    if(char=='c' or char=='d' or char=='k' or char=='l' or char=='m' or char=='p' or char=='t' or char=='y'):
        return 2
    if(char=='b' or char=='g' or char=='h' or char=='j' or char=='ł' or char=='u'):
        return 3
    if(char=='ą' or char=='ę' or char=='f' or char=='ó' or char=='ś' or char=='ż'):
        return 5
    if(char=='ć'):
        return 6
    if(char=='ń'):
        return 7
    if(char=='ź'):
        return 9
    return 1
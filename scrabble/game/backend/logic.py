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
        
def make_move(move, board, user_letters):
    letters = move.split(";")
    used_letters=[]
    sum=0
    if(len(letters)==7):
        bonus=50
    else:
        bonus=0
    multiplier=1

    for letter in letters:
        details=letter.split(":")
        char = details[2].upper()
        used_letters.append(char)
        if(board[int(details[0])][int(details[1])]==''):
            board[int(details[0])][int(details[1])]=char.upper()
            sum_letter,multiplier_word = get_field_value(char,int(details[0]),int(details[1]))
            sum=sum+sum_letter
            multiplier=int(multiplier*multiplier_word)

    used_letters_string = ''.join(map(str, used_letters))
    for letter in used_letters:
        position = user_letters.find(letter)
        if(position!=-1):
            help_letters = user_letters[0 : position ] + user_letters[position + 1 : len(user_letters)]
            user_letters = help_letters
        else:
            print("ERROR")
            #obsluga braku posiadania takowych liter przez uczestnika 
    return board,sum*multiplier+bonus, user_letters.lower(),used_letters_string

def random_string(letters, letters_not_used):
    while(len(letters_not_used)!=7 and len(letters)!=0):
        index=random.randint(0,len(letters)-1)
        char = letters[index]
        letters_not_used=letters_not_used+char
        letters.remove(char)
    return letters_not_used,letters


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

def save_game_log_to_file(board,letters,users,turn,moves):
    text_file = open("resources/saved_game_log.txt", "w")
    users_string=''
    move_string=''
    letters_string=''

    for char in letters:
        letters_string=letters_string+char
    text_file.write("%s\n" % letters_string)

    for user in users:
        users_string=users_string+str(user[0])+"," + str(user[1])+"," + str(user[2])+ "," + str(user[3])+ ";"
    text_file.write("%s\n" % users_string[0:len(users_string)-1])

    text_file.write("%s\n" % str(turn))

    for line in board:
        row=''
        for char in line:
            row=row+char+";"
        text_file.write("%s\n" % row[0:len(row)-1])

    for move in moves:
        move_string = move_string+str(move[0])+","+str(move[1])+","+str(move[2])+ ";"
    text_file.write("%s" % move_string[0:len(move_string)-1])
    text_file.close()


def get_game_log_from_file():
    board=[]
    users=[]
    moves=[]
    turn=0
    letters = []

    text_file = open("resources/saved_game_log.txt", "r")
    letters_string = text_file.readline()
    letters= list(letters_string[0:len(letters_string)-1])

    users_string = text_file.readline()
    users_non_converted= users_string[0:len(users_string)-1].split(';')
    for user_non_converted in users_non_converted:
        if(user_non_converted==''):
            break
        users_parts = user_non_converted.split(',')
        if(users_parts[3]=="True"):
            users.append((int(users_parts[0]),int(users_parts[1]),users_parts[2],True))
        else:
            users.append((int(users_parts[0]),int(users_parts[1]),users_parts[2],False))

    turn = int(text_file.readline())

    for i in range(15):
        row_string = text_file.readline()
        row=row_string[0:len(row_string)-1].split(';')
        board.append(row)

    moves_string = text_file.readline()
    moves_non_converted= moves_string.split(';')
    for move_non_converted in moves_non_converted:
        if(move_non_converted==''):
            break
        move_parts = move_non_converted.split(',')
        moves.append((move_parts[0],move_parts[1],move_parts[2]))
    text_file.close()

    return board, users, moves, turn, letters

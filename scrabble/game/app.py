from flask import Flask, jsonify, request, abort, render_template, flash, redirect, url_for
from .backend.trie import make_trie
from .backend.logic import make_move, random_string, prepare_board
from .backend.algorithm import Algorithm

import sys
app = Flask(__name__)

board=[]
users=[]
moves=[]
trie={}
turn=0
letters = []

@app.route('/')
def student():
    prepare_board()
    return render_template('start.html')

@app.route('/game/view',methods=['GET'])
def game_view():
    last_moves=[]
    if(len(moves)>=10):
        last_moves = moves[0:10].copy()
        last_moves.reverse()
    elif(len(moves)==0):
        last_moves = []
    else:
        last_moves = moves.copy()
        last_moves.reverse()
    return render_template("game.html", board = board, users=users, turn=turn, letters_quantity=len(letters), moves=last_moves)    

@app.route('/game/init',methods = ['POST'])
def board_view():
    global letters,users,board,turn,moves
    if request.method == 'POST':
        letters=['a','a','a','a','a','a','a','a','a','e','e','e','e','e','e','e','i','i','i','i','i','i','i','i','n','n','n','n','n','o','o','o','o','o','o',
         'r','r','r','r','s','s','s','s','w','w','w','w','z','z','z','z','z','c','c','c','d','d','d','k','k','k','l','l','l','m','m','m','p','p','p','t','t','t','y','y','y','y',
         'b','b','g','g','h','h','j','j','ł','ł','u','u','ą','ę','f','ó','u','ś','ż','ć','ń','ź']
        users.clear()
        board.clear()
        moves.clear()
        turn=0
        board=prepare_board()
        info = request.form
        quantity=info['Number of players']
        for i in range(int(quantity)):
            user_letters, letters = random_string(letters,'')
            users.append((i,0,user_letters, False))
        return redirect(url_for('game_view'))

@app.route('/game/move',methods = ['POST'])
def move():
    global users,turn,board, letters
    if(users[turn][3]==False):
        info = request.form
        move=info['move']
        board, points, letters_not_used, word = make_move(move=move, board=board, user_letters=users[turn][2].upper())
        moves.append((turn, word, points))
        new_letters, letters = random_string(letters, letters_not_used)
        user = (users[turn][0], users[turn][1]+points, new_letters, users[turn][3])
        users = list(filter(lambda x: x[0] != turn, users))
        users.append(user)
        users.sort(key=lambda tup: tup[0])

        if(turn<len(users)-1):
            turn = turn+1
        else:
            turn=0
    
    while(users[turn][3]==True):
        for user in users:
            print(user)
        if(len(users[turn][2])==0):
            break
        algorithm = Algorithm(users[turn][2],board)
        board, points, letters_not_used, word = algorithm.algorithm_engine(trie)
        moves.append((turn, word, points))
        letters_not_used_string=''.join(map(str, letters_not_used))
        new_letters, letters = random_string(letters,letters_not_used_string)
        user = (users[turn][0], users[turn][1]+points, new_letters, users[turn][3])
        users = list(filter(lambda x: x[0] != turn, users))
        users.append(user)
        users.sort(key=lambda tup: tup[0])
        if(turn<len(users)-1):
            turn = turn+1
        else:
            turn=0
    return redirect(url_for('game_view'))

@app.route('/game/computer', methods = ['POST'])
def add_computer():
    global letters,trie
    if(len(trie)==0):
        trie = make_trie()
    user_letters, letters = random_string(letters,'')
    users.append((len(users),0,user_letters,True))
    return redirect(url_for('game_view'))

@app.route('/game/save', methods = ['POST'])
def save_to_file():
    text_file = open("resources/saved_board.txt", "w")
    users_string=''

    for user in users:
        users_string=users_string+str(user[0])+", " + str(user[1])+", " + str(user[2])+", " + str(user[3]) + "; "
    text_file.write("%s\n" % users_string)
    text_file.write("%s\n" % str(turn))
    for line in board:
        row=''
        for char in line:
            row=row+char+";"
        text_file.write("%s\n" % row[0:len(row)-1])

    return redirect(url_for('game_view'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
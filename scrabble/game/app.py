from flask import Flask, jsonify, request, abort, render_template, flash, redirect, url_for
from .backend.trie import make_trie
from .backend.logic import make_move, random_string, save_game_log_to_file, get_game_log_from_file
from .backend.algorithm import Algorithm

import sys
app = Flask(__name__)

trie={}

@app.route('/')
def student():
    return redirect(url_for('game_view'))

@app.route('/game/view',methods=['GET'])
def game_view():
    board, users, moves, turn, letters = get_game_log_from_file()

    last_moves=[]
    if(len(moves)>=10):
        last_moves = moves[0:10].copy()
    elif(len(moves)==0):
        last_moves = []
    else:
        last_moves = moves.copy()
    return render_template("game.html", board = board, users=users, turn=turn, letters_quantity=len(letters), moves=last_moves)    

@app.route('/game/move',methods = ['POST'])
def move():
    board, users, moves, turn, letters = get_game_log_from_file()
    if(users[turn][3]==False):
        info = request.form
        move=info['move']
        board, points, letters_not_used, word = make_move(move=move, board=board, user_letters=users[turn][2].upper())
        moves.insert(0,(turn, word, points))
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
        if(len(users[turn][2])==0):
            break
        algorithm = Algorithm(users[turn][2],board)
        board, points, letters_not_used, word = algorithm.algorithm_engine(trie)
        moves.insert(0,(turn, word, points))
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

    save_game_log_to_file(board=board, letters=letters, users=users, turn=turn,moves=moves)
    return redirect(url_for('game_view'))

@app.route('/game/computer', methods = ['POST'])
def add_computer():
    global trie
    board, users, moves, turn, letters = get_game_log_from_file()
    if(len(trie)==0):
        trie = make_trie()
    user_letters, letters = random_string(letters,'')
    users.append((len(users),0,user_letters,True))
    save_game_log_to_file(board=board, letters=letters, users=users, turn=turn,moves=moves)
    return redirect(url_for('game_view'))

    
@app.route('/game/user', methods = ['POST'])
def add_user():
    board, users, moves, turn, letters = get_game_log_from_file()
    user_letters, letters = random_string(letters,'')
    users.append((len(users),0,user_letters,False))
    save_game_log_to_file(board=board, letters=letters, users=users, turn=turn,moves=moves)
    return redirect(url_for('game_view'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
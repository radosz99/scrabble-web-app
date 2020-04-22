from flask import Flask, jsonify, request, abort, render_template, flash, redirect, url_for

app = Flask(__name__)
empDB =[
 {
 'id': '101',
 'name':'Saravanan S',
 'title':'Technical Leader'
 },

 {
 'id':'201',
 'name':'Rajkumar P',
 'title':'Sr Software Engineer'
 }]

board=[]
def prepare_board():
    f = open('resources/board.csv', "r")
    bb = [line.strip().lower() for line in f]
    for x in range(len(bb)):
        line = bb[x].split(";")
        upper_line = [y.upper() for y in line]
        board.append(upper_line)

@app.route('/empdb/employee',methods=['GET'])
def getAllEmp():

    return jsonify({'emps': empDB})

@app.route('/empdb/employee/<empId>',methods=['GET'])
def getEmp(empId):
    usr = [ emp for emp in empDB if (emp['id'] == empId) ] 
    return jsonify({'emp':usr})


@app.route('/empdb/employee/<empId>',methods=['PUT'])
def updateEmp(empId): 
    em = [ emp for emp in empDB if (emp['id'] == empId) ] 
    if 'name' in request.json : 
        em[0]['name'] = request.json['name'] 
    if 'title' in request.json:
        em[0]['title'] = request.json['title'] 
    return jsonify({'emp':em[0]})

@app.route('/empdb/employee',methods=['POST'])
def createEmp(): 
    dat = {
    'id':request.json['id'],
    'name':request.json['name'],
    'title':request.json['title']
    }
    empDB.append(dat)
    return jsonify(dat)

@app.route('/empdb/employee/<empId>',methods=['DELETE'])
def deleteEmp(empId): 
    em = [ emp for emp in empDB if (emp['id'] == empId) ] 
    if (len(em) == 0):
        abort(404) 
    empDB.remove(em[0])
    return jsonify({'response':'Success'})

@app.route('/')
def student():
    prepare_board()
    return render_template('start.html')

@app.route('/game',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      #result = request.form
      return render_template("game.html",result = board)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
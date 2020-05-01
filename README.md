**<p align="center"> Good Programming Practices </p>**
_________________________________
**<p align="center"> Wrocaw University of Science and Technology </p>**
**<p align="center"> Computer Science, Faculty of Electronics, 6 semester </p>**
**<p align="center"> Radoslaw Lis </p>**

# Table of Contents
- [General info](#desc)  
- [Run](#run)  
- [Screenshot](#sc)

<a name="desc"></a>
# General info

Multiplayer scrabble game. First clash with the web, don't judge me :(

Words are inserted in the form:
```
(coordinate X of letter1):(coordinate Y of letter1):(letter1);(coordinate X of letter2):(coordinate Y of letter2):(letter2);...
```

For example:
```
5:6:A;5:7:B;5:8:C;5:9:D;5:10:E
```
The correctness of moves has not been implemented yet (but of course the computer does it correctly).

- [x] Playing with a computer
- [x] Move evaluating
- [ ] Verify correctness of moves

<a name="run"></a>
# Run

```
$ git clone https://git.e-science.pl/rlis241385_dpp/rlis_flaskapi.git
$ cd rlis_flaskapi/scrabble
$ docker build -t game .
$ docker run -p 5000:5000 game
```
<a name="sc"></a>
# Screenshot
From the internal battle of computers:  
<p align="center">
<img src="https://github.com/radosz99/scrabble_web_app/blob/master/scrabble/screenshot.png" width=100% />
</p>

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

Multiplayer scrabble game.

On the start page (*/*) select number of players and go to the main view (*/game/view*). 
It is possible to join a computer game based on the algorithm from *lab07* and save the current state to the *.txt* file - the board, users and their points and who has the queue.

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
<p align="center">
  <img src="https://i.imgur.com/9T3o4km.png" width=100% alt="Img"/>
</p>
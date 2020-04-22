**<p align="center"> Good Programming Practices </p>**
_________________________________
**<p align="center"> Wrocaw University of Science and Technology </p>**
**<p align="center"> Computer Science, Faculty of Electronics, 6 semester </p>**
**<p align="center"> Radoslaw Lis </p>**

# Table of Contents
- [General info](#desc)  
- [Run](#run)  


<a name="desc"></a>
# General info
*Jeszcze nie gotowa, najpozniej wieczor 23.04 bedzie ukonczona*\

Multiplayer scrabble game

<a name="run"></a>
# Run

```
$ git clone https://git.e-science.pl/rlis241385_dpp/rlis_flaskapi.git
$ cd rlis_flaskapi/scrabble
$ docker build -t game .
$ docker run -p 5000:5000 game
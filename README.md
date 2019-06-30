


<img src = "https://github.com/hug58/Lemon-Tank/blob/master/screenshot.png">

<br>

<h3> REQUIERE PYTMX </h3>
<p> Para trabajar con Tiled se necesita este módulo para leer archivos tmx, 
	también si desea puede usar json, pero por comodidad prefiero este </p> 

<p> Un juego bastante sencillo usando pygame, y el módulo socket para el multijugador,
  el cliente-servidor es bastante simple. </p> 
  
  <p> El socket funciona enviando y recibiendo un diccionario del jugador (Player 1) 
  al otro jugador (player 2) y viceversa, de esta forma cada jugador recibe información del contrario. <p>
  
 
    key = {
	  'SPACE': False,
	  'LEFT': False,
	  'RIGHT': False,
	  'UP': False,
    'x': 300,
    'y': 300,

    'angle':0,
    'fire_load':False,
    'player': 0,
    'lifes': 3,
    }




 

  El cliente lo vuelve a convertir en un dict de python, se comprueba qué teclas an sido pulsadas, y luego
  realiza la acción.

</p>

<br>


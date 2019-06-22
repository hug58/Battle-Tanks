

<img src = "https://github.com/hug58/Lemon-Tank/blob/master/screenshot.png">

<br>

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


 <h3> Rota con las flecha izquierda (LEFT) Y derecha(right) y 
  avanza con la flecha de arriba (up),dispara en la barra de espacio (space) </h3>

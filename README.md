


<img src = "https://github.com/hug58/Lemon-Tank/blob/master/screenshot.png">

## Dependencias 
<p> Para trabajar con Tiled se necesita este módulo para leer archivos tmx, 
    La ventaja que ofrece es la capacidad de poder leer superficies (capas) fácilmente, algo que es un problema en json

    pip install pygame
    pip install pytmx
    
   Obviamente también se necesita python y pygame
</p> 


## Multijugador

<p> Quería crear un juego que fuera multijugador pero que no se limitara a una sola pc, osea, crear un socket que transmitiera información de estado de un jugador al otro (red lan si prefieres), y el resultado a quedado bastante bien. </p> 
  
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


## Controles 

* Izquierda: Rotar hacia la izquierda(-)  
* Derecha: Rotar hacia la derecha(+)  
* Space: Fuego!
* Arriba: Mover   


## Más sobre el socket

<p>
 Gran parte del socket lo hice del tutorial de Tech With Tim:
<a href="https://www.youtube.com/watch?v=F257x_E6H4k&t=2s">Tutorial</a>
</p>





<img src = "https://github.com/hug58/Lemon-Tank/blob/master/Captura.png">


## Dependencias 

  
 ```python

    Python 3.6 +

```

<p> Para trabajar con Tiled se necesita este módulo para leer archivos tmx, 
    La ventaja que ofrece es la capacidad de poder leer superficies (capas) fácilmente, algo que es un problema en json

</p>

```bash
    pip install pygame
    pip install pytmx
```
   


## Multijugador

<p> Quería crear un juego que fuera multijugador pero que no se limitara a una sola pc, osea, crear un socket que transmitiera información de estado de un jugador al otro (red lan si prefieres), y el resultado a quedado bastante bien. </p> 
  
  <p> El socket funciona recibiendo la clase Player de los demás jugadores, mientras se actualiza todo los atributos de
  esos jugadores. Un jugador solo puede enviar el objecto de la clase correspondiente, por lo tal deben de haber minimo 2 jugadores para que haya un intercambio de información.<p>
  
 

</p>


## Controles 


** Movimiento

* Izquierda: A  
* Derecha: D  
* Arriba: W
* Abajo: S
   
** Torreta

* Izquieda: I
* Derecha: P
* Disparar: O




## Más sobre el socket

<p>
 Gran parte del socket lo hice del tutorial de Tech With Tim:
<a href="https://www.youtube.com/watch?v=F257x_E6H4k&t=2s">Tutorial</a>
</p>


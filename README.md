# Visión artificial aplicada a un brazo robot (Computer vision control for a handler robot)

Se implementó un sistema clasificador de objetos, en donde se utilizó
la visión artificial para la detección de las posiciones y las características de los objetos,
para que luego puedan ser manipulados por un brazo robot.

Se desarrolló una plataforma de visión artificial, la cual consiste en una cámara webcam
como sistema de captura, una pc para el procesamiento de imágenes, y un brazo robot como
sistema dinámico. 

El brazo robot es controlado por la plataforma de hardware Arduino
UNO. 

<img src="_images/2.jpg" height="300">

Este Proyecto gano el premio [SASE2013](http://www.sase.com.ar/2013/concurso-de-proyectos-estudiantiles/) del congreso Argentino de sistemas embebidos (UBA)

---
El procesamiento consiste en la aplicación de algoritmos y transformaciones de las
imágenes de forma de obtener la información necesaria para manipular el sistema dinámico
y realizar la tarea asignada. Para ello se utilizó la librería de **visión artificial OpenCV,
especialmente sus funciones Histograms, Contours, Moments, ConvexHull, ConvexDefects**,
Meanshift y Camshift, con los cuales se implementaron principalmente los siguientes
algoritmos de reconocimiento de ciertas características de los objetos en imágenes (color y
tamaño) y seguimiento de objetos en una secuencia de imágenes.
Para lograr flexibilidad, portabilidad y la posibilidad de realizar futuras mejoras al
software se desarrolló íntegramente con herramientas libres y de código abierto (lenguaje de
programación Python, PyQt y PyQt4 Designer para la interfaz gráfica).

Se realizaron pruebas de posicionamiento del brazo logrando un error máximo relativo
de 0,087 (8,7 %). 

A su vez se probó el algoritmo de detección de objetos en donde las
posiciones detectadas contuvieron menos del 8% de error, por lo que el funcionamiento del
algoritmo resultó muy aceptable.

<img src="_images/brazo1.gif" height="300">

<img src="https://j.gifs.com/J8rnXJ.gif" height="300">

--- 

## Recursos 

En los siguientes links se describe la funcionalidad en video detallado, para cada aplicación: 

+ [Aplicación 1 - parte 1](https://youtu.be/nQJZ3TgWzf0)

+ [Aplicación 1 - parte 2](https://youtu.be/dcXRqZSGfdI)

+ [Aplicación 2](https://youtu.be/QIql3Fn_dZQ)

## Conclusiones 

- Se elaboraron algoritmos de visión por computadora capaces de extraer la
información visual necesaria en tiempo real

- Se diseñó y construyó un brazo robot de 5 grados de libertad (DOF) con materiales de bajo costo.

- Se realizó el estudio de cinemática inversa permitiendo que el autómata manipule y clasifique los objetos conociendo solamente sus posiciones.

- El método geométrico utilizado resultó sencillo y se logró muy buena precisión.
- Se puede dar mayor funcionalidad al sistema e implementar nuevas aplicaciones mediante simples modificaciones.


## Trabajos futuros 

+ Inclusión de filtros predictivos Kalman.
+ Implementación de visión estéreo.
+ Utilizar cámaras digitales de mayor calidad.
+ Agregar funciones al sistema (más aplicaciones).
+Incorporar a la plataforma un autómata de mayor tamaño y
capacidad (brazo industrial).
+ Implementar realimentación activa del brazo robot.
+ Desarrollar un sistema embebido capaz de realizar el
procesamiento de datos.
+ Agregar sensores al efector final del brazo robot.
+ Aumentar grados de libertad del autómata.
+ Integración del sistema desarrollado al entorno ROS.
+ Implementar un control a distancia del sistema vía Internet
(servidor SSL)





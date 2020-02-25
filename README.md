# TFG
## Estructura
### Android_app
Se encuentra dentro de la carpeta android_app subdividida en:
  - app.zip: aplicación completa exportada de Android Studio.
  - archivos_java: ficheros fuente de los archivos .java usados en la aplicación.
  - archivos_xml: ficheros fuente de los archivos .xml usados en la aplicación.
### Archivos 3d
Contiene los archivos stl originales y modificados usados durante la construcción del dron.
### Control
Contiene el archivo "controlador.py" que es el encargado de gestionar todos los archivos.
### Memoria
Contiene la memoria en pdf y docx del trabajo.
### Reconocimiento
Desarrollado para versiones de tensorFlow < 2.0.

Se encuentra dentro de la carpeta reconocimiento subdividida en:
  - capturas: carpeta deonde se guardan las imágenes durante un recorrido.
  - modelos: carpeta donde se almacenan los modelos pre entrenados de tensorflow.
  - testVideos: carpeta con videos usados para testear el funcionamiento del algoritmo.
  - labels: contiene el archivo "label.pbtxt" con la clase que buscamos reconocer.
  - utils: contiene todas las librerías y archivos que la api necesita para funcionar.
### Sensores
Contiene la carpeta "navio" con los drivers de la placa además de los siguientes archivos:
  - serv_socket.py: archivo correspondiente al servidor tcp.
  - led.py: archivo de control de los leds de la parte superior.
  - barometro: su utilidad es la de devolvernos la altura a la que se encuentra el aparato.



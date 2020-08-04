## Estructura
### Android_app
Se encuentra dentro de la carpeta android_app subdividida en:
  - app.zip: aplicación completa exportada de Android Studio.
  - archivos_java: ficheros fuente de los archivos .java usados en la aplicación.
  - archivos_xml: ficheros fuente de los archivos .xml usados en la aplicación.
### Archivos 3d
Contiene los archivos stl originales y modificados usados durante la construcción del dron.
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
  - barometro.py: permite conocer la altura a la que se encuentra el dron.
  - acelerometro.py: devuelve información sobre el pitch, roll y yaw corregido.
  - Complementary_Filter.py: realiza las mediciones del acelerómetro, magnetómetro y giroscopio filtrando estas últimas
    calculando además pitch, roll y yaw (actúa como driver).
  - gps.py: proporciona información acerca de las coordenadas (latitud y longitud).

### Simulador
Contiene tres archivos referentes a la simulación virtual del prototipo:
 - graf.py: reproduce el resultado de la simulación creando una gráfica que evoluciona temporalmente, variando su posición, velocidad y orientación.
 - uav.py: en él, esta programado el modelo y el controlador del dron.
 - simulador.py: lanza una simulación basada en los parámetros del archivo uav.py.
 
 ### Videos
 Contiene todos los videos explicados en la memoria organizados en subcarpetas.

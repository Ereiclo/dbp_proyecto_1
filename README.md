# dbp_proyecto_1
## Nombre del Proyecto: Apuestas BETSEC
### Integrantes:
- Eric Bracamonte
- Juan Diego Laredo
- Salvador Olivares
- Gabriel Suárez    

# Instrucciones de uso: 
- Crear una base de datos en postgres (modificar la uri en el "app.py" a gusto)
- Hacer flask db upgrade en consola
- Desde la consola de python (antes de entrar asegurénse de estar dentro de la carpeta dbp_proyecto_1), copiar y pegar el archivo "inicializacion_db.txt"
- Ejecutar el archivo app.py y listo, ahora pueden entrar a la página web!

*Es necesario tener los requisitos mencionados en el archivo requirements.txt*
# Descripción del Proyecto:

El proyecto consiste en una casa de apuestas relacionada a la Copa América que se disputa este año. Un usuario podrá registrarse y logearse para apostar a su equipo favorito, de acuerdo a su porcentaje de ganancia y dinero que invierta.

# Objetivos:
- Lograr que un usuario invierta dinero y se almacene en la base de datos.

# Misión:
- Lograr que las personas puedan apostar sin problemas en nuestra página web.

# Visión:
- Ser una página web auto-sostenible y funcional

# Información:
## Back-end:
- Creación de la base de datos Proyecto1, con sus respectivas tablas a través de Class-db.Model.
- Creación de app-routes, donde:
    Se redirecciona usando render template hacia un html.
    Se redirecciona hacia otra página.
    Se obtiene datos de JavaScript y se guardan datos en las tablas usando JSON.
## Templates (como back-end):

Son 4 en total:
- Index: Pagina inicial de la web. Aquí se inicia sesión o se registra el usuario. 

- Partidos: La página principal de la web. Aquí se crea la relación de partidos y la función en JavaScript que se ejecutará cuando el usuario quiera apostar por un equipo. 
- Apuestas: La página accederá a los datos de las apuestas en las que el usuario haya invertido.

- Depositar: Esta página permite tanto agregar una tarjeta de crédito como eliminar 


# Front-end:
Uso de funciones básicas del boostrap, tales como: Containers, Clase Row para tener un mejor manero de posicionamiento, tomando en consideración el orden. 

Se usó una barra Nav para la navegación rápida en los 4 htmls.
Por último, se implementó un CSS Style para vizualisar de mejor forma los resultados de las consultas a la base de datos.

# Script para la db: inicializacion_db.txt
# API: app.py

En el archivo.py llamado app encontramos todas las funciones usadas para enviar mensajes entre el cliente y la base de datos. Aquí se encuentran funciones de lógica que comprueban, por ejemplo, el inicio de sesión o el correcto registro. Tambien tenemos funciones actualizar datos, como la funcion agregar_dinero. Esta, dentro del html de depositar, sirve para aumentar el dinero en cuenta del usuario. El app.py es el núcleo del funcionamiento de la página web, es donde se encuentra la lógica del backend. 


# Requests:
            Ingresar los datos para poder ingresar a la página web.
            Hacer click en un boton para realizar una apuesta por un equipo.
            Insertar una tarjeta para poder apostar.
            Ingresar el monto a apostar.
# Respuestas:
            Si se logea de manera eficiente, se le deja pasar a la página principal. Sino, salta un mensaje de error y se vuelve a intentar.
            Al hacer click en submit cuando se ingresa el dinero, se guarda en la base de datos.
            Respecto al menu, en cada opción se redirige a la pestaña correspondiente.
            
# Host: LocalHost

# Autenticación: 
        Se usa la autenticación por password. Comprobamos que el usuario ingresado es el mismo que en la misma base de datos, además de comprueba que las contraseñas coinciden.

# Manejo de Errores:
        Error 500: Cuando ocurrió este error, siempre revisabamos e inspecionabamos la consola en la página web y el terminal de windows.
        Error 404: Se ha configurado todas las request de forma que este error no puede ocurrir cuando uno accede a algun recurso dentro de los html creados para la página. Aun así no hemos planeado el manejo de este error cuando el usuario quiere hacer a un recurso, desde la url, que no existe. 
        


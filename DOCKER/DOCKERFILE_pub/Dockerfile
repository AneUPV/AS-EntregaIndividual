##################################################################
#	  DOCKERFILE para crear el cliente NATS PUBLISHER	   #
##################################################################

# Imagen tomada como base -> Ubuntu
FROM ubuntu

# Descargar e instalar dependencias para ejecutar el cliente
# Actualizar y conseguir instalador de paquetes pip para python
RUN apt -qq update && apt -qq -y install python3-pip

# Instalar librerías python necesarias
RUN pip install nats-python
RUN pip install nats-py

# Crear la carpeta 'code'
RUN mkdir /code

# Establecer directorio 'code' como directorio de trabajo
WORKDIR /code

# Copiar el cliente python PUBLISHER de NATS dentro del directorio 
# de trabajo del contenedor
COPY cliente-nats-pub.py .


# Establecer como comando de arranque la ejecución del cliente 
# Utilizando las instrucciones CMD y ENTRYPOINT , le indicamos al 
# contenedor que ejecute cliente-nats-pub.py de Python cuando se
# inicie el contenedor.
CMD ["cliente-nats-pub.py"]
ENTRYPOINT ["python3"]



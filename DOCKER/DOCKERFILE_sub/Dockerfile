##################################################################
#	DOCKERFILE para crear el cliente NATS SUBSCRIBER	 #
##################################################################

# Imagen que toma de base -> Ubuntu
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

# Copiar el cliente python SUBSCRIBER de NATS dentro del directorio 
# de trabajo del contenedor
COPY cliente-nats-sub.py .

# Establecer como comando de arranque la ejecución del cliente. 
# Utilizando las instrucciones CMD y ENTRYPOINT , le indicamos al 
# contenedor que ejecute el cliente-nats-sub.py de Python cuando se
# inicie el contenedor.
CMD ["cliente-nats-sub.py"]
ENTRYPOINT ["python3"]


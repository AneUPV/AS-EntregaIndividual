########################################################
#         NATS MESSAGING -CLIENTE PYTHON PUBLISHER       #
##########################################################

# Importar las librerías y dependencias para el programa
import asyncio
import time
# nats tiene una librería para implementar clientes en el lenguaje Python
import nats
# libreria para generar números random
import random


# Asyncio es una biblioteca de Python para escribir codigo concurrente
# utilizando la sintaxis async/await. Asyncio es utilizado como base en
# múltiples frameworks asíncronos de Python y provee un alto rendimiento
# en redes y servidores web

# FUENTES: https://nats-io.github.io/nats.py/modules.html#asyncio-client
#          https://nats-io.github.io/nats.py/


time.sleep(2)
    # Variable boolean para controlar si un evento ha ocurrido

   
    # Ruta para el LOG
path = "/logNats/log-nats.txt" 
   # Variable para la fecha y hora
ahora = time.strftime("%c")
    
nc = nats.connect('servidor-nats:4222')
time.sleep(20)
print(str(nc))
nc.subscribe('admin-sistemas')
nc.publish('admin-sistemas',b'A continuacion se enviaran NUMEROS ALEATORIOS ')

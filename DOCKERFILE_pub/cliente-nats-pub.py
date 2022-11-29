##########################################################
#         NATS MESSAGING -CLIENTE PYTHON PUBLISHER       #
##########################################################

# Importar las librerías y dependencias para el programa
import asyncio
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


# Programa principal
async def main():

    # Variable boolean para controlar si un evento ha ocurrido
    is_done = asyncio.Future()
    # IP estática que corresponde al servidor nats
    ip="172.16.238.20"


    # Metodo de cierre de conexión
    async def closed_cb():
        print('Conexión a NATS server se ha cerrado con éxito!!')
        is_done.set_result(True)

    # Establecer conexión con localhost:4222
    async with (await nats.connect(ip+':4222', closed_cb=closed_cb)) as nc:

        # Prints informativos
        print (f'-> Conectado al server NATS :: IP -> {nc.connected_url.netloc}...')
        print ('')
        print ('........................................')
        print ('.       CLIENTE NATS - PUBLISHER       .')
        print ('........................................')
        print ('')
        print (' DESCRIPCIóN: Este cliente se suscribirá al tópico "admin-sistemas"')
        print (' y publicará mensajes. El otro cliente python, el SUBSCRIBER       ')
        print (' [cliente-nats-pub.py] deberá recibir los mensajes enviados por el ')
        print (' PUBLISHER')

        print ('#####################################################################')
        print ('')
        print ('-  ENVIANDO mensajes...  -')
        print ('')
        print ('     [ESTADO]         [TÓPICO]            [MENSAJE]')
        print ('--------------------------------------------------------------')


    # En este método se muestran por output los mensajes que se reciben.
    # Será el método gestor de mensajes
        async def subscribe_handler(msg):
            subject = msg.subject
            reply = msg.reply
            data = msg.data.decode()

            print('Mensaje ENVIADO [{subject}] : {data}'.format(subject=subject, reply=reply, data=data))

        # Suscribirse al tópico ‘admin-sistemas’
        await nc.subscribe('admin-sistemas', cb=subscribe_handler)
        await nc.flush()

        # Envía 30 mensajes al tópico 'admin-sistemas'. Los mensajes serán  
        # números aleatorios
        for i in range(0, 30):
                        
            if i == 0:
                # Se publica un mensaje, indicando tópico y contenido
                await nc.publish('admin-sistemas',b'A continuacion se enviaran NUMEROS ALEATORIOS ')
            else:
                if i == 29:
                    # Se publica un mensaje, indicando tópico y contenido
                    await nc.publish('admin-sistemas',b'Este mensaje es de despedida, Agur!!!')
                else:
                    # Se consigue el número aleatorio y se publica el mensaje
                    numero = str(random.randrange(1,20000))
                    await nc.publish('admin-sistemas',b'NUMERO: '+ numero.encode('utf-8'))
            # Espera medio segundo entre mensajes
            await asyncio.sleep(0.5)

        # Estos mensajes son leidos por el cliente SUBSCRIBER, ya que está a la escucha en el 
        # tópico 'admin-sistemas'.
        print("###########################################")
        print("#   A espera del cliente SUBSCRIBER...    #")
        print("###########################################")


    await asyncio.wait_for(is_done, 60.0)

if __name__ == '__main__':
    # Se ejecuta el programa principal
    asyncio.run(main())

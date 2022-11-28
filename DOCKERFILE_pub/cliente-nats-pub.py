##########################################################
#         NATS MESSAGING -CLIENTE PYTHON PUBLISHER       #
##########################################################

import asyncio
import nats
import random


# Asyncio es una biblioteca de Python para escribir codigo concurrente
# utilizando la sintaxis async/await. Asyncio es utilizado como base en
# múltiples frameworks asíncronos de Python y provee un alto rendimiento
# en redes y servidores web

# FUENTES: https://nats-io.github.io/nats.py/modules.html#asyncio-client
#          https://nats-io.github.io/nats.py/


async def main():

    # Variable boolean para controlar si un evento ha ocurrido
    is_done = asyncio.Future()

    ip="172.16.238.20"


    # Metodo de cierre de conexión
    async def closed_cb():
        print('Conexión a NATS server se ha cerrado con éxito!!')
        is_done.set_result(True)

    # Establecer conexión con localhost:4222
    async with (await nats.connect(ip+':4222', closed_cb=closed_cb)) as nc:

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


    # En este método el cliente se suscribe al tópicoadmin-sistemas'
    # y se muestran por output los mensajes que recibe.
        async def subscribe_handler(msg):
            subject = msg.subject
            reply = msg.reply
            data = msg.data.decode()

            print('Mensaje ENVIADO [{subject}] {reply}: {data}'.format(subject=subject, reply=reply, data=data))

        # Suscribirse
        await nc.subscribe('admin-sistemas', cb=subscribe_handler)
        await nc.flush()

        # Envía 10 mensajes al tópico 'topico-pruebas'
        for i in range(0, 25):
                        
            if i == 0:
                await nc.publish('admin-sistemas',b'A continuacion se enviaran NUMEROS ALEATORIOS ')
            else:
                if i == 24:
                    await nc.publish('admin-sistemas',b'Este mensaje es de despedida, Agur!!!')
                else:
                    numero = str(random.randrange(1,20000))
                    await nc.publish('admin-sistemas',b'NUMERO: '+ numero.encode('utf-8'))
            # Espera 1 segundo entre mensajes
            await asyncio.sleep(1)


    await asyncio.wait_for(is_done, 60.0)

if __name__ == '__main__':
    asyncio.run(main())

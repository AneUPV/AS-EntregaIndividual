#################################################
#         NATS MESSAGING -CLIENTE PYTHON        #
#################################################

import asyncio
import nats

# Asyncio es una biblioteca de Python para escribir codigo concurrente
# utilizando la sintaxis async/await. Asyncio es utilizado como base en
# múltiples frameworks asíncronos de Python y provee un alto rendimiento
# en redes y servidores web

# FUENTES: https://nats-io.github.io/nats.py/modules.html#asyncio-client
#          https://nats-io.github.io/nats.py/


async def main():

    # Variable boolean para controlar si un evento ha ocurrido 
    is_done = asyncio.Future()

    # Metodo de cierre de conexión
    async def closed_cb():
        print('Conexión a NATS server se ha cerrado con éxito!!')
        is_done.set_result(True)

    # Establecer conexión con localhost:4222
    async with (await nats.connect('localhost:4222', closed_cb=closed_cb)) as nc:
        print(f'Conectado al server NATS -> {nc.connected_url.netloc}...')


    # En este método el cliente se suscribe al tópico 'topico-pruebas'
    # y se muestran por output los mensajes que recibe.

        async def subscribe_handler(msg):
            subject = msg.subject
            reply = msg.reply
            data = msg.data.decode()
            print('Mensaje recibido en el tópico {subject} {reply}: {data}'.format(subject=subject, reply=reply, data=data))

        # Suscribirse
        await nc.subscribe('topico-pruebas', cb=subscribe_handler)
        await nc.flush()

        # Envía 10 mensajes al tópico 'topico-pruebas'
        for i in range(0, 12):

            numero = str(i)
            if i == 0:
                await nc.publish('topico-pruebas',b'A continuacion se enviaran 10 mensajes: ')
            else:
                if i == 11:
                    await nc.publish('topico-pruebas',b'Este mensaje es de despedida, Agur!!!')
                else:
                    await nc.publish('topico-pruebas',b'Este es el mensaje numero '+ numero.encode('utf-8'))
            # Espera 1 segundo entre mensajes
            await asyncio.sleep(1)
            

    await asyncio.wait_for(is_done, 60.0)

if __name__ == '__main__':
    asyncio.run(main())

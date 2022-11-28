############################################################
#         NATS MESSAGING - CLIENTE PYTHON SUBSCRIBER       #
############################################################

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
    ip="172.16.238.20"


    # Metodo de cierre de conexión
    async def closed_cb():
        print('Conexión a NATS server se ha cerrado con éxito!!')
        is_done.set_result(True)

    # Establecer conexión con localhost:4222
    async with (await nats.connect(ip+':4222', closed_cb=closed_cb)) as nc:
        print(f'->Conectado al server NATS :: IP -> {nc.connected_url.netloc}...')
        print ('')
        print ('.........................................')
        print ('.       CLIENTE NATS - SUBSCRIBER       .')
        print ('.........................................')
        print ('')
        print (' DESCRIPCIóN: Este cliente se suscribirá al tópico "admin-sistemas" ')
        print (' y leerá los mensajes que lleguen a él. El otro cliente python, el  ')
        print (' PUBLISHER [cliente-nats-pub.py] deberá enviar los mensajes para que')
        print (' el SUBSCRIBER los lea.')
        print ('#####################################################################')
        print ('')
        print ('-  ESPERANDO mensajes...  -')
        print ('')
        print ('     [ESTADO]         [TÓPICO]            [MENSAJE]')
        print ('--------------------------------------------------------------')

    # En este método el cliente se suscribe al tópico 'admin-siemas'
    # y se muestran por output los mensajes que recibe.

        async def subscribe_handler(msg):

            subject = msg.subject
            reply = msg.reply
            data = msg.data.decode()
            if not data ==  None:

                print('NUEVO mensaje en [{subject}] {reply}: {data}'.format(subject=subject, reply=reply, data=data))

        # Suscribirse
        await nc.subscribe('admin-sistemas', cb=subscribe_handler)
        await nc.flush()

        # Dejar contenedor inactivo a la escucha
        msg = await sub.next_msg()


    await asyncio.wait_for(is_done, 60.0)

if __name__ == '__main__':
    asyncio.run(main())


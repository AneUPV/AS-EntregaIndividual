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

    #async def subscribe_handler(msg):
    # Dejar contenedor inactivo a la escucha
    #    try:
    #        subject = msg.subject
    #        reply = msg.reply
    #        data = msg.data.decode()
    #        await asyncio.sleep(1)
    #        print('NUEVO mensaje en [{subject}] {reply}: {data}'.format(subject=subject, reply=reply, data=data))
    #    except:        
    #        print('----------------------')
    #        print('Tópico:', msg.subject)
    #        print('Datos   :', msg.data)
    #        print('Cabeceras:', msg.header)
    #        subject = msg.subject
    #        reply = msg.reply
    #        data = msg.data.decode()
    #        print('NUEVO mensaje en [{subject}] {reply}: {data}'.format(subject=subject, reply=reply, data=data))

    # Metodo de cierre de conexión
    async def closed_cb():
        print('Conexión a NATS server se ha cerrado con éxito!!')
        is_done.set_result(True)

    # Metodo de desconexión
    async def disconnected_cb():
        print('Cliente SUBSCRIBER se ha desconectado')

    async def reconnected_cb():
        print(f'Se ha reconectado a {nc.connected_url.netloc}')

    async def error_cb(e):
        print(f'Ha ocurrido un error: {e}')


    # Establecer conexión con nats-servidor:4222
    nc = await nats.connect(ip+':4222',error_cb=error_cb,reconnected_cb=reconnected_cb,disconnected_cb=disconnected_cb,closed_cb=closed_cb)
    
    
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
    
    # Suscribirse
    sub = await nc.subscribe('admin-sistemas')

    while True: 
        print('')
        print('> Esperando mensajes...')
        # next_msg se puede usar para recuperar el siguiente mensaje de una secuencia
        # de mensajes usando la sintaxis 'await', pero esto solo funciona cuando no se
        # pasa una devolución de llamada al suscribirse.
        msg = await sub.next_msg(timeout = 200)
           
        await nc.flush()
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
            
        print('>> NUEVO mensaje en [{subject}] {reply}: {data}'.format(subject=subject, reply=reply, data=data))        

    await asyncio.wait_for(is_done, 60.0)

if __name__ == '__main__':
    asyncio.run(main())


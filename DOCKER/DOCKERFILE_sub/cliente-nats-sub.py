############################################################
#         NATS MESSAGING - CLIENTE PYTHON SUBSCRIBER       #
############################################################

# Importar las librerías y dependencias para el programa
# Importar librería Asyncio
import asyncio
# Nats tiene una librería para implementar clientes en el lenguaje Python
import nats
# Librería necesaria para escribir la fecha en el registro de mensajes y esperar
import time

# Asyncio es una biblioteca de Python para escribir codigo concurrente
# utilizando la sintaxis async/await. Asyncio es utilizado como base en
# múltiples frameworks asíncronos de Python y provee un alto rendimiento
# en redes y servidores web

# FUENTES: https://nats-io.github.io/nats.py/modules.html#asyncio-client
#          https://nats-io.github.io/nats.py/

##################################################################
#                       PROGRAMA PRINCIPAL                       #
##################################################################
async def main():

    # Tiempo para asegurarse de que al servidor le ha dado tiempo de arrancar
    time.sleep(7)
    # Variable boolean para controlar si un evento ha ocurrido
    is_done = asyncio.Future()
    
    
    # Metodo de cierre de conexión
    async def closed_cb():
        print('Conexión a NATS server se ha cerrado con éxito!!')
        is_done.set_result(True)

    # Establecer conexión con servidor-nats:4222
    async with (await nats.connect('servidor-nats:4222', closed_cb=closed_cb)) as nc:
        print(f'Conectado al servidor NATS --> {nc.connected_url.netloc}...')

	# Método gestor de suscripciones. Este se ejecuta cada vez que se recibe un mensaje en 
	# un tópico en el que está suscrito el cliente
        async def subscribe_handler(msg):
            subject = msg.subject
            reply = msg.reply
            data = msg.data.decode()
            # Enseñar por pantalla el mensaje recibido
            print('>> NUEVO mensaje en [{subject}] {reply}: {data}'.format(subject=subject, reply=reply, data=data))
	
	# Prints informativos
        print(f'->Conectado al server NATS :: IP -> {nc.connected_url.netloc}...')
        print ('')
        print ('')
        print ('Fichero log disponible ---> /log/log-nats.txt')
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
        
        # En este punto el cliente se suscribe al tópico 'admin-sistemas'

        # Suscribirse
        await nc.subscribe('admin-sistemas', cb=subscribe_handler)
        await nc.flush()

	# En este bucle, el programa hará tiempo para quedarse a la escucha del publisher. Si no, el cliente acabaría rápidamente
	# y no llegaría a recibir ningún mensaje porque el contenedor se cerraría de inmediato.
        for i in range(0, 100):
            await asyncio.sleep(0.6)
            
    # Este método espera a que el programa haya acabado y hace un wait 
    # de 10 segundos antes de acabar
    await asyncio.wait_for(is_done, 10.0)

if __name__ == '__main__':
    # Se ejecuta el programa principal
    asyncio.run(main())

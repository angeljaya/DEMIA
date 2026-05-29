import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import messaging  # Nueva librería para enviar notificaciones push
import time

# 1. Configurar la llave de seguridad de Firebase
cred = credentials.Certificate("llave.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

print("==================================================")
print("  MONITOR DE POSTS CON ENVÍO DE NOTIFICACIONES    ")
print("==================================================")
print("Vigilando 'posts' y listo para enviar alertas masivas...\n")

primer_bloque_leido = False

# 2. Función para ordenar a Firebase que envíe la notificación push a todos
def enviar_push_familiar(usuario, mensaje):
    # Creamos la estructura de la notificación que flotará en el celular
    notificacion = messaging.Notification(
        title="🔔 ¡Nueva publicación en DEMIA!",
        body=f"@{usuario} dice: {mensaje}"
    )
    
    # Configuramos el mensaje apuntando al tema (topic) 'familia'
    mensaje_fcm = messaging.Message(
        notification=notificacion,
        topic="familia"  # Todos los celulares suscritos a este tema recibirán la alerta
    )
    
    try:
        # Python le da la orden a Firebase y Firebase la distribuye a los teléfonos
        respuesta = messaging.send(mensaje_fcm)
        print(f"🚀 ¡Notificación Push enviada con éxito a toda la familia!")
    except Exception as e:
        print(f"❌ Error al intentar enviar la notificación Push: {e}")

# 3. Función que reacciona a las publicaciones en tiempo real
def al_detectar_publicacion(snapshots, cambios, fecha_actual):
    global primer_bloque_leido
    
    if not primer_bloque_leido:
        primer_bloque_leido = True
        return 
        
    for cambio in cambios:
        if cambio.type.name == 'ADDED':
            datos = cambio.document.to_dict()
            
            usuario = datos.get('hermano') or datos.get('usuario') or datos.get('autor') or 'Alguien de la familia'
            mensaje = datos.get('texto') or datos.get('post') or datos.get('nota') or datos.get('mensaje') or 'Nueva publicación'
            
            print(f"\n📢 Publicación detectada en el muro.")
            print(f"👤 @{usuario}: {mensaje}")
            
            # Lanzamos la alerta colectiva
            enviar_push_familiar(usuario, mensaje)

# 4. Vigilar la colección 'posts'
coleccion_posts = db.collection('posts')
monitor_muro = coleccion_posts.on_snapshot(al_detectar_publicacion)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nMonitor apagado.")
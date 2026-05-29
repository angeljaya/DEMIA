// 1. Importar los scripts necesarios de Firebase
importScripts('https://www.gstatic.com/firebasejs/9.0.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.0.0/firebase-messaging-compat.js');

// 2. TUS CREDENCIALES REALES extraídas de tu captura de pantalla:
const firebaseConfig = {
    apiKey: "AIzaSyABMNSOKZMsRVSBdogqhBDULQ2ArvyMr9A",
    authDomain: "demia-f9708.firebaseapp.com",
    projectId: "demia-f9708",
    storageBucket: "demia-f9708.firebasestorage.app",
    messagingSenderId: "1004088726819",
    appId: "1:1004088726819:web:ba2132e526491577816896"
};

firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging();

// 3. Recibir la notificación cuando la app está en segundo plano o cerrada
messaging.onBackgroundMessage((payload) => {
    console.log('Notificación recibida en segundo plano: ', payload);

    const tituloNotificacion = payload.notification.title;
    const opcionesNotificacion = {
        body: payload.notification.body,
        icon: '/icono.png' // Si tienes un logo en tu proyecto, pon su ruta aquí
    };

    self.registration.showNotification(tituloNotificacion, opcionesNotificacion);
});
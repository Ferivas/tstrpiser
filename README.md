# tstrpiser
Prueba puerto serial del Raspberry
Se utiliza la siguiente tarjeta para señalizar con un led (en este ejemplo conectado a GPIO4) si funciona el puerto serial del Raspberry.
Hay que unir los pines de RX y TX del Rpi (en este caso el led titila rápido) y si los pines no están unidos el led parpadea lento.

También se uriliza la entrada GPIO22 para apagar el Rpi (con un shutdown) si se mantiene presionado por más de 6 segundos.


# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 16:11:27 2021
Programa para enviar comandos por el puerto serial y obtener respuesta
@author: Fernando
"""

import serial
import time
import binascii as ubinascii

print("TEST SERIAL")

runpi=True
if runpi:
    import RPi.GPIO as GPIO
    #PUERTO="/dev/ttyUSB0"
    PUERTO="/dev/serial0"
  
else:    
    PUERTO="COM5"
ser = serial.Serial(PUERTO, 9600,timeout=1)
if runpi:
    led_b=4  #Proc archivos 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led_b, GPIO.OUT) ## GPIO 18 como salida
    GPIO.output(led_b, False)
    time.sleep(1)
    GPIO.output(led_b, False)

def sndcmd(comando):
    salida="SETSAL,"+comando
    salidab=str.encode(salida)
    crccalc=ubinascii.crc32(salidab)
    salida="%%"+salida+"&"+'{0:X}'.format(crccalc)
    print (salida)
    salida=salida+"\r\n"
    ser.write(salida.encode('ascii'))
    ackok=False
    tled=0
    while not ackok:
        try:
            arxb=ser.readline()
        except:
            arxb=None
        if arxb!=None:
            try:
              arx=str(arxb.decode("ascii"))
            except:
              arxb=None
              arx=''
        if len(arx)>0:
            print(arx)
            ackok=True
            if arx[0]=='$':
                arx1=arx[1:-2]
                lista=arx1.split('&')
                if len(lista)==2:
                    datob=str.encode(lista[0])
                    crccalc=ubinascii.crc32(datob)
                    #print("CRCcal=",crccalc) 
                    crcval='0x'+lista[1]
                    try:
                        crcdec=int(crcval,0)
                    except:
                        crcdec=0
                    #print("CRCrx=",crcdec)
                    if crccalc==crcdec:
                        print('CRC OK')
                        ackok=True
                else:
                    print('Sin CRC')                        

        tled=tled+1
        if runpi:
            if tled==0:
                GPIO.output(led_b, False)
                ackok=True
            else:
                GPIO.output(led_b, True)
                ackok=True           
    print("OK CMD")

cntr=0    
while True:
    try:
        print(cntr)
        cntr=cntr+1
        cmd=str(cntr)
        sndcmd(cmd)
        GPIO.output(led_b, False)
        time.sleep(1)
        GPIO.output(led_b, True)
        
    except KeyboardInterrupt:
        print('Fin por teclado')
        ser.close()
        break    

    


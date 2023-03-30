import machine
from time import sleep
import random
import time

#Informacion = open("Datos_recolectados.txt", "w")

#tiempo en millis
none = 0
Bajo = 800
Medio = 1600
Alto = 2400

#Vector de datos

vector_temporal = [[[0, none],[0, none]],
                   [[0, Bajo],[0, Medio]],
                   [[1, Medio],[1, Alto]],
                   [[1, Bajo],[0, Alto]],
                   [[1, Alto],[0, Bajo]],
                   [[0, Medio],[1, Medio]],
                   [[1, Bajo],[1, Alto]],
                   [[0, Alto],[0, Bajo]],
                   [[0, Alto],[1, Medio]],
                   [[0, none],[0, none]]]

#Variables

tiempo_valvula_solenoide_1 = 0
tiempo_valvula_solenoide_2 = 0

Numero_pulsos = 0
Caudal = 0
SEG1 = 0
SEG2 = 0
calculo = 0
numeracion = 0
Porcentaje_anterior = 0
valvula_Open = False
        
Pin_rele = machine.Pin(18, machine.Pin.OUT)
Valvula_open = machine.Pin(19, machine.Pin.OUT)
Valvula_close = machine.Pin(20, machine.Pin.OUT)
Electrovalvula_0 = machine.PWM(machine.Pin(21))
Electrovalvula_0.freq(10)
Electrovalvula_1 = machine.PWM(machine.Pin(22))
Electrovalvula_1.freq(10)

reloj = machine.Timer()

Lista_valvulas = [Electrovalvula_0, Electrovalvula_1]
Lista_nombres = ["Electrovalvula_0", "Electrovalvula_1"]

Lista_estados_valvulas = [0,0,0,0]

class electrovalvulas:
    def __init__(self):
        #print("Inicializando...")
        self.Electrovalvula = ""
        self.Duty = 100
        self.Conversion = int((self.Duty * 65535) / 100)
        
    def electrovalvula_on(self, Nvalvula):
        self.Electrovalvula = "Electrovalvula_" +str(Nvalvula)
        for nombre in Lista_nombres:
            if self.Electrovalvula == nombre: 
                print("Encontrado")
                Lista_estados_valvulas[Lista_nombres.index(self.Electrovalvula)] = 1
                Lista_valvulas[Lista_nombres.index(self.Electrovalvula)].duty_u16(self.Conversion)
                break
            else:   
                None
    
    def electrovalvula_off(self, Nvalvula):
        self.Electrovalvula = "Electrovalvula_" +str(Nvalvula)
        for nombre in Lista_nombres:
            if self.Electrovalvula == nombre:
                #print("Encontrado")
                Lista_estados_valvulas[Lista_nombres.index(self.Electrovalvula)] = 0
                Lista_valvulas[Lista_nombres.index(self.Electrovalvula)].duty_u16(0)
                break
            else:
                None
                #print("Nulo")
  
class rele:
    def activacion(self, listado):
        if 1 in listado:
            #print('Sistema activo')
            Pin_rele.value(0)
            
        else:
            #print('Sistema inactivo')
            Pin_rele.value(1)
            #objeto_proporcional.cerrar()

class electrovalvula_proporcional:
    
    def __init__(self):
        self.calculo = 0
        
    def abrir(self, calculo):
        Valvula_close.value(1)
        time.sleep(calculo)
        Valvula_close.value(0)
        
    def cerrar(self):
        Valvula_open.value(1)
        time.sleep(0.55)
        Valvula_open.value(0)
        
class muestreo:
    
    def conteo(pin):
        global Numero_pulsos
        Numero_pulsos += 1
        
    def frecuencia(timer):
        global SEG
        
        if 1 in Lista_estados_valvulas:
            SEG += 1
            if SEG == tiempo_valvula_solenoide_1:
                objeto_electrovalvula.electrovalvula_off(0)
                objeto_rele.activacion(Lista_estados_valvulas)
                
                
            if SEG == tiempo_valvula_solenoide_2:
                objeto_electrovalvula.electrovalvula_off(1)
                objeto_rele.activacion(Lista_estados_valvulas)
        else:
            None
            #objeto_proporcional.cerrar()
            
    reloj.init(mode= machine.Timer.PERIODIC, period = 1, callback = frecuencia)

objeto_electrovalvula = electrovalvulas()
objeto_rele = rele()
objeto_proporcional = electrovalvula_proporcional()

valor_apertura = 90 #valor cierre
calculo = (valor_apertura * 0.55) / 100
objeto_proporcional.abrir(calculo)

for Data in vector_temporal:
    
    datos_posicion = [Data[0][0], Data[1][0]]
    datos_tamaño = [Data[0][1], Data[1][1]]
    
    if 1 in datos_posicion:
        #valor_apertura = 70
        #calculo = (valor_apertura * 0.55) / 100
        
        if 1 in Lista_estados_valvulas:
            None
        else:
            #objeto_proporcional.abrir(calculo)
            SEG = 0
            
        for posicion in range (0, len(datos_posicion)):
            if datos_posicion[posicion] == 1:
                objeto_electrovalvula.electrovalvula_on(posicion)
                if posicion == 0:
                    tiempo_valvula_solenoide_1 = tiempo_valvula_solenoide_1 + datos_tamaño[0]
                    #print(tiempo_valvula_solenoide_1)
                elif posicion == 1:
                    tiempo_valvula_solenoide_2 = tiempo_valvula_solenoide_2 + datos_tamaño[1]
                    #print(tiempo_valvula_solenoide_2)
            else:
                None
                
    objeto_rele.activacion(Lista_estados_valvulas)
    time.sleep(2.4)
objeto_proporcional.cerrar()

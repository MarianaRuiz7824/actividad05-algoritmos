import pandas as pd
import xlsxwriter
from datetime import datetime

Cadena = "TGTAGTGCAGTGGCGTGATCTTGGCTCACTGCAGCCTCCACCTTAGAGCAATCCTCTTGCCTCATCCTCCCGGGTAGTTGGGACTACATGTGCATGCCACATGCCTGGCTAATTTTTGTATTTTTAGTA"
Indices = {43 : "C", 15 : "A", 100 : "G", 54 : "A", 33 : "A", 19 : "G", 97 : "T", 13 : "A"};
Caracteres = list(Cadena);
Lista = [];

def recorrido(Cadena, Longitud, Recorrido,Indices):
    
    Auxiliar = {};

    for i in range(0, len(Cadena), Recorrido):

        for j in range(i, i + Longitud, 1):

            if j in Indices:
                Auxiliar[j] = Indices[j]; #Almacenar los datos de indices validos a intercambiar

        if(len(Auxiliar) > 0): 
           
            permutacion(len(Auxiliar), Auxiliar); 

        Auxiliar.clear();

def permutacion(N, Diccionario): #Reducir coste de memoria de m(2^n) a 2^n, solo me interesa los datos que cambian respecto al array original
                                 #Coste ejecución 2^n * m
  Auxiliar = {}
  Indices = list(Diccionario.keys());

  for i in range(2**N):

    for j in range(N -1, -1, -1):

      Posicion = (2**j); #Tasa Cambio

      if(i == 0):
          
          continue;

      Resultado = (i + Posicion) // Posicion; #Paridad  0 mod 2 = 0
      Paridad = Resultado % 2;

      if(Paridad == 0):
        #Número par, causa positiva.
        Auxiliar.update({ Indices[j] : Diccionario[Indices[j]]})

    if(len(Auxiliar) > 0):

        unico(Auxiliar);
    
    Auxiliar.clear();

def unico(Auxiliar):
   
  Unico = True

  for k in range(len(Lista)):
           
    if(Lista[k] == Auxiliar):
              
        Unico = False;
        continue;

  if(Unico):        

    Temporal = Auxiliar.copy();
    Lista.append(Temporal);

def compararLista(Inicio, Final):
   
  Auxiliar = {};
  Inicio -= 1

  for Inicio in range(Final):
     
     Auxiliar.update(Lista[Inicio])
  
  permutacion(len(Auxiliar), Auxiliar);

def imprimirArchivo():
   
  Contador = 0 # Determinar la cadena más larga a fin de delimitar el tamaño de la celda cambios.
  Encabezado = ["ID", "Cadena", "Cambio"]
  wb = xlsxwriter.Workbook("Resultados_" + obtenerFecha() + ".xlsx")
  Hoja = wb.add_worksheet()

  Estandar = wb.add_format();
  Rojo = wb.add_format({'color': 'red'}); #Colores especiales para resaltar los cambios

  # Escribir encabezados y centrarlos horizontalmente
  for i, encabezado in enumerate(Encabezado, start=1):
    
      Hoja.write(0, i - 1, encabezado)

  Centrar = wb.add_format({'align': 'center'})

  for i in range(len(Lista)):
      
      Cambios = convertir(Lista[i].items())
      Temporal = Caracteres.copy()  # Variable global para obtener la lista de caracteres.
      Claves = list(Lista[i].keys());
      Estilo = [];
      
      if len(Cambios) > Contador:
          Contador = len(Cambios)
      
      for clave, valor in Lista[i].items():
          Temporal[clave] = valor
      
      Auxiliar = ''.join(Temporal) #Unir todas las modificaciones en un string.

      for Indice, Elemento in  enumerate(Auxiliar):
         
         if Indice in Claves: # Agregar el caracter con formato rojo a la lista de elementos

          Estilo.append(Rojo);
          Estilo.append(Elemento);
      
         else:
            
            Estilo.append(Estandar);
            Estilo.append(Elemento);
      
      Hoja.write(i + 1, 0, i) #Escribir ID
      Hoja.write_rich_string(i + 1, 1, *Estilo);
      Hoja.write(i + 1, 2, Cambios) #Escribir Diccionario Cambios
      Estilo.clear();

  Hoja.set_column(1, 1, len(Cadena) * 1.15)
  Hoja.set_column(2, 2, Contador * 0.75)
  Hoja.set_column(0,0, len(str(len(Lista))) * 1.25, Centrar);
  Hoja.set_row(0, None, Centrar) 

  wb.close();  

def obtenerFecha():
   
  Fecha = datetime.now()

  # Obtener el año, mes, día, hora, minutos y segundos como cadenas de texto
  Anio = str(Fecha.year)
  Mes = str(Fecha.month).zfill(2)  # Asegura que el mes tenga 2 dígitos (rellenando con ceros si es necesario)
  Dia = str(Fecha.day).zfill(2)   # Asegura que el día tenga 2 dígitos (rellenando con ceros si es necesario)
  Hora = str(Fecha.hour).zfill(2) # Asegura que la hora tenga 2 dígitos (rellenando con ceros si es necesario)
  Minuto = str(Fecha.minute).zfill(2) # Asegura que los minutos tengan 2 dígitos (rellenando con ceros si es necesario)
  Segundo = str(Fecha.second).zfill(2) # Asegura que los segundos tengan 2 dígitos (rellenando con ceros si es necesario)

  # Concatenar el año, mes, día, hora, minutos y segundos y convertirlo a un número entero
  return Anio + Mes + Dia + Hora + Minuto + Segundo;

def convertir(Dato):

  Texto = "";

  for Clave, Valor in Dato:

    Texto += " {} : {} ,".format(Clave, Valor); 
    
  Texto = Texto[:-1]

  return Texto;
  
recorrido(Cadena, 10, 5, Indices);

compararLista(1, len(Lista));

imprimirArchivo();

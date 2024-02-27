import sys
import os
import pandas as pd
import xlsxwriter
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox, QVBoxLayout, QWidget, QTextEdit, QGroupBox
from PyQt5.QtGui import QFont

Indices = {}
Cadena = ""
Lista = []
Caracteres = []
Direccion = ""
Bandera = True;

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Actividad 04: Edición de cadenas de caracteres")
        self.setGeometry(400, 400, 700, 400)
        layout = QVBoxLayout()
        self.boton = QPushButton("Abrir CSV", self)
        self.boton.clicked.connect(self.abrir_csv)
        layout.addWidget(self.boton)
        
        self.nuevo_boton = QPushButton("Mostrar cambios", self)
        self.nuevo_boton.clicked.connect(self.funcion_nuevo_boton)
        layout.addWidget(self.nuevo_boton)
        
        self.group_box_cadena = QGroupBox("Cadena", self)
        self.group_layout_cadena = QVBoxLayout()
        self.text_edit_cadena = QTextEdit(self)
        self.text_edit_cadena.setReadOnly(True)
        font = QFont('Arial', 12)
        self.text_edit_cadena.setFont(font)
        self.group_layout_cadena.addWidget(self.text_edit_cadena)
        self.group_box_cadena.setLayout(self.group_layout_cadena)
        layout.addWidget(self.group_box_cadena)

        self.group_box_columna_0 = QGroupBox("Indices", self)
        self.group_layout_columna_0 = QVBoxLayout()
        self.text_edit_columna_0 = QTextEdit(self)
        self.text_edit_columna_0.setReadOnly(True)
        self.text_edit_columna_0.setFont(font)
        self.group_layout_columna_0.addWidget(self.text_edit_columna_0)
        self.group_box_columna_0.setLayout(self.group_layout_columna_0)
        layout.addWidget(self.group_box_columna_0)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setFont(QFont('Arial', 13))
        self.cadena = None
        self.datos_columna_0 = {}
        self.datos_columna_2 = {}

    def abrir_csv(self):
        global Indices
        global Cadena
        global Caracteres
        global Direccion
        
        opciones = QFileDialog.Options()
        nombre_archivo, _ = QFileDialog.getOpenFileName(self, "Abrir archivo CSV", "", "Archivos CSV (*.csv)", options=opciones)
        Direccion = os.path.dirname(nombre_archivo);        

        if nombre_archivo:
            try:
                df = pd.read_csv(nombre_archivo, dtype=str)
                
                fila = 0
                columna = 3
                cadena = df.iloc[fila, columna]
                self.text_edit_cadena.setPlainText(str(cadena))
                Cadena = cadena
                
                Caracteres = list(cadena)

                for index, valor in enumerate(df.iloc[0:, 0]):
                    if pd.notna(valor):
                        key = int(valor)
                        value = df.iloc[index, 2]
                        self.datos_columna_0[key] = value

                Indices = self.datos_columna_0
                self.mostrar_datos_en_qtextedit(self.text_edit_columna_0, self.datos_columna_0)

                QMessageBox.information(self, "Éxito", "Los datos han sido extraídos correctamente !!", QMessageBox.Ok)
                
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se han podido extraer los datos: {str(e)}", QMessageBox.Ok)

    def mostrar_datos_en_qtextedit(self, text_edit, datos):
        texto = ""
        for key, value in datos.items():
            texto += f"{key} : {value}\n"
        text_edit.setPlainText(texto)

    def obtener_datos_columna_0(self):
        return self.datos_columna_0

    def obtener_cadena(self):
        return self.cadena
    
    def funcion_nuevo_boton(self):
        Longitud = 10
        Recorrido = 5
        self.recorrido(Cadena, Longitud, Recorrido, Indices)
        self.compararLista(1, len(Lista)) # Modificar
        self.imprimirArchivo()

    def recorrido(self, Cadena, Longitud, Recorrido, Indices):
        Auxiliar = {}

        for i in range(0, len(Cadena), Recorrido):
            for j in range(i, i + Longitud, 1):
                if j in Indices:
                    Auxiliar[j] = Indices[j]

            if len(Auxiliar) > 0:
                self.permutacion(len(Auxiliar), Auxiliar)

            Auxiliar.clear()

    def permutacion(self, N, Diccionario): 
        Auxiliar = {}
        Indices = list(Diccionario.keys())

        for i in range(2**N):
            for j in range(N - 1, -1, -1):
                Posicion = (2**j)
                if i == 0:
                    continue

                Resultado = (i + Posicion) // Posicion
                Paridad = Resultado % 2

                if Paridad == 0:
                    Auxiliar.update({Indices[j]: Diccionario[Indices[j]]})

            if len(Auxiliar) > 0:
                self.unico(Auxiliar)

            Auxiliar.clear()

    def unico(self, Auxiliar):
        global Lista
        Unico = True

        for k in range(len(Lista)):
            if Lista[k] == Auxiliar:
                Unico = False
                continue

        if Unico:
            Temporal = Auxiliar.copy()
            Lista.append(Temporal)

    def compararLista(self, Inicio, Final):
        global Lista
        Auxiliar = {}
        Inicio -= 1

        for Inicio in range(Final):
            Auxiliar.update(Lista[Inicio])

        self.permutacion(len(Auxiliar), Auxiliar)

    def imprimirArchivo(self):
    
        global Direccion
        global Bandera;

        if(Bandera): #Crear Carpeta
            Direccion = os.path.join(Direccion, "Resultados");
            os.makedirs(Direccion, exist_ok=True)
            Bandera = False;

        Contador = 0 # Determinar la cadena más larga a fin de delimitar el tamaño de la celda cambios.
        Encabezado = ["ID", "Cadena", "Cambio"]
        wb = xlsxwriter.Workbook(Direccion + "/Resultados_" + self.obtenerFecha() + ".xlsx")
        Hoja = wb.add_worksheet()

        Estandar = wb.add_format();
        Rojo = wb.add_format({'color': 'red'}); #Colores especiales para resaltar los cambios

        # Escribir encabezados y centrarlos horizontalmente
        for i, encabezado in enumerate(Encabezado, start=1):
            
            Hoja.write(0, i - 1, encabezado)

        Centrar = wb.add_format({'align': 'center'})

        for i in range(len(Lista)):
            
            Cambios = self.convertir(Lista[i].items())
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


    def convertir(self, Dato):
        Texto = ""

        for Clave, Valor in Dato:
            Texto += " {} : {} ,".format(Clave, Valor)

        Texto = Texto[:-1]

        return Texto
    
    def obtenerFecha(self):
    
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())

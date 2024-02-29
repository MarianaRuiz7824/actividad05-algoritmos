import sys
import os
import pandas as pd
import xlsxwriter
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QGridLayout, QWidget, QTextEdit, QGroupBox, QLineEdit, QLabel, QInputDialog
from PyQt5.QtGui import QFont

Indices = {}
Cadena = ""
Lista = []
Caracteres = []
Bandera = True

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Actividad 04: Edición de cadenas de caracteres")
        self.setGeometry(500, 200, 1000, 300)
        layout = QGridLayout()
        
        self.group_box_cadena = QGroupBox("Cadena", self)
        self.group_layout_cadena = QVBoxLayout()
        self.text_edit_cadena = QTextEdit(self)
        self.text_edit_cadena.setReadOnly(True)
        font = QFont('Arial', 12)
        self.text_edit_cadena.setFont(font)
        self.group_layout_cadena.addWidget(self.text_edit_cadena)
        self.group_box_cadena.setLayout(self.group_layout_cadena)
        layout.addWidget(self.group_box_cadena, 0, 0, 1, 2)

        self.group_box_columna_0 = QGroupBox("Indices", self)
        self.group_layout_columna_0 = QVBoxLayout()
        self.text_edit_columna_0 = QTextEdit(self)
        self.text_edit_columna_0.setReadOnly(True)
        self.text_edit_columna_0.setFont(font)
        self.group_layout_columna_0.addWidget(self.text_edit_columna_0)
        self.group_box_columna_0.setLayout(self.group_layout_columna_0)
        layout.addWidget(self.group_box_columna_0, 0, 2, 1, 2)
        
        self.boton_abrir = QPushButton("Abrir CSV")
        self.boton_abrir.setFixedWidth(180)
        self.boton_abrir.clicked.connect(self.abrir_csv)
        layout.addWidget(self.boton_abrir, 1, 0)

        self.boton_nuevo = QPushButton("Comparación por Rangos")
        self.boton_nuevo.setFixedWidth(180)
        self.boton_nuevo.clicked.connect(self.mostrar_notificacion)
        layout.addWidget(self.boton_nuevo, 1, 2)
        
        self.boton_todos = QPushButton("Comparación final")
        self.boton_todos.setFixedWidth(180)
        self.boton_todos.clicked.connect(self.funcion_boton4)
        layout.addWidget(self.boton_todos, 1, 3)
        
        self.boton_libre = QPushButton("Recorrido")
        self.boton_libre.setFixedWidth(180)
        self.boton_libre.clicked.connect(self.funcion_recorrido)
        layout.addWidget(self.boton_libre, 1, 1)

        
        self.boton_imprimir = QPushButton("Imprimir Archivo")
        self.boton_imprimir.setFixedWidth(180)
        self.boton_imprimir.clicked.connect(self.funcion_nuevo_boton)
        layout.addWidget(self.boton_imprimir, 1, 4)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setFont(QFont('Arial', 13))
        self.Cadena = None
        self.Indices_columna_0 = {}

    def abrir_csv(self):
        global Indices
        global Cadena
        global Caracteres
        global Direccion
        
        opciones = QFileDialog.Options()
        nombre_archivo, _ = QFileDialog.getOpenFileName(self, "Abrir archivo CSV", "", "Archivos CSV (*.csv)", options=opciones)
        
        Direccion = os.path.dirname(nombre_archivo)
        
        if nombre_archivo:
            try:
                df = pd.read_csv(nombre_archivo, dtype=str)
                
                fila = 0
                columna = 3
                cadena = df.iloc[fila, columna]
                self.text_edit_cadena.setPlainText(str(cadena))
                self.Cadena = cadena
                
                Caracteres = list(cadena)

                for index, valor in enumerate(df.iloc[0:, 0]):
                    if pd.notna(valor):
                        key = int(valor)
                        value = df.iloc[index, 2]
                        self.Indices_columna_0[key] = value

                self.mostrar_datos_en_qtextedit(self.text_edit_columna_0, self.Indices_columna_0)

                QMessageBox.information(self, "Éxito", "Los datos han sido extraídos correctamente !!", QMessageBox.Ok)
                    
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se han podido extraer los datos: {str(e)}", QMessageBox.Ok)

    def mostrar_datos_en_qtextedit(self, text_edit, datos):
        texto = ""
        for key, value in datos.items():
            texto += f"{key} : {value}\n"
        text_edit.setPlainText(texto)

    def obtener_datos_columna_0(self):
        return self.Indices_columna_0

    def obtener_cadena(self):
        return self.Cadena
    
    def funcion_nuevo_boton(self):
        ruta_archivo = self.imprimirArchivo()  # Obtenemos la ruta del archivo
        mensaje = f"Se ha creado el archivo con éxito.\nRuta: {ruta_archivo}"
        
        # Mostrar notificación
        QMessageBox.information(self, "Éxito", mensaje, QMessageBox.Ok)

    def funcion_boton4(self):
        self.compararLista(1, len(Lista))
        
        QMessageBox.information(self, "Éxito", "Se ejecutó la comparación final.", QMessageBox.Ok)
        
    def funcion_recorrido(self):
        Longitud = 10
        Recorrido = 5
        self.recorrido(self.Cadena, Longitud, Recorrido, self.Indices_columna_0)
        QMessageBox.information(self, "Éxito", "Se ejecutó recorrido.", QMessageBox.Ok)



    def recorrido(self, cadena, Longitud, Recorrido, indices): 
        Auxiliar = {}

        for i in range(0, len(cadena), Recorrido):

            for j in range(i, i + Longitud, 1):

                if j in indices:
                    Auxiliar[j] = indices[j]

            if(len(Auxiliar) > 0): 
                self.permutacion(len(Auxiliar), Auxiliar)

            Auxiliar.clear()

    def permutacion(self, N, diccionario):
        Auxiliar = {}
        Indices = list(diccionario.keys())

        for i in range(2**N):

            for j in range(N -1, -1, -1):
                Posicion = (2**j)

            if(i == 0):
                continue

            Resultado = (i + Posicion) // Posicion
            Paridad = Resultado % 2

            if(Paridad == 0):
                Auxiliar.update({ Indices[j] : diccionario[Indices[j]]})

            if(len(Auxiliar) > 0):
                self.unico(Auxiliar)
            
            Auxiliar.clear()
            
    def unico(self, auxiliar):
        Unico = True

        for k in range(len(Lista)):
                
            if(Lista[k] == auxiliar):
                    
                Unico = False
                continue

        if(Unico):        

            Temporal = auxiliar.copy()
            Lista.append(Temporal)

    def compararLista(self, Inicio, Final):
        Auxiliar = {}
        Inicio -= 1

        for Inicio in range(Final):
            
            Auxiliar.update(Lista[Inicio])
        
        self.permutacion(len(Auxiliar), Auxiliar)

    def imprimirArchivo(self):
        global Direccion
        global Bandera
        
        if(Bandera):
            Direccion = os.path.join(Direccion, "Resultados")
            os.makedirs(Direccion, exist_ok=True)
            Bandera = False
        
        Contador = 0
        Encabezado = ["ID", "Cadena", "Cambio"]
        ruta_archivo = os.path.join(Direccion, "Resultados_" + self.obtenerFecha() + ".xlsx")
        wb = xlsxwriter.Workbook(ruta_archivo)
        Hoja = wb.add_worksheet()

        Estandar = wb.add_format()
        Rojo = wb.add_format({'color': 'red'})

        for i, encabezado in enumerate(Encabezado, start=1):
            Hoja.write(0, i - 1, encabezado)

        Centrar = wb.add_format({'align': 'center'})

        for i in range(len(Lista)):
            Cambios = self.convertir(Lista[i].items())
            Temporal = list(self.Cadena)  # Convertir la cadena en una lista para modificar caracteres individualmente
            Claves = list(Lista[i].keys())
            Estilo = []
            
            if len(Cambios) > Contador:
                Contador = len(Cambios)
            
            for clave, valor in Lista[i].items():
                Temporal[clave] = valor
            
            Auxiliar = ''.join(Temporal) # Convertir la lista modificada de nuevo a una cadena

            for Indice, Elemento in  enumerate(Auxiliar):
                
                if Indice in Claves:
                    Estilo.append(Rojo)
                    Estilo.append(Elemento)
            
                else:
                    Estilo.append(Estandar)
                    Estilo.append(Elemento)
            
            Hoja.write(i + 1, 0, i)
            Hoja.write_rich_string(i + 1, 1, *Estilo)
            Hoja.write(i + 1, 2, Cambios)
            Estilo.clear()

        Hoja.set_column(1, 1, len(self.Cadena) * 1.15)
        Hoja.set_column(2, 2, Contador * 0.75)
        Hoja.set_column(0, 0, len(str(len(Lista))) * 1.25, Centrar)
        Hoja.set_row(0, None, Centrar) 

        wb.close()
        
        return ruta_archivo
        
    def obtenerFecha(self):
        Fecha = datetime.now()

        Anio = str(Fecha.year)
        Mes = str(Fecha.month).zfill(2)
        Dia = str(Fecha.day).zfill(2)
        Hora = str(Fecha.hour).zfill(2)
        Minuto = str(Fecha.minute).zfill(2)
        Segundo = str(Fecha.second).zfill(2)

        return Anio + Mes + Dia + Hora + Minuto + Segundo


    def convertir(self, Dato):
        Texto = ""

        for Clave, Valor in Dato:
            Texto += " {} : {} ,".format(Clave, Valor)

        Texto = Texto[:-1]

        return Texto

    def mostrar_notificacion(self):
        global Lista
        Longitud = 10
        Recorrido = 5
        
        self.recorrido(self.Cadena, Longitud, Recorrido, self.Indices_columna_0)
        mensaje = f"Tienes {len(Lista)} listas disponibles para elegir.\nIngrese 2 valores:"
        
        QMessageBox.information(self, "Notificación", mensaje, QMessageBox.Ok)
        
        valor1, ok1 = QInputDialog.getInt(self, 'Ingrese el primer valor', 'Valor 1:')
        valor2, ok2 = QInputDialog.getInt(self, 'Ingrese el segundo valor', 'Valor 2:')
        
        global ValorGlobal1
        global ValorGlobal2
        ValorGlobal1 = valor1
        ValorGlobal2 = valor2

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())

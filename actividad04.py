import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox, QVBoxLayout, QWidget, QTextEdit, QGroupBox
from PyQt5.QtGui import QFont

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Actividad 04: Edición de cadenas de caracteres")
        self.setGeometry(400, 400, 700, 400)
        layout = QVBoxLayout()
        self.boton = QPushButton("Abrir CSV", self)
        self.boton.clicked.connect(self.abrir_csv)
        layout.addWidget(self.boton)
        
        self.nuevo_boton = QPushButton("Nuevo Botón", self) # No sé qué nombre quieres que le pongamos al botón
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
        opciones = QFileDialog.Options()
        nombre_archivo, _ = QFileDialog.getOpenFileName(self, "Abrir archivo CSV", "", "Archivos CSV (*.csv)", options=opciones)
        if nombre_archivo:
            try:
                df = pd.read_csv(nombre_archivo, dtype=str)
                
                fila = 0
                columna = 3
                cadena = df.iloc[fila, columna]
                self.text_edit_cadena.setPlainText(str(cadena))
                
                for index, valor in enumerate(df.iloc[0:, 0]):
                    if pd.notna(valor):
                        key = int(valor)
                        value = df.iloc[index, 2]
                        self.datos_columna_0[key] = value

                self.mostrar_datos_en_qtextedit(self.text_edit_columna_0, self.datos_columna_0)

                QMessageBox.information(self, "Éxito", "Los datos han sido extraídos correctamente !!", QMessageBox.Ok)

                print("Datos de los índices de la columna 0:")
                for key, value in self.datos_columna_0.items():
                    print(f"{key}: {value}")
                    
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
        # Aquí agrega la función del botón :)
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())

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
        self.boton = QPushButton("abrir csv", self)
        self.boton.clicked.connect(self.abrir_csv)
        layout.addWidget(self.boton)
        
        # Crear un grupo para el QTextEdit
        self.group_box = QGroupBox("Cadena de caracteres", self)
        self.group_layout = QVBoxLayout()
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        font = QFont('Arial', 12)
        self.text_edit.setFont(font)
        self.group_layout.addWidget(self.text_edit)
        self.group_box.setLayout(self.group_layout)
        layout.addWidget(self.group_box)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setFont(QFont('Arial', 13))

    def abrir_csv(self):
        opciones = QFileDialog.Options()
        nombre_archivo, _ = QFileDialog.getOpenFileName(self, "Abrir archivo CSV", "", "Archivos CSV (*.csv)", options=opciones)
        if nombre_archivo:
            try:
                df = pd.read_csv(nombre_archivo, dtype=str)
                fila = 0
                columna = 3
                cadena = df.iloc[fila, columna]
                self.text_edit.setPlainText(str(cadena))
                QMessageBox.information(self, "Éxito", "La cadena de caracteres ha sido extraída correctamente !!", QMessageBox.Ok)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se ha podido extraer la cadena de caracteres: {str(e)}", QMessageBox.Ok)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())

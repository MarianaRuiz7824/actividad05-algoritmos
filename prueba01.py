import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox, QVBoxLayout, QWidget, QTextEdit

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Actividad 04 de Python con Pyqt")
        self.setGeometry(400, 400, 800, 600)
        layout = QVBoxLayout()
        self.boton = QPushButton("Abrir CSV", self)
        self.boton.clicked.connect(self.abrir_csv)
        layout.addWidget(self.boton)
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def abrir_csv(self):
        opciones = QFileDialog.Options()
        nombre_archivo, _ = QFileDialog.getOpenFileName(self, "Abrir archivo CSV", "", "Archivos CSV (*.csv)", options=opciones)
        if nombre_archivo:
            try:
                df = pd.read_csv(nombre_archivo)
                # Supongamos que deseas extraer la cadena de la celda en la fila 2 y la columna 3
                fila = 1  # La indexación comienza desde 0
                columna = 2
                cadena = df.iloc[fila, columna]
                matriz = [list(fila) for fila in cadena.split('\n')]
                self.text_edit.setPlainText(str(matriz))
                QMessageBox.information(self, "Éxito", "Cadena de caracteres extraída correctamente", QMessageBox.Ok)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo extraer la cadena de caracteres: {str(e)}", QMessageBox.Ok)

def Recorrido(Lista, Longitud, tasaRecorrido):

  Auxiliar = [];

  for i in range(Longitud, tasaRecorrido, len(Lista)):

    Cadena = "";

    for j in range(i, tasaRecorrido, Longitud):

      Cadena += Lista[j]

    Auxiliar.append(Cadena);

  return Auxiliar;


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())

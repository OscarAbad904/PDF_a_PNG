import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6 import uic
import fitz  # PyMuPDF

class PDFtoImagesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        directorio_base = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(f"{directorio_base}/PDF_a_PNG.ui", self)

        self.btnSeleccionarPDF.clicked.connect(self.seleccionar_pdf)
        self.btnSeleccionarCarpeta.clicked.connect(self.seleccionar_carpeta)
        self.btnProcesar.clicked.connect(self.procesar_pdf)

    def seleccionar_pdf(self):
        print("Botón 'Seleccionar PDF' presionado")  # Mensaje de depuración
        ruta_pdf, _ = QFileDialog.getOpenFileName(self, "Seleccionar PDF", "", "Archivos PDF (*.pdf)")
        if ruta_pdf:
            self.leRutaPDF.setText(ruta_pdf)
            # Establecer la carpeta de salida automáticamente
            carpeta_predeterminada = os.path.dirname(ruta_pdf)
            self.leRutaCarpeta.setText(carpeta_predeterminada)

    def seleccionar_carpeta(self):
        print("Botón 'Seleccionar Carpeta' presionado")  # Mensaje de depuración
        carpeta = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de salida")
        if carpeta:
            self.leRutaCarpeta.setText(carpeta)

    def procesar_pdf(self):
        print("Botón 'Procesar' presionado")  # Mensaje de depuración
        ruta_pdf = self.leRutaPDF.text()
        carpeta_salida = self.leRutaCarpeta.text()

        if not ruta_pdf or not carpeta_salida:
            print("Error: Ruta PDF o carpeta de salida no especificada")  # Mensaje de error
            return

        # Abrimos el PDF con fitz (PyMuPDF)
        doc = fitz.open(ruta_pdf)
        # Eliminamos la extensión ".pdf" del nombre
        nombre_pdf = ruta_pdf.split("/")[-1].rsplit(".pdf", 1)[0]

        # Crear una carpeta con el nombre del archivo PDF en la ruta de salida
        carpeta_destino = os.path.join(carpeta_salida, nombre_pdf)
        os.makedirs(carpeta_destino, exist_ok=True)

        # Recorremos todas las páginas
        total_paginas = len(doc)
        for i, pagina in enumerate(doc, start=1):
            # Obtenemos el Pixmap de la página (renderizado en memoria)
            pix = pagina.get_pixmap()
            # Construimos la ruta de salida dentro de la nueva carpeta
            ruta_imagen = os.path.join(carpeta_destino, f"{nombre_pdf}_pagina_{i}.png")
            # Guardamos la imagen
            pix.save(ruta_imagen)

        doc.close()

        # Mostrar cuadro de diálogo con el número de páginas procesadas
        QMessageBox.information(self, "Proceso completado", f"Se han procesado {total_paginas} páginas de {total_paginas} páginas.")

def main():
    app = QApplication(sys.argv)
    ventana = PDFtoImagesApp()
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

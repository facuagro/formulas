import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QPushButton, QLabel, 
    QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit, QInputDialog
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QDir, QDateTime
from fpdf import FPDF

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gestión de Fórmulas')
        self.setGeometry(100, 100, 800, 600)
        
        # Set the window icon
        self.setWindowIcon(QIcon('logo.png'))  # Assuming the logo file is in the same directory as main.py
        
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create a container widget for the logo and title
        header_widget = QWidget()
        header_layout = QVBoxLayout()
        
        # Load and resize the logo
        logo_pixmap = QPixmap('logo.png')
        logo_pixmap = logo_pixmap.scaled(200, 200, Qt.KeepAspectRatio)  # Adjust size as needed
        logo_label = QLabel()
        logo_label.setPixmap(logo_pixmap)
        
        # Add the logo and title to the header layout
        title_label = QLabel('Gestión de Fórmulas')
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        
        header_layout.addWidget(logo_label, alignment=Qt.AlignCenter)
        header_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        header_widget.setLayout(header_layout)
        
        layout.addWidget(header_widget)

        self.comboBox = QComboBox()
        self.loadButton = QPushButton('Cargar Fórmulas')
        self.saveButton = QPushButton('Guardar Cantidades')
        self.exportButton = QPushButton('Exportar a PDF')
        self.tableWidget = QTableWidget()
        self.dateTimeLabel = QLabel()  # Label para mostrar fecha y hora

        self.loadButton.clicked.connect(self.loadFormulas)
        self.saveButton.clicked.connect(self.saveQuantities)
        self.exportButton.clicked.connect(self.exportToPDF)
        self.comboBox.currentIndexChanged.connect(self.displayFormula)

        layout.addWidget(QLabel('Selecciona una fórmula:'))
        layout.addWidget(self.comboBox)
        layout.addWidget(self.loadButton)
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.saveButton)
        layout.addWidget(self.exportButton)
        layout.addWidget(self.dateTimeLabel)  # Añadir label al layout

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.formulas = {}
        self.current_formula = None

        # Actualiza la fecha y hora cada vez que se carga la aplicación
        self.updateDateTime()

    def updateDateTime(self):
        current_date_time = QDateTime.currentDateTime().toString("dd/MM/yyyy hh:mm:ss")
        self.dateTimeLabel.setText(f"Fecha y Hora: {current_date_time}")

    def loadFormulas(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilters(["Excel files (*.xlsx)"])
        file_dialog.setFilter(QDir.Files)
        file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            self.formulas = {}
            for path in file_paths:
                try:
                    df = pd.read_excel(path)
                    print(f"Datos de {path}:")
                    print(df.head())  # Imprime las primeras filas del DataFrame
                    self.formulas[path] = df
                except Exception as e:
                    print(f"Error al leer {path}: {e}")
            self.populateComboBox()

    def populateComboBox(self):
        self.comboBox.clear()
        self.comboBox.addItems([os.path.basename(f) for f in self.formulas.keys()])

    def clearTable(self):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)

    def displayFormula(self):
        self.clearTable()  # Limpia la tabla antes de cargar una nueva fórmula

        if self.comboBox.currentText():
            file_path = [k for k in self.formulas.keys() if os.path.basename(k) == self.comboBox.currentText()][0]
            df = self.formulas[file_path]
            print(f"Mostrando fórmula desde: {file_path}")
            print(df)  # Imprime todo el DataFrame para ver qué datos se están cargando
            if df is not None and not df.empty:
                self.tableWidget.setRowCount(len(df))
                self.tableWidget.setColumnCount(len(df.columns))
                self.tableWidget.setHorizontalHeaderLabels(df.columns)

                for i, row in df.iterrows():
                    for j, value in enumerate(row):
                        print(f"Estableciendo valor en ({i}, j): {value}")  # Depura el valor que se está estableciendo
                        item = QTableWidgetItem(str(value))
                        if j == df.columns.get_loc('Cantidad Utilizada') or j == df.columns.get_loc('LOTE'):  
                            item.setFlags(item.flags() | Qt.ItemIsEditable)
                        else:
                            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # No editable
                        self.tableWidget.setItem(i, j, item)
            
            # Actualiza la fecha y hora al cargar una nueva fórmula
            self.updateDateTime()

    def saveQuantities(self):
        if self.comboBox.currentText():
            file_path = [k for k in self.formulas.keys() if os.path.basename(k) == self.comboBox.currentText()][0]
            df = self.formulas[file_path]
            for i in range(self.tableWidget.rowCount()):
                for j in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(i, j)
                    if item is not None:
                        df.iloc[i, j] = item.text()
            df.to_excel(file_path, index=False)
            print(f"Datos guardados en {file_path}")

    def exportToPDF(self):
        if self.comboBox.currentText():
            operario, ok = QInputDialog.getText(self, 'Nombre del Operario', 'Ingrese el nombre del operario:')
            if ok and operario:
                file_path = [k for k in self.formulas.keys() if os.path.basename(k) == self.comboBox.currentText()][0]
                df = self.formulas[file_path]

                pdf = FPDF(orientation='L', unit='mm', format='A4')  # Orientación horizontal
                pdf.add_page()

                # Añadir el logo en la parte superior izquierda
                pdf.image('logo.png', 10, 8, 33)

                # Añadir título y fecha
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(0, 10, f'Fórmula: {os.path.basename(file_path)}', 0, 1, 'C')
                pdf.cell(0, 10, f'Operario: {operario}', 0, 1, 'C')
                pdf.cell(0, 10, f'Fecha y Hora: {self.dateTimeLabel.text()}', 0, 1, 'C')
                pdf.ln(10)

                # Añadir tabla con datos
                pdf.set_font('Arial', '', 10)
                col_width = pdf.w / (len(df.columns) + 1)
                for i, row in df.iterrows():
                    for item in row:
                        pdf.cell(col_width, 10, str(item), border=1)
                    pdf.ln()

                # Guardar PDF con la hora en el nombre del archivo
                current_time = QDateTime.currentDateTime().toString("yyyyMMdd_hhmmss")
                pdf_output_path = os.path.splitext(file_path)[0] + f'_{current_time}.pdf'
                pdf.output(pdf_output_path)

                # Mostrar cuadro de diálogo con la ruta del archivo PDF guardado
                QMessageBox.information(self, 'PDF Guardado', f'El PDF ha sido guardado en:\n{pdf_output_path}')


    def closeEvent(self, event):
        password, ok = QInputDialog.getText(self, 'Contraseña Requerida', 'Ingrese la contraseña para cerrar:', QLineEdit.Password)
        if ok and password == 'clave_segura':
            event.accept()
        else:
            QMessageBox.warning(self, 'Contraseña Incorrecta', 'La contraseña ingresada es incorrecta.')
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

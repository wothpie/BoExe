import os
import sys
import subprocess
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QSplashScreen
from PyQt5.QtCore import Qt

class SplashScreen(QSplashScreen):
    def __init__(self, splash_pixmap):
        super().__init__(splash_pixmap)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setEnabled(False)

class ExeConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Bo Exe Çevirici")
        self.setGeometry(300, 300, 400, 200)
        self.setWindowIcon(QIcon('../bo.ico'))
        self.setStyleSheet("""
            QSplashScreen {
                background-color: #2c3e50; /* Arka plan rengi */
            }

            #splash_label {
                color: #ecf0f1; /* Metin rengi */
                font-size: 18px;
            }
        """)
        self.splash_pix = QPixmap("loading.png")
        self.splash = SplashScreen(self.splash_pix)
        self.splash.show()

        self.splash.showMessage("Yükleniyor...", Qt.AlignBottom | Qt.AlignRight, Qt.black)
        # PyInstaller'ı güncelle ve hataları kontrol et
        self.update_pyinstaller()
        QApplication.processEvents()

        # Yüklenme ekranını kapat
        self.splash.finish(self)

        self.label = QLabel("Python Dosyasını Seç:")
        self.browse_button = QPushButton("Dosya Seç", self)
        self.browse_button.clicked.connect(self.browse_file)

        self.icon_label = QLabel("Icon Dosyasını Seç (isteğe bağlı):")
        self.icon_button = QPushButton("Icon Seç", self)
        self.icon_button.clicked.connect(self.browse_icon)




        self.convert_button = QPushButton("Dönüştür", self)
        self.convert_button.clicked.connect(self.convert_to_exe)

        self.selected_file = ""
        self.selected_icon = ""
        self.selected_side_files = ""
        self.output_path = ""

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.icon_label)
        layout.addWidget(self.icon_button)
        layout.addWidget(self.convert_button)

        self.setLayout(layout)

        # Fusion stilini uygula
        self.setStyle(QApplication.setStyle("Fusion"))

        # Stil ayarları
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f8f8;
            }

            QLabel {
                color: #333333;
                font-size: 14px;
            }

            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
            }

            QPushButton:hover {
                background-color: #2980b9;
            }

            QPushButton:pressed {
                background-color: #21618c;
            }
        """)

    def browse_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.selected_file, _ = QFileDialog.getOpenFileName(self, "Python Dosyasını Seç", "", "Python Dosyaları (*.py);;All Files (*)", options=options)
        self.label.setText(f"Seçilen Dosya: {self.selected_file}")

    def browse_icon(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.selected_icon, _ = QFileDialog.getOpenFileName(self, "Icon Dosyasını Seç (isteğe bağlı)", "", "ICO Dosyaları (*.ico);;All Files (*)", options=options)
        self.icon_label.setText(f"Seçilen Icon: {self.selected_icon}")



    def browse_output_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.output_path = QFileDialog.getExistingDirectory(self, "Dönüştürülen .exe Dosyasını Kaydet", "")
        if self.output_path:
            print(f"Seçilen Çıkış Dizini: {self.output_path}")

    def convert_to_exe(self):
        if not self.selected_file:
            print("Lütfen bir dosya seçin.")
            return

        if not self.selected_file.endswith(".py"):
            print("Lütfen geçerli bir Python dosyası seçin.")
            return

        # Prompt user to select output directory
        self.browse_output_path()

        if not self.output_path:
            print("Lütfen bir çıkış dizini seçin.")
            return

        exe_name = os.path.splitext(os.path.basename(self.selected_file))[0] + ".exe"
        options = f"--icon={self.selected_icon}" if self.selected_icon else ""
        side_files = " ".join(self.selected_side_files)

        self.splash_pix = QPixmap("loading.png")
        self.splash = SplashScreen(self.splash_pix)
        self.splash.show()

        self.splash.showMessage("Dönüştürülüyor...", Qt.AlignBottom | Qt.AlignRight, Qt.black)

        command = [
            "pyinstaller",
            "--onefile",
            "--noconsole",
            options,
            "--distpath",
            self.output_path.replace("/", "\\"),
            self.selected_file.replace("/", "\\")
        ]

        subprocess.run(command)

        print(
            f"{self.selected_file} dosyası {exe_name} adlı .exe dosyasına dönüştürüldü ve {self.output_path} konumuna kaydedildi.")
        QApplication.processEvents()
        # Yüklenme ekranını kapat
        self.splash.finish(self)

    def update_pyinstaller(self):
        print("PyInstaller güncelleniyor...")
        command = ["pip", "install", "--upgrade", "pyinstaller"]
        subprocess.run(command)
        print("PyInstaller güncelleme tamamlandı.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ExeConverter()
    ex.show()
    sys.exit(app.exec_())

import sys
import requests
import zipfile
import os
import io
from packaging import version
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QTextEdit, QVBoxLayout, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

MEVCUT_SURUM = "1.0.0"
GUNCELLEME_URL = "https://raw.githubusercontent.com/yamann0101/sur-bey-updates/main/version.txt"
GUNCELLEME_DOSYA_URL = "https://github.com/yamann0101/sur-bey-updates/raw/main/update.zip"

class CustomWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SUR'BEY - Masaüstü Uygulama")
        self.setGeometry(400, 100, 700, 500)
        self.setStyleSheet("background-color: black; color: white;")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("SUR'BEY")
        self.label.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: orange;")
        layout.addWidget(self.label)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("background-color: #222; color: #0f0; font-family: Consolas;")
        layout.addWidget(self.log_output)

        self.check_button = QPushButton("Güncellemeleri Kontrol Et ve Yükle")
        self.check_button.setStyleSheet("""
            QPushButton {
                background-color: orange;
                color: black;
                font-size: 18px;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #ffaa00;
            }
        """)
        self.check_button.clicked.connect(self.kontrol_ve_guncelle)
        layout.addWidget(self.check_button)

    def kontrol_ve_guncelle(self):
        try:
            self.log_output.append("Güncelleme kontrol ediliyor...")
            response = requests.get(GUNCELLEME_URL, timeout=5)
            if response.status_code == 200:
                guncel_surum = response.text.strip()
                self.log_output.append(f"Güncel sürüm: {guncel_surum}")
                if version.parse(guncel_surum) > version.parse(MEVCUT_SURUM):
                    self.log_output.append("Yeni sürüm bulundu. İndiriliyor...")
                    self.indir_ve_yukle()
                else:
                    QMessageBox.information(self, "Güncel", "Uygulamanız güncel.")
            else:
                self.log_output.append("Güncelleme dosyasına erişilemedi.")
        except Exception as e:
            self.log_output.append(f"Hata oluştu: {e}")

    def indir_ve_yukle(self):
        try:
            response = requests.get(GUNCELLEME_DOSYA_URL, timeout=20)
            if response.status_code == 200:
                self.log_output.append("Güncelleme dosyası indirildi. Açılıyor...")
                with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                    zip_ref.extractall(".")  # Şu anki klasöre açıyor (değiştirilebilir)
                self.log_output.append("Güncelleme tamamlandı. Lütfen uygulamayı yeniden başlatın.")
                QMessageBox.information(self, "Güncelleme Tamamlandı", "Güncelleme tamamlandı. Uygulamayı yeniden başlatın.")
            else:
                self.log_output.append("Güncelleme dosyası indirilemedi.")
        except Exception as e:
            self.log_output.append(f"Güncelleme indirirken hata: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomWindow()
    window.show()
    sys.exit(app.exec())

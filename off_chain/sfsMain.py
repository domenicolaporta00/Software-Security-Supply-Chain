import sys
import time
import os

# Aggiungi la directory principale al PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen

from view.vista_accedi import VistaAccedi
# Prova
if __name__ == "__main__":
    app = QApplication(sys.argv)

    splash_image_path = os.path.join(current_dir, "images", "logo_splash.png")
    splash = QSplashScreen(QPixmap(splash_image_path), Qt.WindowStaysOnTopHint)
    splash.show()
    time.sleep(1)
    finestra = VistaAccedi()
    finestra.show()
    splash.finish(finestra)
    sys.exit(app.exec())

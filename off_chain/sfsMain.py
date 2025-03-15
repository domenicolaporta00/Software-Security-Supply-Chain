import sys
import time
import os
import traceback

# Aggiungi la directory principale al PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen, QMessageBox

from view.vista_accedi import VistaAccedi

if __name__ == "__main__":
    try:
        print("Inizializzazione dell'applicazione...")
        app = QApplication(sys.argv)
        
        print("Caricamento dello splash screen...")
        splash_image_path = os.path.join(current_dir, "images", "logo_splash.png")
        print(f"Percorso immagine splash: {splash_image_path}")
        
        if not os.path.exists(splash_image_path):
            print(f"ERRORE: Immagine splash non trovata in: {splash_image_path}")
            raise FileNotFoundError(f"Immagine splash non trovata: {splash_image_path}")
            
        splash_pixmap = QPixmap(splash_image_path)
        if splash_pixmap.isNull():
            print("ERRORE: Impossibile caricare l'immagine splash")
            raise Exception("Impossibile caricare l'immagine splash")
            
        splash = QSplashScreen(splash_pixmap, Qt.WindowStaysOnTopHint)
        splash.show()
        app.processEvents()  # Forza l'aggiornamento dell'interfaccia
        
        print("Attesa di 1 secondo...")
        time.sleep(1)
        
        print("Creazione della finestra principale...")
        finestra = VistaAccedi()
        finestra.show()
        app.processEvents()  # Forza l'aggiornamento dell'interfaccia
        
        print("Chiusura dello splash screen...")
        splash.finish(finestra)
        
        print("Avvio del loop principale...")
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"ERRORE CRITICO: {str(e)}")
        print("Traceback completo:")
        traceback.print_exc()
        
        # Se l'applicazione Qt è già inizializzata, mostra un messaggio di errore grafico
        if 'app' in locals():
            QMessageBox.critical(None, "Errore", f"Si è verificato un errore critico:\n{str(e)}")
        sys.exit(1)

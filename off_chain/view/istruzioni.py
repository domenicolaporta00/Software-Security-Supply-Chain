from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QScrollArea, QMessageBox
)

from off_chain.view import funzioni_utili


class Istruzioni(QMainWindow):
    closed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.testo_istruzioni = None
        self.setWindowTitle('SupplyChain')
        self.setGeometry(0, 0, 750, 650)  # Dimensioni fisse
        self.setFixedSize(750, 650)  # Blocca il ridimensionamento

        self.setWindowIcon(QIcon("images\\logo_centro.png"))

        funzioni_utili.center(self)

        self.init_ui()

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()

    def init_ui(self):
        # Crea il widget centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principale
        outer_layout = QVBoxLayout(central_widget)

        # Crea un'area scrollabile
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Permette di adattarsi al contenuto
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Widget contenitore del testo
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(10, 10, 10, 10)  # Margini ridotti

        # Testo delle istruzioni formattato come elenco puntato
        testo = """
        • Ciclo di vita di un prodotto (materia prima):
          ◦ prodotto da un'azienda agricola;
          ◦ trasportato da un'azienda di trasporto (azienda agricola -> azienda di trasformazione);
          ◦ trasformato da un'azienda di trasformazione;
          ◦ utilizzato nella produzione di un prodotto finale da un'azienda di trasformazione.
          
        • Ciclo di vita alternativo di un prodotto (materia prima):
          ◦ prodotto da un'azienda agricola;
          ◦ trasportato da un'azienda di trasporto (azienda agricola -> rivenditore);
          ◦ messo sugli scaffali da un rivenditore.
          
        • Ciclo di vita di un prodotto (finale):
          ◦ prodotto da un'azienda di trasformazione (necessario specificare le materie prime utilizzate);
          ◦ trasportato da un'azienda di trasformazione (azienda di trasformazione -> rivenditore);
          ◦ messo sugli scaffali da un rivenditore.
        
        • Ogni azienda agricola può effettuare soltanto operazioni di produzione su prodotti 
          (materie prime) già istanziati nel database. In fase di creazione di ogni operazione 
          bisogna selezionare l'azienda di trasporto a cui destinare il prodotto selezionato.

        • Ogni azienda di trasporto può effettuare soltanto operazioni di trasporto sui prodotti 
          che una qualsiasi azienda agricola/di trasformazione ha prodotto per essa. 
          Ogni prodotto può essere trasportato una sola volta. In fase di creazione di ogni 
          operazione bisogna selezionare l'azienda di trasformazione/rivenditore a cui 
          destinare il prodotto selezionato.

        • Ogni azienda di trasformazione può effettuare operazioni di trasformazione oppure 
          di produzione.
          ◦ Trasformazione: ogni azienda può trasformare soltanto prodotti che sono stati destinati 
            ad essa da una qualsiasi azienda di trasporto. Ogni prodotto può essere trasformato 
            una sola volta.
          ◦ Produzione: ogni azienda può produrre soltanto prodotti (finali) già istanziati nel 
            database; in fase di produzione è necessario selezionare, tra i prodotti che l'azienda 
            autenticata ha trasformato, le materie prime con cui il bene finale viene prodotto 
            (esempio: succo ACE prodotto con arance e carote). Bisogna infine selezionare 
            l'azienda di trasporto a cui destinare il prodotto finale.

        • Ogni rivenditore può effettuare soltanto operazioni di messa sugli scaffali sui prodotti 
          che una qualsiasi azienda di trasporto ha destinato ad essa. Ogni prodotto può essere 
          messo sugli scaffali una sola volta.

        • Ogni azienda di certificazione può certificare tutti i prodotti che sono stati messi 
          sugli scaffali da un qualsiasi rivenditore. Ogni prodotto può essere certificato una 
          sola volta.

        • Ogni guest può visualizzare tutti i prodotti che sono stati messi sugli scaffali da un 
          qualsiasi rivenditore.
        
        """

        # Crea e configura il QLabel
        self.testo_istruzioni = QLabel(testo)
        self.testo_istruzioni.setFont(QFont("Times Roman", 11))
        self.testo_istruzioni.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # Allinea in alto a sinistra
        self.testo_istruzioni.setWordWrap(True)  # Permette il ritorno a capo automatico

        # Aggiunge il QLabel al layout interno dello scroll
        scroll_layout.addWidget(self.testo_istruzioni)
        scroll_widget.setLayout(scroll_layout)

        # Imposta il widget contenitore nel QScrollArea
        scroll_area.setWidget(scroll_widget)

        # Aggiunge lo scroll_area al layout principale
        outer_layout.addWidget(scroll_area)

from PyQt5.QtCore import Qt, QTimer, QEvent
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QMessageBox

from off_chain.controllers.controller_certificatore import ControllerCertificatore
from off_chain.view import funzioni_utili
from off_chain.view.istruzioni import Istruzioni
from off_chain.view.vista_stato_azienda import VistaStatoAzienda
from off_chain.view.vista_prodotti import VistaProdotti
from off_chain.view.vista_soglie import VistaSoglie
from off_chain.view.vista_sviluppatori import VistaSviluppatori


class HomePageCertificatore(QMainWindow):
    def __init__(self, callback, utente):
        super().__init__()

        self.controller = ControllerCertificatore()

        self.vista_soglie = None
        self.vista_sviluppatori = None
        self.vista_azienda = None
        self.vista_certificazioni = None
        self.vista_istruzioni = None
        self.utente = utente

        self.menu_bar = self.menuBar()
        self.menu_bar.setStyleSheet("background-color: rgb(240, 240, 240)")
        funzioni_utili.config_menubar(
            self, "File", QIcon("images\\exit.png"),
            "Logout", 'Ctrl+Q', self.menu_bar
        ).triggered.connect(self.logout)
        funzioni_utili.config_menubar(
            self, "Termini e condizioni d'uso", QIcon("images\\tcu.png"),
            "Leggi i termini e le condizioni d'uso", 'Ctrl+W', self.menu_bar
        ).triggered.connect(self.tcu)
        funzioni_utili.config_menubar(
            self, "FAQ", QIcon("images\\faq.png"),
            "Visualizza le domande più frequenti", 'Ctrl+E', self.menu_bar
        ).triggered.connect(self.faq)
        funzioni_utili.config_menubar(
            self, "Tutorial", QIcon("images\\tutorial.png"),
            "Visualizza tutorial", 'Ctrl+E', self.menu_bar
        ).triggered.connect(self.tutorial)

        self.setWindowIcon(QIcon("images\\logo_centro.png"))

        self.callback = callback

        # Elementi di layout
        self.logo = QLabel()
        self.welcome_label = QLabel(f"Ciao {self.utente[3]} 👋!\nBenvenuto in SupplyChain.\n"
                                    f"Prego selezionare un'opzione dal menu")
        self.button_certificazione = QPushButton('Certificazioni')
        self.button_aziende = QPushButton('Stato azienda')
        self.button_soglie = QPushButton('Soglie')
        self.button_sviluppatori = QPushButton('Sviluppatori')

        # Inizializza il timer di inattività
        self.inactivity_timer = QTimer(self)
        self.inactivity_timer.setInterval(funzioni_utili.timeout())
        self.inactivity_timer.timeout.connect(self.logout_per_inattivita)

        self.init_ui()
        self.start_inactivity_timer()
        self.installEventFilter(self)  # Intercetta eventi utente

    def start_inactivity_timer(self):
        """Avvia o resetta il timer di inattività."""
        self.inactivity_timer.start()

    def logout_per_inattivita(self):
        """Chiude la finestra se l'utente è inattivo per troppo tempo."""
        self.inactivity_timer.stop()
        reply = QMessageBox.warning(
            self,
            "Sessione scaduta",
            "Sei stato inattivo per troppo tempo. Verrai disconnesso.",
            QMessageBox.Ok
        )
        if reply == QMessageBox.Ok:
            self.close()
            self.callback()  # Torna alla schermata di login

    def eventFilter(self, obj, event):
        """Intercetta gli eventi dell'utente e resetta il timer."""
        if event.type() in (QEvent.MouseMove, QEvent.KeyPress):
            self.start_inactivity_timer()  # Reset del timer
        return super().eventFilter(obj, event)

    def init_ui(self):
        self.setWindowTitle('SupplyChain')
        self.setGeometry(0, 0, 750, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        outer_layout = QVBoxLayout(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(50)
        main_layout.setAlignment(Qt.AlignCenter)

        funzioni_utili.insert_label(self.welcome_label, main_layout)

        button_layout = QGridLayout()
        button_layout.setSpacing(1)

        funzioni_utili.insert_button_in_grid(self.button_certificazione, button_layout, 1, 2)
        self.button_certificazione.clicked.connect(self.show_certificazioni)

        funzioni_utili.insert_button_in_grid(self.button_aziende, button_layout, 1, 4)
        self.button_aziende.clicked.connect(self.show_azienda)

        funzioni_utili.insert_button_in_grid(self.button_soglie, button_layout, 5, 2)
        self.button_soglie.clicked.connect(self.show_soglie)

        funzioni_utili.insert_button_in_grid(self.button_sviluppatori, button_layout, 5, 4)
        self.button_sviluppatori.clicked.connect(self.show_sviluppatori)

        funzioni_utili.insert_logo(self.logo, button_layout, QPixmap("images\\logo_centro.png"))

        main_layout.addLayout(button_layout)

        outer_layout.addLayout(main_layout)

        funzioni_utili.center(self)

    def logout(self):
        self.inactivity_timer.stop()
        # Mostra una finestra di conferma
        reply = QMessageBox.question(
            self,
            "Conferma logout",
            "Sei sicuro di voler effettuare il logout?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        # Procede solo se l'utente clicca "Yes"
        if reply == QMessageBox.Yes:
            self.close()
            self.callback()

    def mostra(self):
        self.start_inactivity_timer()
        self.show()

    def tutorial(self):
        QMessageBox.information(
            self, 'SupplyChain', 'Tutorial work in progress')

    def faq(self):
        QMessageBox.information(
            self, 'SupplyChain', "FAQ work in progress")

    def tcu(self):
        self.inactivity_timer.stop()
        self.hide()
        self.vista_istruzioni = Istruzioni()
        self.vista_istruzioni.closed.connect(self.mostra)
        self.vista_istruzioni.show()

    def show_certificazioni(self):
        self.inactivity_timer.stop()
        self.hide()
        self.vista_certificazioni = VistaProdotti(
            self.controller, self.utente
        )
        self.vista_certificazioni.closed.connect(self.mostra)
        self.vista_certificazioni.show()

    def show_azienda(self):
        self.inactivity_timer.stop()
        self.hide()
        self.vista_azienda = VistaStatoAzienda(
            self.aggiorna_profilo, self.utente,
            self.controller, True
        )
        self.vista_azienda.closed.connect(self.mostra)
        self.vista_azienda.show()

    def aggiorna_profilo(self, utente):
        self.utente = utente

    def show_sviluppatori(self):
        self.inactivity_timer.stop()
        self.hide()
        self.vista_sviluppatori = VistaSviluppatori()
        self.vista_sviluppatori.closed.connect(self.mostra)
        self.vista_sviluppatori.show()

    def show_soglie(self):
        self.inactivity_timer.stop()
        self.hide()
        self.vista_soglie = VistaSoglie(True)
        self.vista_soglie.closed.connect(self.mostra)
        self.vista_soglie.show()

import pyotp
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QPushButton, \
    QHBoxLayout, QMainWindow, QMessageBox, QAction, QCheckBox, QStackedWidget, QComboBox

from controllers.controller_autenticazione import ControllerAutenticazione
from view import funzioni_utili
from view.home_page_aziende import HomePage
from view.home_page_certificatore import HomePageCertificatore
from view.home_page_guest import HomePageGuest

from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import pyotp


class VistaAccedi(QMainWindow):
    def __init__(self):
        super().__init__()

        self.controller = ControllerAutenticazione()

        self.home_certificatore = None
        self.home_page = None
        self.home_guest = None
        self.setWindowIcon(QIcon("images\\logo_centro.png"))

        # Elementi di layout
        self.login_label = QLabel("Login")
        self.section_switcher = QCheckBox()
        self.register_label = QLabel("Registrati")
        self.stacked_widget = QStackedWidget()

        self.username_label = QLabel('Nome Azienda:')
        self.username_input = QLineEdit()
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.otp_label = QLabel("Codice OTP")
        self.otp_input = QLineEdit()
        self.login_button = QPushButton('Accedi')
        self.guest_button = QPushButton('Entra come guest')
        self.logo = QLabel()

        self.username_label_ = QLabel('Nome Azienda:')
        self.username_input_ = QLineEdit()
        self.tipo_label = QLabel('Tipo Azienda:')
        self.tipo_input = QComboBox()
        self.indirizzo_label = QLabel('Indirizzo:')
        self.indirizzo_input = QLineEdit()
        self.password_label_ = QLabel('Password:')
        self.password_input_ = QLineEdit()
        self.conferma_password_label = QLabel('Conferma Password:')
        self.conferma_password_input = QLineEdit()
        self.tcu_cb = QCheckBox("Ho letto e accetto i termini e le condizioni d'uso")
        self.tcu = QLabel("Visualizza i termini e le condizioni d'uso")
        self.password = [
            self.password_input, self.password_input_, self.conferma_password_input]
        self.icons_action = []
        self.register_button = QPushButton('Registrati')

        self.password_visibile = False

        self.init_ui_()

    def init_ui_(self):
        self.setWindowTitle('SupplyChain')
        self.setGeometry(0, 0, 750, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        outer_layout = QVBoxLayout(central_widget)
        outer_layout.setAlignment(Qt.AlignCenter)  # Centra verticalmente

        # Add section switcher
        switcher_layout = QHBoxLayout()
        switcher_layout.setAlignment(Qt.AlignCenter)

        self.login_label.setFont(QFont("Times Roman", 11, QFont.Bold))
        self.login_label.setStyleSheet("color: green")

        self.section_switcher.setFixedSize(60, 30)
        self.section_switcher.setStyleSheet(funzioni_utili.stile_checkbox())
        self.section_switcher.stateChanged.connect(self.switch_section)

        self.register_label.setFont(QFont("Times Roman", 11, QFont.Bold))
        self.register_label.setStyleSheet("color: green")

        switcher_layout.addWidget(self.login_label)
        switcher_layout.addWidget(self.section_switcher)
        switcher_layout.addWidget(self.register_label)

        switcher_container = QVBoxLayout()
        switcher_container.addLayout(switcher_layout)
        switcher_container.setAlignment(Qt.AlignCenter)

        self.stacked_widget.setFixedWidth(600)  # Imposta dimensioni fisse per il QStackedWidget

        # Centra il QStackedWidget orizzontalmente e verticalmente
        stacked_container = QVBoxLayout()
        stacked_container.addWidget(self.stacked_widget, alignment=Qt.AlignCenter)
        stacked_container.setAlignment(Qt.AlignCenter)

        outer_layout.addLayout(stacked_container)

        outer_layout.addLayout(switcher_container)

        # Login section
        login_widget = QWidget()
        self.init_login_ui(login_widget)
        self.stacked_widget.addWidget(login_widget)

        # Registrati section
        registrati_widget = QWidget()
        self.init_registrati_ui(registrati_widget)
        self.stacked_widget.addWidget(registrati_widget)

        funzioni_utili.center(self)

    def init_login_ui(self, widget):
        main_layout = QVBoxLayout(widget)

        welcome_label = QLabel('Benvenuto!')

        form_layout = QFormLayout()

        form_container = QVBoxLayout()

        funzioni_utili.config_widget(
            main_layout, welcome_label, form_layout, form_container, 100
        )

        funzioni_utili.add_field_to_form(
            self.username_label, self.username_input, form_layout)

        self.password_input.setEchoMode(QLineEdit.Password)
        funzioni_utili.add_field_to_form(
            self.password_label, self.password_input, form_layout)

        funzioni_utili.add_field_to_form(
            self.otp_label, self.otp_input, form_layout
        )

        main_layout.addLayout(form_container)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.setAlignment(Qt.AlignCenter)

        self.login_button.clicked.connect(lambda: self.accedi())
        funzioni_utili.insert_button(self.login_button, button_layout)

        self.guest_button.clicked.connect(self.entra_guest)
        funzioni_utili.insert_button(self.guest_button, button_layout)

        main_layout.addLayout(button_layout)

        self.logo.setPixmap(QPixmap("images\\logo_trasparente.png"))
        self.logo.setScaledContents(True)
        self.logo.setFixedSize(300, 300)
        main_layout.addWidget(self.logo, alignment=Qt.AlignCenter)

    def init_registrati_ui(self, widget):
        main_layout = QVBoxLayout(widget)

        registrati_label = QLabel('Registrati!')

        form_layout = QFormLayout()

        form_container = QVBoxLayout()

        funzioni_utili.config_widget(
            main_layout, registrati_label, form_layout, form_container, 100
        )

        funzioni_utili.add_field_to_form(
            self.username_label_, self.username_input_, form_layout)

        self.tipo_input.addItems([
            'Agricola', 'Trasportatore', 'Trasformatore', 'Rivenditore', 'Certificatore'
        ])
        funzioni_utili.add_field_to_form(self.tipo_label, self.tipo_input, form_layout)

        funzioni_utili.add_field_to_form(
            self.indirizzo_label, self.indirizzo_input, form_layout)

        self.password_input_.setEchoMode(QLineEdit.Password)
        funzioni_utili.add_field_to_form(
            self.password_label_, self.password_input_, form_layout)

        self.conferma_password_input.setEchoMode(QLineEdit.Password)
        funzioni_utili.add_field_to_form(
            self.conferma_password_label, self.conferma_password_input, form_layout)

        for p in self.password:
            self.icons_action.append(QAction(QIcon("images\\pass_invisibile.png"), "", p))
        for index, p in enumerate(self.password):
            self.icons_action[index].triggered.connect(self.change_password_visibility)
            p.addAction(self.icons_action[index], QLineEdit.TrailingPosition)

        main_layout.addLayout(form_container)

        main_layout.addWidget(self.tcu_cb, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.tcu, alignment=Qt.AlignCenter)

        self.tcu.setStyleSheet("color: blue; text-decoration: underline;")
        self.tcu.mousePressEvent = self.on_tcu_click

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.setAlignment(Qt.AlignCenter)

        self.register_button.clicked.connect(self.registrati)
        funzioni_utili.insert_button(self.register_button, button_layout)

        main_layout.addLayout(button_layout)

    def on_tcu_click(self, event):
        QMessageBox.warning(
            self, "SupplyChain", f"Termini e condizioni d'uso work in progress!")

    def switch_section(self, state):
        if state == Qt.Checked:
            self.stacked_widget.setCurrentIndex(1)
        else:
            self.stacked_widget.setCurrentIndex(0)

    def accedi(self):
        username = self.username_input.text()
        password = self.password_input.text()
        otp_code = self.otp_input.text()

        if "'" in username or " " in username or " " in password or "'" in password:
            QMessageBox.warning(
                self, "SupplyChain",
                "È inutile che provi la SQL injection.\n"
                "Le query nel database sono state implementate in modo parametrico :D"
            )
        else:
            # Verifica le credenziali dell'utente
            # utente = self.controller.login(username, password, otp_code)

            utente, messaggio = self.controller.login(username, password, otp_code)

            if not utente:
                QMessageBox.warning(self, "SupplyChain", messaggio)
            else:
                QMessageBox.information(self, "SupplyChain", messaggio)

                # Procedi con il resto del login come prima
                if utente[2] == 'Certificatore':
                    self.home_certificatore = HomePageCertificatore(self.reset, utente)
                    self.home_certificatore.show()
                else:
                    self.home_page = HomePage(self.reset, utente)
                    self.home_page.show()

                self.setVisible(False)  # Nascondi la finestra di login

    def entra_guest(self):
        self.home_guest = HomePageGuest(self.reset)
        QMessageBox.information(
            self, "EdilGest", "Puoi entrare come guest!")
        self.home_guest.show()
        self.close()

    def registrati(self):
        if not self.tcu_cb.isChecked():
            QMessageBox.warning(
                self, "SupplyChain", "Devi accettare i termini e le condizioni d'uso!")
        else:
            username = self.username_input_.text()
            password = self.password_input_.text()
            conferma_password = self.conferma_password_input.text()
            tipo = self.tipo_input.currentText()
            indirizzo = self.indirizzo_input.text()

            if funzioni_utili.is_blank([
                username, password, conferma_password, tipo, indirizzo
            ]):
                QMessageBox.warning(
                    self, "SupplyChain", "Completare tutti i campi!")
            elif password != conferma_password:
                QMessageBox.warning(
                    self, "SupplyChain", "Conferma password errata!")
            else:
                success, message, secret_key = self.controller.registrazione(
                    username, password, tipo, indirizzo
                )
                if success:
                    QMessageBox.information(self, "Successo", message)

                    # Mostra il dialogo per inserire il codice OTP
                    while True:  # Ciclo che ripete il dialogo finché il codice OTP non è corretto
                        dialog = SecretKeyDialog(secret_key)
                        dialog.exec_()

                        # Se l'OTP è corretto
                        if dialog.result() == QDialog.Accepted:
                            self.reset()
                            self.switch_section(Qt.Unchecked)
                            self.section_switcher.setChecked(False)
                            break  # Esci dal ciclo, registrazione completata
                        else:
                            # Se il codice OTP è errato, mostra un messaggio di errore
                            QMessageBox.warning(self, "Errore", "OTP errato, riprova.")
                else:
                    QMessageBox.warning(self, "Errore", message)

    def change_password_visibility(self):
        self.password_visibile = not self.password_visibile
        if not self.password_visibile:
            for index, p in enumerate(self.password):
                p.setEchoMode(QLineEdit.Password)
                self.icons_action[index].setIcon(QIcon("images\\pass_invisibile.png"))
        else:
            for index, p in enumerate(self.password):
                p.setEchoMode(QLineEdit.Normal)
                self.icons_action[index].setIcon(QIcon("images\\pass_visibile.png"))

    def reset(self):
        self.tcu_cb.setChecked(False)
        self.username_input.setText("")
        self.password_input.setText("")
        self.username_input_.setText("")
        self.indirizzo_input.setText("")
        self.password_input_.setText("")
        self.conferma_password_input.setText("")
        self.otp_input.setText("")
        self.password_visibile = False
        self.setVisible(True)


class SecretKeyDialog(QDialog):
    def __init__(self, secret_key):
        super().__init__()
        self.secret_key = secret_key  # La chiave segreta dell'utente
        self.setWindowTitle("Inserisci la chiave segreta nell'app di autenticazione")

        # Crea l'oggetto TOTP usando la chiave segreta
        self.totp = pyotp.TOTP(self.secret_key)

        # Layout e widget per la finestra di dialogo
        layout = QVBoxLayout()
        self.label = QLabel(f"Chiave segreta: {self.secret_key}\nInserisci questa chiave nell'app di autenticazione.")
        self.instruction_label = QLabel("Una volta inserita, inserisci il codice OTP generato.")
        self.otp_input = QLineEdit()
        self.confirm_button = QPushButton("Conferma")
        self.confirm_button.setEnabled(
            False)  # Disabilita il pulsante fino a quando non viene inserito un codice valido
        self.confirm_button.clicked.connect(self.confirm_secret_key)

        layout.addWidget(self.label)
        layout.addWidget(self.instruction_label)
        layout.addWidget(self.otp_input)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

        # Convalida del codice OTP mentre viene inserito
        self.otp_input.textChanged.connect(self.check_otp)

    def check_otp(self):
        """Verifica che l'OTP inserito sia corretto e abilita il pulsante di conferma"""
        otp_code = self.otp_input.text()
        if self.totp.verify(otp_code):
            self.confirm_button.setEnabled(True)  # Abilita il pulsante se il codice è valido
        else:
            self.confirm_button.setEnabled(False)  # Mantieni il pulsante disabilitato se il codice non è valido

    def confirm_secret_key(self):
        """Procedi con la registrazione se il codice OTP è corretto"""
        otp_code = self.otp_input.text()
        if self.totp.verify(otp_code):
            QMessageBox.information(self, "Successo", "Codice OTP corretto. Registrazione completata.")
            self.accept()  # Procedi con la registrazione
        else:
            QMessageBox.warning(self, "Errore", "Codice OTP errato. Inserisci un codice valido.")
            self.otp_input.clear()  # Pulisce il campo di inserimento OTP

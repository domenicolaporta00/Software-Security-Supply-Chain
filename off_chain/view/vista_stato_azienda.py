from PyQt5.QtCore import Qt, QRegExp, QRegularExpression, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QRegExpValidator
from PyQt5.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QWidget, QFormLayout, QLineEdit,
                             QHBoxLayout, QPushButton, QMessageBox, QAction)

from view import funzioni_utili


class VistaStatoAzienda(QMainWindow):
    closed = pyqtSignal()

    def __init__(self, callback, azienda, controller, is_certificatore=False):
        super().__init__()

        self.callback = callback
        self.azienda = azienda
        self.controller = controller
        self.is_certificatore = is_certificatore

        self.dettaglio = self.controller.get_dettaglio_azienda(self.azienda[0])[0]

        # Elementi di layout
        self.id_azienda_label = QLabel("ID")
        self.id_azienda_input = QLineEdit(str(self.azienda[0]))

        self.nome_label = QLabel("Nome")
        self.nome_input = QLineEdit(str(self.azienda[3]))

        self.tipo_label = QLabel("Tipo")
        self.tipo_input = QLineEdit(str(self.azienda[2]))

        self.indirizzo_label = QLabel("Indirizzo")
        self.indirizzo_input = QLineEdit(str(self.azienda[4]))

        self.email_label = QLabel("Email")
        self.email_input = QLineEdit(str(self.azienda[6]))

        self.co2_consumata_totale_label = QLabel("CO2 consumata totale")
        self.co2_consumata_totale_input = QLineEdit("100")  # Da modificare con la query corretta

        self.co2_risparmiata_totale_label = QLabel("CO2 risparmiata totale")
        self.co2_risparmiata_totale_input = QLineEdit("50")  # Da modificare con la query corretta

        self.saldo_totale_label = QLabel("Saldo CO2 complessivo")
        self.saldo_totale_input = QLineEdit("(100)")  # Da modificare con la query corretta

        self.certificazioni_label = QLabel("Certificazioni effettuate")
        self.certificazioni_input = QLineEdit("3")  # Da modificare con la query corretta

        self.vecchia_password_label = QLabel("Vecchia password")
        self.vecchia_password_input = QLineEdit()

        self.nuova_password_label = QLabel("Nuova password")
        self.nuova_password_input = QLineEdit()

        self.conferma_password_label = QLabel("Conferma password")
        self.conferma_password_input = QLineEdit()

        self.tipo_label = QLabel("Tipo")
        self.tipo_input = QLineEdit(str(self.azienda[2]))

        self.passwords = [
            self.vecchia_password_input, self.nuova_password_input,
            self.conferma_password_input
        ]
        self.icons_action = []

        self.conferma_button = QPushButton('Conferma modifiche')

        self.setWindowIcon(QIcon("images\\logo_centro.png"))

        self.password_visibile = False

        self.init_ui()

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()

    def init_ui(self):
        self.setWindowTitle('SupplyChain')
        self.setGeometry(0, 0, 750, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        outer_layout = QVBoxLayout(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignCenter)  # Centra verticalmente

        welcome_label = QLabel('Informazioni azienda')
        funzioni_utili.insert_label(welcome_label, main_layout)

        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        form_container = QVBoxLayout()
        form_container.addLayout(form_layout)
        form_container.setContentsMargins(150, 0, 150, 0)

        self.id_azienda_input.setReadOnly(True)
        funzioni_utili.add_field_to_form(self.id_azienda_label, self.id_azienda_input, form_layout)

        self.nome_input.setReadOnly(True)
        # self.nome_input.setValidator(QRegExpValidator(QRegExp("[A-Za-z0-9 ]+")))  # Nome con lettere e numeri
        funzioni_utili.add_field_to_form(self.nome_label, self.nome_input, form_layout)

        self.tipo_input.setReadOnly(True)
        funzioni_utili.add_field_to_form(self.tipo_label, self.tipo_input, form_layout)

        # self.indirizzo_input.setReadOnly(True)
        self.indirizzo_input.setValidator(QRegExpValidator(QRegExp("[A-Za-z0-9, ]+")))  # Lettere, numeri e virgole
        funzioni_utili.add_field_to_form(self.indirizzo_label, self.indirizzo_input, form_layout)

        funzioni_utili.add_field_to_form(self.email_label, self.email_input, form_layout)

        if not self.is_certificatore:
            self.co2_consumata_totale_input.setText(str(self.dettaglio[1]))
            self.co2_consumata_totale_input.setReadOnly(True)
            funzioni_utili.add_field_to_form(self.co2_consumata_totale_label, self.co2_consumata_totale_input,
                                             form_layout)

            self.co2_risparmiata_totale_input.setText(str(self.dettaglio[2]))
            self.co2_risparmiata_totale_input.setReadOnly(True)
            funzioni_utili.add_field_to_form(self.co2_risparmiata_totale_label, self.co2_risparmiata_totale_input,
                                             form_layout)

            saldo = self.dettaglio[2] - self.dettaglio[1]
            if saldo < 0:
                saldo = f"({-saldo})"
            self.saldo_totale_input.setText(str(saldo))
            self.saldo_totale_input.setReadOnly(True)
            funzioni_utili.add_field_to_form(self.saldo_totale_label, self.saldo_totale_input, form_layout)

        else:
            self.certificazioni_input.setText(str(self.dettaglio))
            self.certificazioni_input.setReadOnly(True)
            funzioni_utili.add_field_to_form(self.certificazioni_label, self.certificazioni_input,
                                             form_layout)

        funzioni_utili.add_field_to_form(
            self.vecchia_password_label, self.vecchia_password_input, form_layout)
        self.vecchia_password_input.setEchoMode(QLineEdit.Password)
        vecchia_password = str(self.controller.recupera_password(self.azienda[0]))
        self.vecchia_password_input.setText(vecchia_password)  # Da togliere

        funzioni_utili.add_field_to_form(
            self.nuova_password_label, self.nuova_password_input, form_layout)
        self.nuova_password_input.setEchoMode(QLineEdit.Password)

        funzioni_utili.add_field_to_form(
            self.conferma_password_label, self.conferma_password_input, form_layout)
        self.conferma_password_input.setEchoMode(QLineEdit.Password)

        for p in self.passwords:
            self.icons_action.append(QAction(QIcon("images\\pass_invisibile.png"), "", p))
        for index, p in enumerate(self.passwords):
            self.icons_action[index].triggered.connect(self.change_password_visibility)
            p.addAction(self.icons_action[index], QLineEdit.TrailingPosition)

        main_layout.addLayout(form_container)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.setAlignment(Qt.AlignCenter)

        funzioni_utili.insert_button(self.conferma_button, button_layout)
        self.conferma_button.clicked.connect(self.on_conferma_button_clicked)

        main_layout.addLayout(button_layout)

        outer_layout.addLayout(main_layout)

        funzioni_utili.center(self)

    def on_conferma_button_clicked(self):
        id_azienda = self.id_azienda_input.text()
        indirizzo = self.indirizzo_input.text()
        email = self.email_input.text()
        password_from_db = self.controller.recupera_password(self.azienda[0])
        vecchia_password = self.vecchia_password_input.text()
        nuova_password = self.nuova_password_input.text()
        conferma_password = self.conferma_password_input.text()

        self.modifica(
            id_azienda, indirizzo, email, vecchia_password,
            nuova_password, conferma_password, password_from_db
        )

    def modifica(self, id_azienda, indirizzo, email, vecchia_password,
                 nuova_password, conferma_password, password_from_db):
        # Controlla se ci sono campi vuoti
        if funzioni_utili.is_blank([indirizzo, email, vecchia_password,
                                    nuova_password, conferma_password]):
            QMessageBox.information(self, "SupplyChain", "Completare tutti i campi!")
            return

        # Verifica che la vecchia password sia corretta
        if vecchia_password != password_from_db:
            QMessageBox.warning(self, "Errore", "La password inserita non è corretta!")
            return

        # Verifica che la nuova password e la conferma siano uguali
        if nuova_password != conferma_password:
            QMessageBox.warning(self, "Errore", "Conferma password errata!")
            return

        # Verifica che la nuova password non sia identica alla vecchia
        if nuova_password == password_from_db:
            QMessageBox.warning(self, "Errore", "La nuova password è identica a quella vecchia!")
            return

        # TODO: Aggiungere la logica per il controllo di UNIQUE Azienda(Email) e Azienda(Indirizzo) nel DB

        # Modifica i dati aziendali
        success, message = self.controller.modifica_dati_azienda(id_azienda, email, indirizzo)
        # TODO: Implementare la funzione per modificare la password

        if success:
            QMessageBox.information(self, "SupplyChain", message)
            nuovo_utente = self.controller.get_anagrafica_azienda(id_azienda)[0]
            self.callback(nuovo_utente)
            self.close()
        else:
            QMessageBox.warning(self, "Errore", message)

    def change_password_visibility(self):
        self.password_visibile = not self.password_visibile
        if not self.password_visibile:
            for index, p in enumerate(self.passwords):
                p.setEchoMode(QLineEdit.Password)
                self.icons_action[index].setIcon(QIcon("images\\pass_invisibile.png"))
        else:
            for index, p in enumerate(self.passwords):
                p.setEchoMode(QLineEdit.Normal)
                self.icons_action[index].setIcon(QIcon("images\\pass_visibile.png"))

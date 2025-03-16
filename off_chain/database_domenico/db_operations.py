import os
import sqlite3
import hashlib
import re
from off_chain.database_domenico.db_operations import Database

class DuplicatedEntryError(Exception):
    """Eccezione personalizzata per i dati duplicati nel database."""
    pass


class Database:
    def __init__(self, db_path='database.db'):
        # Percorso assoluto del database nella cartella del progetto
        if db_path == 'database.db':  # Se viene usato il percorso di default
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.db_path = os.path.join(BASE_DIR, db_path)
        else:
            self.db_path = db_path

        # Controlla che il database esista prima di connettersi
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database non trovato: {self.db_path}")

        # Connessione al database esistente
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()

    def fetch_query(self, query, params=()):
        """Esegue una SELECT e restituisce i risultati"""
        try:
            self.cur.execute(query, params)
            return self.cur.fetchall()
        except sqlite3.Error as e:
            raise RuntimeError(f"Errore SQLite durante la SELECT: {e}")

    def execute_query(self, query, params=()):
        """Esegue una query di modifica (INSERT, UPDATE, DELETE) sul database"""
        try:
            self.cur.execute(query, params)
            self.conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Errore SQLite durante l'esecuzione della query: {e}")

    def co2_consumata_prodotti(self, prodotti):
        lista_con_co2 = []
        for prodotto in prodotti:
            storico = self.get_storico_prodotto(prodotto[0])
            totale_co2 = sum(t[4] for t in storico)
            lista_con_co2.append((prodotto, totale_co2))
        return lista_con_co2

    # Restituisce la lista di prodotti sugli scaffali per il guest
    def get_lista_prodotti(self):
        query = """
        SELECT
            Prodotto.Id_prodotto,
            Prodotto.Nome,
            Prodotto.Quantita,
            Prodotto.Stato,
            Azienda.Nome
        FROM Operazione
        JOIN Azienda ON Operazione.Id_azienda = Azienda.Id_azienda
        JOIN Prodotto ON Operazione.Id_prodotto = Prodotto.Id_prodotto
        WHERE Operazione.Operazione = "Messo sugli scaffali";
        """
        return self.co2_consumata_prodotti(self.fetch_query(query))

    # Restituisce tutti i prodotti sugli scaffali ordinati per co2 consumata
    def get_prodotti_ordinati_co2(self):
        return sorted(self.get_lista_prodotti(), key=lambda x: x[1])

    # Restituisce tutti i prodotti sugli scaffali con un certo nome
    def get_prodotti_by_nome(self, nome):
        query = """
                SELECT
                    Prodotto.Id_prodotto,
                    Prodotto.Nome,
                    Prodotto.Quantita,
                    Prodotto.Stato,
                    Azienda.Nome
                FROM Operazione
                JOIN Azienda ON Operazione.Id_azienda = Azienda.Id_azienda
                JOIN Prodotto ON Operazione.Id_prodotto = Prodotto.Id_prodotto
                WHERE Operazione.Operazione = "Messo sugli scaffali"
                AND Prodotto.Nome = ?;
                """
        return self.co2_consumata_prodotti(self.fetch_query(query, (nome,)))

    # Restituisce una lista di prodotti sullo scaffale filtrati per rivenditore
    def get_lista_prodotti_by_rivenditore(self, rivenditore):
        query = """
        SELECT
            Prodotto.Id_prodotto,
            Prodotto.Nome,
            Prodotto.Quantita,
            Prodotto.Stato,
            Azienda.Nome
        FROM Operazione
        JOIN Azienda ON Operazione.Id_azienda = Azienda.Id_azienda
        JOIN Prodotto ON Operazione.Id_prodotto = Prodotto.Id_prodotto
        WHERE Operazione.Operazione = "Messo sugli scaffali"
        AND Operazione.Id_azienda = ?;
        """
        return self.co2_consumata_prodotti(self.fetch_query(query, (rivenditore,)))

    # Restituisce la lista di tutti i prodotti sullo scaffale certificati
    def get_prodotti_certificati(self):
        query = """
        SELECT
            Prodotto.Id_prodotto,
            Prodotto.Nome,
            Prodotto.Quantita,
            Prodotto.Stato,
            Azienda.Nome
        FROM Operazione
        JOIN Azienda ON Operazione.Id_azienda = Azienda.Id_azienda
        JOIN Prodotto ON Operazione.Id_prodotto = Prodotto.Id_prodotto
        WHERE Operazione.Operazione = "Messo sugli scaffali"
        AND Operazione.Id_prodotto IN (
            SELECT Id_prodotto FROM Certificato
        );
        """
        return self.co2_consumata_prodotti(self.fetch_query(query))

    # Restituisce i prodotti certificati sullo scaffale filtrati per rivenditore
    def get_prodotti_certificati_by_rivenditore(self, id_rivenditore):
        query = """
        SELECT
            Prodotto.Id_prodotto,
            Prodotto.Nome,
            Prodotto.Quantita,
            Prodotto.Stato,
            Azienda.Nome
        FROM Operazione
        JOIN Azienda ON Operazione.Id_azienda = Azienda.Id_azienda
        JOIN Prodotto ON Operazione.Id_prodotto = Prodotto.Id_prodotto
        WHERE Operazione.Operazione = "Messo sugli scaffali"
        AND Operazione.Id_prodotto IN (
            SELECT Id_prodotto FROM Certificato
        )
        AND Operazione.Id_azienda = ?;
        """
        return self.co2_consumata_prodotti(self.fetch_query(query, (id_rivenditore,)))

    # Restituisce i prodotti certificati sullo scaffale ordinati per co2 consumata
    def get_prodotti_certificati_ordinati_co2(self):
        return sorted(self.get_prodotti_certificati(), key=lambda x: x[1])

    # Restituisce i prodotti certificati sullo scaffale filtrati per nome
    def get_prodotti_certificati_by_nome(self, nome):
        query = """
        SELECT
            Prodotto.Id_prodotto,
            Prodotto.Nome,
            Prodotto.Quantita,
            Prodotto.Stato,
            Azienda.Nome
        FROM Operazione
        JOIN Azienda ON Operazione.Id_azienda = Azienda.Id_azienda
        JOIN Prodotto ON Operazione.Id_prodotto = Prodotto.Id_prodotto
        WHERE Operazione.Operazione = "Messo sugli scaffali"
        AND Operazione.Id_prodotto IN (
            SELECT Id_prodotto FROM Certificato
        )
        AND Prodotto.Nome = ?;
        """
        return self.co2_consumata_prodotti(self.fetch_query(query, (nome,)))

    # Restituisce lo storico del prodotto selezionato
    def get_storico_prodotto(self, prodotto):
        query = """
        SELECT
            Operazione.Id_operazione,
            Azienda.Nome,
            Prodotto.Nome,
            Operazione.Data_operazione,
            Operazione.Consumo_CO2,
            Operazione.Operazione
        FROM Operazione
        JOIN Azienda ON Operazione.Id_azienda = Azienda.Id_azienda
        JOIN Prodotto ON Operazione.Id_prodotto = Prodotto.Id_prodotto
        WHERE Operazione.Id_prodotto IN (
            SELECT Materia_prima
            FROM Composizione
            WHERE Prodotto = ?
        );
        """
        return self.fetch_query(query, (prodotto,))

    # Restituisce la certificazione del prodotto selezionato
    def get_certificazione_by_prodotto(self, prodotto):
        query = """
        SELECT 
            Certificato.Id_certificato,
            Prodotto.Nome,
            Certificato.Descrizione,
            Azienda.Nome,
            Certificato.Data
        FROM Certificato
        JOIN Azienda ON Certificato.Id_azienda_certificatore = Azienda.Id_azienda
        JOIN Prodotto ON Certificato.Id_prodotto = Prodotto.Id_prodotto
        WHERE Certificato.Id_prodotto = ?;
        """
        return self.fetch_query(query, (prodotto,))

    # Restituisce la lista dei rivenditori
    def get_lista_rivenditori(self):
        query = """
        SELECT Id_azienda, Tipo, Indirizzo, Nome FROM Azienda WHERE Tipo = "Rivenditore"
        """
        return self.fetch_query(query)

    # Restituisce la lista di tutte le aziende con i rispettivi valori di CO2 consumata e compensata
    def get_lista_aziende(self):
        query = """
        SELECT Id_azienda, Tipo, Indirizzo, Nome FROM Azienda WHERE Tipo != "Certificatore"
        """
        aziende = self.fetch_query(query)
        lista_con_co2 = []
        for azienda in aziende:
            query_co2_consumata = """
            SELECT SUM(Consumo_CO2) FROM Operazione WHERE Id_azienda = ?;
            """
            query_co2_compensata = """
            SELECT SUM(Co2_compensata) FROM Azioni_compensative WHERE Id_azienda = ?;
            """
            if not self.fetch_query(query_co2_consumata, (azienda[0],))[0][0]:
                co2_consumata = 0
            else:
                co2_consumata = self.fetch_query(query_co2_consumata, (azienda[0],))[0][0]
            if not self.fetch_query(query_co2_compensata, (azienda[0],))[0][0]:
                co2_compensata = 0
            else:
                co2_compensata = self.fetch_query(query_co2_compensata, (azienda[0],))[0][0]
            lista_con_co2.append((azienda, co2_consumata, co2_compensata))
        return lista_con_co2

    # Restituisce la lista ordinata per saldo CO2 di tutte le aziende
    def get_lista_aziende_ordinata(self):
        lista_ordinata = sorted(self.get_lista_aziende(), key=lambda x: (x[2] or 0) - (x[1] or 0), reverse=True)
        return lista_ordinata

    # Restituisce la lista di tutte le aziende con i rispettivi valori di CO2 consumata e compensata
    # filtrata per tipo
    def get_lista_aziende_filtrata_tipo(self, tipo):
        query = """
        SELECT Id_azienda, Tipo, Indirizzo, Nome FROM Azienda WHERE Tipo != "Certificatore"
        AND Tipo = ?
        """
        aziende = self.fetch_query(query, (tipo,))
        lista_con_co2 = []
        for azienda in aziende:
            query_co2_consumata = """
            SELECT SUM(Consumo_CO2) FROM Operazione WHERE Id_azienda = ?;
            """
            query_co2_compensata = """
            SELECT SUM(Co2_compensata) FROM Azioni_compensative WHERE Id_azienda = ?;
            """
            if not self.fetch_query(query_co2_consumata, (azienda[0],))[0][0]:
                co2_consumata = 0
            else:
                co2_consumata = self.fetch_query(query_co2_consumata, (azienda[0],))[0][0]
            if not self.fetch_query(query_co2_compensata, (azienda[0],))[0][0]:
                co2_compensata = 0
            else:
                co2_compensata = self.fetch_query(query_co2_compensata, (azienda[0],))[0][0]
            lista_con_co2.append((azienda, co2_consumata, co2_compensata))
        return lista_con_co2

    # Restituisce la lista di tutte le aziende con i rispettivi valori di CO2 consumata e compensata
    # filtrata per nome
    def get_azienda_by_nome(self, nome):
        query = """
        SELECT Id_azienda, Tipo, Indirizzo, Nome FROM Azienda WHERE Tipo != "Certificatore"
        AND Nome = ?
        """
        aziende = self.fetch_query(query, (nome,))
        lista_con_co2 = []
        for azienda in aziende:
            query_co2_consumata = """
            SELECT SUM(Consumo_CO2) FROM Operazione WHERE Id_azienda = ?;
            """
            query_co2_compensata = """
            SELECT SUM(Co2_compensata) FROM Azioni_compensative WHERE Id_azienda = ?;
            """
            if not self.fetch_query(query_co2_consumata, (azienda[0],))[0][0]:
                co2_consumata = 0
            else:
                co2_consumata = self.fetch_query(query_co2_consumata, (azienda[0],))[0][0]
            if not self.fetch_query(query_co2_compensata, (azienda[0],))[0][0]:
                co2_compensata = 0
            else:
                co2_compensata = self.fetch_query(query_co2_compensata, (azienda[0],))[0][0]
            lista_con_co2.append((azienda, co2_consumata, co2_compensata))
        return lista_con_co2

    def get_azienda_by_id(self, id_):
        query = """
        SELECT Id_azienda, Tipo, Indirizzo, Nome, Email FROM Azienda WHERE Id_azienda = ?;
        """
        aziende = self.fetch_query(query, (id_,))
        lista_con_co2 = []
        for azienda in aziende:
            query_co2_consumata = """
            SELECT SUM(Consumo_CO2) FROM Operazione WHERE Id_azienda = ?;
            """
            query_co2_compensata = """
            SELECT SUM(Co2_compensata) FROM Azioni_compensative WHERE Id_azienda = ?;
            """
            if not self.fetch_query(query_co2_consumata, (azienda[0],))[0][0]:
                co2_consumata = 0
            else:
                co2_consumata = self.fetch_query(query_co2_consumata, (azienda[0],))[0][0]
            if not self.fetch_query(query_co2_compensata, (azienda[0],))[0][0]:
                co2_compensata = 0
            else:
                co2_compensata = self.fetch_query(query_co2_compensata, (azienda[0],))[0][0]
            lista_con_co2.append((azienda, co2_consumata, co2_compensata))
        return lista_con_co2

    def get_azienda(self, n):
        return self.get_lista_aziende()[n]

    def get_anagrafica_azienda(self, id_):
        query = """
        SELECT * FROM Azienda WHERE Id_azienda = ?
        """
        return self.fetch_query(query, (id_,))

    def modifica_dati_azienda(self, id_azienda, nuova_email, nuovo_indirizzo):
        query = """
        UPDATE Azienda 
        SET Email = ?, Indirizzo = ?
        WHERE Id_azienda = ? 
        """
        try:
            self.cur.execute(query, (nuova_email, nuovo_indirizzo, id_azienda, ))
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise DuplicatedEntryError("L'email o l'indirizzo sono già in uso.")
        except Exception as e:
            raise Exception(f"Errore generico: {str(e)}")  # Cattura altre eccezioni generiche

    @staticmethod
    def hash_password(password):
        """Esegue l'hashing della password usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def modifica_password(self, id_azienda, vecchia_password, nuova_password):
        """Modifica la password di un'azienda dopo aver verificato quella attuale"""

        # Recupera la password attuale dal database
        query_get_password = """
        SELECT Password FROM Credenziali WHERE Id_credenziali = (
            SELECT Id_credenziali FROM Azienda WHERE Id_azienda = ?
        );
        """
        password_db = self.fetch_query(query_get_password, (id_azienda,))

        if not password_db:
            raise ValueError("Azienda non trovata o credenziali non valide.")

        # Confronta la password inserita con quella memorizzata (già hashata)
        hashed_old_password = self.hash_password(vecchia_password)
        if password_db[0][0] != hashed_old_password:
            raise ValueError("La vecchia password non è corretta.")

        # Controllo sulla nuova password
        if len(nuova_password) < 8:
            raise ValueError("La password deve contenere almeno 8 caratteri!")
        if not re.search(r'[A-Z]', nuova_password):
            raise ValueError("La password deve contenere almeno una lettera maiuscola.")
        if not re.search(r'[a-z]', nuova_password):
            raise ValueError("La password deve contenere almeno una lettera minuscola.")
        if not re.search(r'[0-9]', nuova_password):
            raise ValueError("La password deve contenere almeno un numero.")
        if not re.search(r'\W', nuova_password):
            raise ValueError("La password deve contenere almeno un carattere speciale (!, @, #, etc.).")
        if "'" in nuova_password or " " in nuova_password:
            raise ValueError("La password non può contenere spazi o caratteri pericolosi.")

        # Hash della nuova password
        hashed_new_password = self.hash_password(nuova_password)

        # Aggiorna la password nel database
        query_update_password = """
        UPDATE Credenziali 
        SET Password = ? 
        WHERE Id_credenziali = (
            SELECT Id_credenziali FROM Azienda WHERE Id_azienda = ?
        );
        """
        self.execute_query(query_update_password, (hashed_new_password, id_azienda))
        return True

    # Restituisce la password dell'azienda
    def get_password(self, id_azienda):
        query = """
        SELECT Password
        FROM Credenziali
        WHERE Id_credenziali = ?
        """
        return self.fetch_query(query, (id_azienda,))[0][0]
        
    # Verifica la password dell'azienda
    def verify_password(self, id_azienda, password):
        """Verifica se la password fornita corrisponde a quella memorizzata per l'azienda"""
        # Recupera la password attuale dal database
        query_get_password = """
        SELECT Password FROM Credenziali WHERE Id_credenziali = (
            SELECT Id_credenziali FROM Azienda WHERE Id_azienda = ?
        );
        """
        password_db = self.fetch_query(query_get_password, (id_azienda,))

        if not password_db:
            return False

        # Confronta la password inserita con quella memorizzata (già hashata)
        hashed_password = self.hash_password(password)
        return password_db[0][0] == hashed_password

    # Restituisce il numero di certificazioni di un'azienda
    def get_numero_certificazioni(self, id_azienda):
        query = """
        SELECT COUNT(*) FROM Certificato WHERE Id_azienda_certificatore = ?;
        """
        return self.fetch_query(query, (id_azienda,))[0]

    # Restituisce true se il prodotto è certificato, false altrimenti
    def is_certificato(self, id_prodotto):
        query = """
        SELECT * FROM Certificato WHERE Id_prodotto = ?;
        """
        if not self.fetch_query(query, (id_prodotto,)):
            return False
        return True

    # Inserisce un nuovo certificato
    def inserisci_certificato(self, prodotto, tipo, azienda, data):
        query = """
        INSERT INTO Certificato (Id_prodotto, Descrizione, Id_azienda_certificatore, Data)
        VALUES (?, ?, ?, ?);
        """
        self.execute_query(query, (prodotto, tipo, azienda, data))

    # Restituisce la lista delle azioni compensative per azienda
    def get_lista_azioni(self, id_azienda):
        query = """
        SELECT * FROM Azioni_compensative WHERE Id_azienda = ?;
        """
        return self.fetch_query(query, (id_azienda,))

    # Restituisce la lista di azioni compensative filtrate per data
    def get_lista_azioni_per_data(self, id_azienda, d1, d2):
        query = """
        SELECT * FROM Azioni_compensative
        WHERE Id_azienda = ? AND Data BETWEEN ? AND ?;
        """
        return self.fetch_query(query, (id_azienda, d1, d2))

    # Restituisce la lista di azioni compensative ordinata per co2 risparmiata
    def get_lista_azioni_ordinata(self, id_azienda):
        query = """
        SELECT * FROM Azioni_compensative
        WHERE Id_azienda = ?
        ORDER BY Co2_compensata DESC;
        """
        return self.fetch_query(query, (id_azienda,))

    # Restituisce il valore della co2 compensata per azienda
    def get_co2_compensata(self, id_azienda):
        query = """
        SELECT SUM(Co2_compensata) FROM Azioni_compensative WHERE Id_azienda = ?;
        """
        return self.fetch_query(query, (id_azienda,))[0][0]

    # Inserisce una nuova azione compensativa
    def inserisci_azione(self, data, azienda, co2_compensata, nome_azione):
        query = """
        INSERT INTO Azioni_compensative (Data, Id_azienda, Co2_compensata, Nome_azione)
        VALUES (?, ?, ?, ?);
        """
        self.execute_query(query, (data, azienda, co2_compensata, nome_azione))

    # Restituisce la lista di tutte le soglie
    def get_lista_soglie(self):
        query = """
        SELECT * FROM Soglie;
        """
        return self.fetch_query(query)

    # Le seguenti quattro funzioni restituiscono gli elementi che verranno visualizzati nelle
    # rispettive combo box, a seconda del tipo di azienda che sta effettuando l'operazione
    def get_prodotti_to_azienda_agricola(self):
        query = """
        SELECT DISTINCT Prodotto FROM Soglie WHERE Tipo = "materia prima";
        """
        lista_finale = []
        for i in self.fetch_query(query):
            lista_finale.append(i[0])
        return lista_finale

    def get_prodotti_to_azienda_trasporto(self, destinatario, id_azienda):
        query_to_trasformazione = """
        SELECT Prodotto.Id_prodotto, Prodotto.Nome, Prodotto.Quantita, Operazione.Destinatario
        FROM Prodotto JOIN Operazione
        ON Prodotto.Id_prodotto = Operazione.Id_prodotto
        WHERE Operazione.Destinatario = ?
        AND Prodotto.Stato = 00 OR Prodotto.Stato = 10
        AND Prodotto.Nome IN (
            SELECT Tipo
            FROM Soglie
            WHERE Tipo = "materia prima"
        );
        """
        query_to_rivenditore = """
        SELECT DISTINCT Prodotto.Id_prodotto, Prodotto.Nome, Prodotto.Quantita 
        FROM Prodotto JOIN Operazione
        WHERE Operazione.Destinatario = ?
        AND Prodotto.Stato = 00 OR Prodotto.Stato = 10;
        """
        if destinatario == "Azienda di trasformazione":
            return self.fetch_query(query_to_trasformazione, (id_azienda,))
        return self.fetch_query(query_to_rivenditore, (id_azienda,))

    def get_prodotti_to_azienda_trasformazione(self, operazione, id_azienda):
        if operazione == "Trasformazione":
            query = """
            SELECT Prodotto.Id_prodotto, Prodotto.Nome, Prodotto.Quantita
            FROM Prodotto JOIN Operazione
            ON Prodotto.Id_prodotto = Operazione.Id_prodotto
            WHERE Stato = 01
            AND Operazione.Operazione = "Trasporto"
            AND Operazione.Destinatario = ?;
            """
        else:
            query = """
            SELECT DISTINCT Prodotto FROM Soglie WHERE Tipo = "prodotto finale"
            """
            lista_finale = []
            for i in self.fetch_query(query):
                lista_finale.append(i[0])
            return lista_finale
        return self.fetch_query(query, (id_azienda,))

    def get_prodotti_to_rivenditore(self, id_azienda):
        query = """
        SELECT Prodotto.Id_prodotto, Prodotto.Nome, Prodotto.Quantita
        FROM Prodotto JOIN Operazione
        ON Prodotto.Id_prodotto = Operazione.Id_prodotto
        WHERE Stato = 11
        AND Operazione.Operazione = "Trasporto"
        AND Operazione.Destinatario = ?;
        """
        return self.fetch_query(query, (id_azienda,))

    # Questa funzione restituisce i prodotti che l'azienda di trasformazione
    # può inserire nella tabella "composizione" come valori dell'attributo "materia prima"
    def get_materie_prime(self, azienda):
        query = """
        SELECT Prodotto.Id_prodotto, Prodotto.Nome, Prodotto.Quantita
        FROM Prodotto
        JOIN Operazione
        ON Prodotto.Id_prodotto = Operazione.Id_prodotto
        WHERE Operazione.Operazione = "Trasformazione"
        AND Operazione.Id_azienda = ?
        ORDER BY Operazione.Data_operazione DESC;
        """
        return self.fetch_query(query, (azienda,))

    # Le seguenti quattro funzioni permettono l'inserimento di un'operazione
    # a seconda del tipo di azienda che la sta effettuando
    def inserisci_operazione_azienda_agricola(self, nome, quantita, azienda, data, co2, evento,
                                              destinatario):
        try:
            self.cur.execute("BEGIN TRANSACTION;")  # Inizio transazione

            # Inserisci il prodotto
            query_prodotto = """
            INSERT INTO Prodotto (Nome, Quantita, Stato) VALUES (?, ?, ?);
            """
            self.cur.execute(query_prodotto, (nome, quantita, 0))

            prodotto_id = self.cur.lastrowid  # Ottieni l'ID del prodotto inserito

            # Inserisci l'operazione
            query_operazione = """
            INSERT INTO Operazione (Id_azienda, Id_prodotto, Data_operazione, Consumo_CO2, Operazione, 
            Destinatario)
            VALUES (?, ?, ?, ?, ?, ?);
            """
            self.cur.execute(query_operazione, (
                azienda, prodotto_id, data, co2, evento, destinatario))

            self.conn.commit()  # Conferma la transazione

        except sqlite3.Error as e:
            self.conn.rollback()  # Annulla tutto se c'è un errore
            raise Exception(f"Errore durante l'inserimento: {str(e)}")  # Lancia un'eccezione

    def inserisci_operazione_azienda_trasporto(self, azienda, prodotto, data, co2, evento, nuovo_stato,
                                               destinatario):
        try:
            self.cur.execute("BEGIN TRANSACTION;")  # Inizio transazione

            # Inserisci l'operazione
            query_operazione = """
            INSERT INTO Operazione (Id_azienda, Id_prodotto, Data_operazione, Consumo_CO2, Operazione, 
            Destinatario)
            VALUES (?, ?, ?, ?, ?, ?);
            """
            self.cur.execute(query_operazione, (
                azienda, prodotto, data, co2, evento, destinatario))

            # Modifica lo stato del prodotto
            query_prodotto = """
            UPDATE Prodotto SET Stato = ? WHERE Id_prodotto = ?;
            """
            self.cur.execute(query_prodotto, (nuovo_stato, prodotto))

            if nuovo_stato == 11:  # Cioè se il destinatario è il rivenditore
                query_composizione = """
                INSERT OR IGNORE INTO Composizione VALUES(?, ?)
                """
                self.cur.execute(query_composizione, (prodotto, prodotto))

            self.conn.commit()  # Conferma la transazione

        except sqlite3.Error as e:
            self.conn.rollback()  # Annulla tutto se c'è un errore
            raise Exception(f"Errore durante l'inserimento: {str(e)}")  # Lancia un'eccezione

    def inserisci_operazione_azienda_trasformazione(self, azienda, prodotto, data, co2, evento,
                                                    destinatario, quantita=0, materie_prime=None):
        if materie_prime is None:
            materie_prime = []
        if evento == "Trasformazione":
            # In questo caso, il parametro prodotto è l'id del prodotto che seleziono
            try:
                self.cur.execute("BEGIN TRANSACTION;")  # Inizio transazione

                # Inserisci l'operazione
                query = """
                INSERT INTO Operazione (Id_azienda, Id_prodotto, Data_operazione, Consumo_CO2,
                Operazione, Destinatario)
                VALUES (?, ?, ?, ?, ?, ?);
                """
                self.cur.execute(query, (
                    azienda, prodotto[0], data, co2, evento, destinatario))

                # Modifica lo stato del prodotto
                query_prodotto = """
                UPDATE Prodotto SET Stato = ? WHERE Id_prodotto = ?;
                """
                self.cur.execute(query_prodotto, (101, prodotto[0]))

                self.conn.commit()  # Conferma la transazione

            except sqlite3.Error as e:
                self.conn.rollback()  # Annulla tutto se c'è un errore
                raise Exception(f"Errore durante l'inserimento: {str(e)}")  # Lancia un'eccezione

        else:
            # In quest'altro caso, invece, il parametro prodotto è il nome del prodotto che seleziono.
            # Questo perché devo creare una nuova istanza di prodotto e mi serve il nome
            # (l'id nella tabella prodotto è autoincrement).
            try:
                self.cur.execute("BEGIN TRANSACTION;")  # Inizio transazione

                # Inserisci il prodotto
                query_prodotto = """
                INSERT INTO Prodotto (Nome, Quantita, Stato) VALUES (?, ?, ?);
                """
                self.cur.execute(query_prodotto, (prodotto, quantita, 10))

                prodotto_id = self.cur.lastrowid  # Ottieni l'ID del prodotto inserito

                # Inserisci l'operazione
                query_operazione = """
                INSERT INTO Operazione (Id_azienda, Id_prodotto, Data_operazione, Consumo_CO2,
                Operazione, Destinatario)
                VALUES (?, ?, ?, ?, ?, ?);
                """
                self.cur.execute(query_operazione, (
                    azienda, prodotto_id, data, co2, evento, destinatario))

                # Inserisci la composizione
                query_composizione = """
                INSERT INTO Composizione VALUES(?, ?)
                """
                # Modifica lo stato del prodotto
                query_stato = """
                UPDATE Prodotto SET Stato = ? WHERE Id_prodotto = ?;
                """
                self.cur.execute(query_composizione, (prodotto_id, prodotto_id))
                for mp in materie_prime:
                    self.cur.execute(query_composizione, (prodotto_id, mp))
                    self.cur.execute(query_stato, (110, mp))

                self.conn.commit()  # Conferma la transazione

            except sqlite3.Error as e:
                self.conn.rollback()  # Annulla tutto se c'è un errore
                raise Exception(f"Errore durante l'inserimento: {str(e)}")  # Lancia un'eccezione

    def inserisci_operazione_azienda_rivenditore(self, azienda, prodotto, data, co2, evento):
        try:
            self.cur.execute("BEGIN TRANSACTION;")  # Inizio transazione

            # Inserisci l'operazione
            query_operazione = """
            INSERT INTO Operazione (Id_azienda, Id_prodotto, Data_operazione, Consumo_CO2, Operazione)
            VALUES (?, ?, ?, ?, ?);
            """
            self.cur.execute(query_operazione, (azienda, prodotto, data, co2, evento))

            # Modifica lo stato del prodotto
            query_prodotto = """
            UPDATE Prodotto SET Stato = ? WHERE Id_prodotto = ?;
            """
            self.cur.execute(query_prodotto, (111, prodotto))

            self.conn.commit()  # Conferma la transazione

        except sqlite3.Error as e:
            self.conn.rollback()  # Annulla tutto se c'è un errore
            raise Exception(f"Errore durante l'inserimento: {str(e)}")  # Lancia un'eccezione

    # Questa funzione restituisce la soglia data l'operazione e il prodotto
    def get_soglia_by_operazione_and_prodotto(self, operazione, prodotto):
        query = """
        SELECT Soglia_Massima FROM Soglie WHERE Operazione = ? AND Prodotto = ?;
        """
        if not self.fetch_query(query, (operazione, prodotto)):
            print('non ce')
            return 999
        return self.fetch_query(query, (operazione, prodotto))[0][0]

    # Restituisce la lista di tutte le operazioni effettuate da una certa azienda
    def get_operazioni_by_azienda(self, azienda):
        query = """
        SELECT Operazione.Id_operazione, Prodotto.Id_prodotto, Prodotto.Nome, Prodotto.Quantita, 
        Operazione.Data_operazione, Operazione.Consumo_CO2, Operazione.Operazione
        FROM Operazione JOIN Prodotto
        ON Operazione.Id_prodotto = Prodotto.Id_prodotto
        WHERE Operazione.Id_azienda = ?;
        """
        return self.fetch_query(query, (azienda,))

    # Restituisce la lista di tutte le operazioni effettuate da una certa azienda filtrate per data
    def get_operazioni_by_data(self, azienda, d1, d2):
        query = """
        SELECT Operazione.Id_operazione, Prodotto.Id_prodotto, Prodotto.Nome, Prodotto.Quantita, Operazione.Data_operazione, Operazione.Consumo_CO2, Operazione.Operazione
        FROM Operazione JOIN Prodotto
        ON Operazione.Id_prodotto = Prodotto.Id_prodotto
        WHERE Operazione.Id_azienda = ?
        AND Operazione.Data_operazione BETWEEN ? AND ?;
        """
        return self.fetch_query(query, (azienda, d1, d2))

    # Restituisce la lista di tutte le operazioni effettuate da una certa azienda ordinate per co2 consumata
    def get_operazioni_ordinate_co2(self, azienda):
        query = """
        SELECT Operazione.Id_operazione, Prodotto.Id_prodotto, Prodotto.Nome, Prodotto.Quantita, Operazione.Data_operazione, Operazione.Consumo_CO2, Operazione.Operazione
        FROM Operazione JOIN Prodotto
        ON Operazione.Id_prodotto = Prodotto.Id_prodotto
        WHERE Operazione.Id_azienda = ?
        ORDER BY Operazione.Consumo_CO2 ASC;
        """
        return self.fetch_query(query, (azienda,))

    # Restituisce i prodotti con cui un trasformatore può fare la composizione
    def get_prodotti_to_composizione(self, azienda):
        query = """
        SELECT Id_prodotto, Nome, Quantita
        FROM Prodotto
        WHERE Stato != 110
        AND Id_prodotto IN (
            SELECT Id_prodotto
            FROM Operazione
            WHERE Id_azienda = ? AND Operazione = "Trasformazione"
        )
        """
        return self.fetch_query(query, (azienda,))

    # Restituisce la lista di destinatari
    def get_destinatari(self, tipo_mittente, destinazione):
        if tipo_mittente == "Agricola":
            query = "SELECT * FROM Azienda WHERE Tipo IN ('Trasportatore')"
        elif tipo_mittente == "Trasportatore":
            if destinazione == 'Azienda di trasformazione':
                query = "SELECT * FROM Azienda WHERE Tipo IN ('Trasformatore')"
            else:
                query = "SELECT * FROM Azienda WHERE Tipo IN ('Rivenditore')"
        elif tipo_mittente == "Trasformatore":
            query = "SELECT * FROM Azienda WHERE Tipo IN ('Trasportatore')"
        elif tipo_mittente == "Rivenditore":
            return ()
        else:
            return ()

        return self.fetch_query(query)

    def is_trasformatore(self, id_azienda):
        query = "SELECT Tipo FROM Azienda WHERE Id_azienda = ?"
        result = self.fetch_query(query, (id_azienda,))
        return result[0][0] == "Trasformatore" if result else False

    def get_stato_prodotto(self, id_prodotto):
        query = "SELECT Stato FROM Prodotto WHERE Id_prodotto = ?"
        result = self.fetch_query(query, (id_prodotto,))
        if not result:
            raise ValueError("Prodotto non trovato.")
        return result[0][0]

    def aggiorna_stato_prodotto(self, id_prodotto, nuovo_stato):
        query = "UPDATE Prodotto SET Stato = ? WHERE Id_prodotto = ?"
        self.execute_query(query, (nuovo_stato, id_prodotto))
    
    def close(self):
        self.conn.close()

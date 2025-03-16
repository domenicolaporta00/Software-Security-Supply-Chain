from off_chain.database_domenico.db_operations import Database, DuplicatedEntryError


class ControllerAzienda:
    def __init__(self):
        self.database = Database()

    # Restituisce tutte le soglie
    def lista_soglie(self):
        lista_soglie = self.database.get_lista_soglie()
        return lista_soglie

    # Restituisce il dettaglio della soglia selezionata dato l'indice n
    def get_dettaglio_soglia(self, n):
        pass

    # Restituisce il dettaglio della co2/il numero di certificati della sua azienda
    def get_dettaglio_azienda(self, id_azienda):
        return self.database.get_azienda_by_id(id_azienda)

    # Restituisce i dati anagrafici dell'azienda
    def get_anagrafica_azienda(self, id_azienda):
        azienda = self.database.get_anagrafica_azienda(id_azienda)
        return azienda

    # Restituisce la lista di tutte le azioni compensative della sua azienda
    def lista_azioni_compensative(self, azienda):
        lista_azioni_compensative = self.database.get_lista_azioni(azienda)
        return lista_azioni_compensative

    # Restituisce la lista delle sue azioni compensative filtrate per data
    def lista_azioni_per_data(self, azienda, d1, d2):
        lista_azioni_per_data = self.database.get_lista_azioni_per_data(azienda, d1, d2)
        return lista_azioni_per_data

    # Restituisce la lista di tutte le azioni compensative della sua azienda
    def lista_azioni_compensative_ordinata(self, azienda):
        lista_azioni_compensative = self.database.get_lista_azioni_ordinata(azienda)
        return lista_azioni_compensative

    # Restituisce il dettaglio dell'azione compensativa selezionata
    # dato l'indice n e la lista (filtrata o meno)
    def get_dettaglio_azione(self, n, lista):
        pass

    # Aggiunge un'azione compensativa
    def aggiungi_azione(self, data, azienda, co2_compensata, nome_azione):
        self.database.inserisci_azione(data, azienda, co2_compensata, nome_azione)

    # Restituisce la lista di tutte le operazioni della sua azienda
    def lista_operazioni(self, azienda):
        lista_operazioni = self.database.get_operazioni_by_azienda(azienda)
        return lista_operazioni

    # Restituisce la lista delle sue operazioni filtrate per data
    def lista_operazioni_per_data(self, azienda, d1, d2):
        lista_operazioni = self.database.get_operazioni_by_data(azienda, d1, d2)
        return lista_operazioni

    def lista_operazioni_ordinata_co2(self, azienda):
        lista_operazioni = self.database.get_operazioni_ordinate_co2(azienda)
        return lista_operazioni

    # Restituisce il dettaglio dell'operazione selezionata dato l'indice n e la lista (filtrata o meno)
    def get_dettaglio_operazione(self, n, lista):
        pass

    # Restituisce la lista dei destinatari
    def get_destinatari(self, tipo_mittente, destinazione):
        lista_destinatari = self.database.get_destinatari(tipo_mittente, destinazione)
        return lista_destinatari

    # Restituisce gli elementi da visualizzare nella combo box
    def elementi_combo_box(self, azienda, operazione, destinatario='', id_azienda=0):
        if azienda == "Agricola":
            return self.database.get_prodotti_to_azienda_agricola()
        elif azienda == "Trasportatore":
            return self.database.get_prodotti_to_azienda_trasporto(destinatario, id_azienda)
        elif azienda == "Trasformatore":
            return self.database.get_prodotti_to_azienda_trasformazione(operazione, id_azienda)
        elif azienda == "Rivenditore":
            return self.database.get_prodotti_to_rivenditore(id_azienda)

    # Verifica la password dell'azienda
    def verify_password(self, id_azienda, password):
        """Verifica se la password fornita corrisponde a quella memorizzata per l'azienda"""
        return self.database.verify_password(id_azienda, password)

    # Aggiunge un'operazione
    def aggiungi_operazione(
        self, tipo_azienda, azienda, prodotto, data, co2, evento,
        quantita='', destinatario=0, materie_prime=None, password=None):
        
        # Verifica la password prima di procedere
        if password is None:
            return False, "Password richiesta per questa operazione."
            
        if not self.verify_password(azienda, password):
            return False, "Password non corretta. Operazione annullata."
        
        try:
            # Recupera lo stato attuale del prodotto
            stato_attuale = self.database.get_stato_prodotto(prodotto)
            nuovo_stato = None  # Initialize to avoid reference before assignment

            # **1️⃣ Produzione (Azienda Agricola)**
            if tipo_azienda == "Agricola":
                nuovo_stato = 0  # Stato iniziale
                self.database.inserisci_operazione_azienda_agricola(
                    prodotto, quantita, azienda, data, co2, evento, destinatario
                )

            # **2️⃣ Trasporto**
            elif tipo_azienda == "Trasportatore":
                if stato_attuale == 0:
                    # Se il destinatario è un **trasformatore**, metti stato a 1, altrimenti a 3
                    nuovo_stato = 1 if self.database.is_trasformatore(destinatario) else 3  
                elif stato_attuale == 2:
                    # Se trasporta un prodotto trasformato, va al rivenditore con stato 3
                    nuovo_stato = 3
                else:
                    raise ValueError("Operazione di trasporto non valida per lo stato attuale.")

                self.database.inserisci_operazione_azienda_trasporto(
                    azienda, prodotto, data, co2, evento, nuovo_stato, destinatario
                )

            # **3️⃣ Trasformazione (Azienda Trasformatrice)**
            elif tipo_azienda == "Trasformatore":
                if stato_attuale == 1:
                    nuovo_stato = 2  # Il prodotto è stato trasformato
                    self.database.inserisci_operazione_azienda_trasformazione(
                        azienda, prodotto, data, co2, evento, destinatario, int(quantita) if quantita else 0, materie_prime
                    )
                else:
                    raise ValueError("Il prodotto non può essere trasformato dallo stato attuale.")

            # **4️⃣ Messa in vendita (Azienda Rivenditore)**
            elif tipo_azienda == "Rivenditore":
                if stato_attuale == 3:
                    nuovo_stato = 4  # Prodotto messo in vendita
                    self.database.inserisci_operazione_azienda_rivenditore(
                        azienda, prodotto, data, co2, evento
                    )
                else:
                    raise ValueError("Il prodotto non può essere messo in vendita dallo stato attuale.")
            else:
                raise ValueError(f"Tipo di azienda non valido: {tipo_azienda}")

            # Verify nuovo_stato is set
            if nuovo_stato is None:
                raise ValueError("Stato del prodotto non determinato.")

            # **Aggiornamento dello stato del prodotto**
            self.database.aggiorna_stato_prodotto(prodotto, nuovo_stato)
            
            return True, "Operazione aggiunta con successo."
        except Exception as e:
            return False, f"Errore durante l'aggiunta dell'operazione: {str(e)}"

    # Restituisce le opzioni per la combo box del dialog per la composizione
    def get_prodotti_to_composizione(self, id_azienda):
        lista = self.database.get_prodotti_to_composizione(id_azienda)
        return lista

    # Restituisce lo scarto dalla soglia di riferimento
    def scarto_soglia(self, co2, operazione, prodotto):
        soglia = self.database.get_soglia_by_operazione_and_prodotto(operazione, prodotto)
        return soglia - float(co2)

    # Modifica i dati dell'azienda in base all'id
    def modifica_dati_azienda(self, id_azienda, nuova_email, nuovo_indirizzo):
        try:
            self.database.modifica_dati_azienda(id_azienda, nuova_email, nuovo_indirizzo)
            return True, "Dati modificati correttamente!"
        except DuplicatedEntryError:
            return False, "L'email o l'indirizzo sono già in uso!"
        except Exception as e:
            return False, f"Errore sconosciuto: {str(e)}"

    def modifica_password(self, id_azienda, vecchia_password, nuova_password):
        """Interfaccia per modificare la password di un'azienda"""
        try:
            self.database.modifica_password(id_azienda, vecchia_password, nuova_password)
            return True, "Password modificata con successo!"
        except ValueError as e:
            return False, str(e)
        except Exception:
            return False, "Errore durante la modifica della password."

    def recupera_password(self, id_azienda):
        password = self.database.get_password(id_azienda)
        return password


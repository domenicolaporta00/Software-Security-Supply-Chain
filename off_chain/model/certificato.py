from off_chain.model.base_model import BaseModel

class Certificato(BaseModel):
    """Model representing a Certificato (Certificate) in the system.
    
    Attributes:
        id_certificato (int): The certificate ID.
        id_prodotto (int): The product ID associated with this certificate.
        descrizione (str): The certificate description.
        id_azienda_certificatore (int): The certifier company ID.
        data (str): The timestamp when the certificate was issued.
    """
    
    def __init__(self, id_certificato=None, id_prodotto=None, descrizione=None, 
                 id_azienda_certificatore=None, data=None):
        """Initialize a Certificato instance.
        
        Args:
            id_certificato (int, optional): The certificate ID.
            id_prodotto (int, optional): The product ID associated with this certificate.
            descrizione (str, optional): The certificate description.
            id_azienda_certificatore (int, optional): The certifier company ID.
            data (str, optional): The timestamp when the certificate was issued.
        """
        super().__init__(
            id_certificato=id_certificato,
            id_prodotto=id_prodotto,
            descrizione=descrizione,
            id_azienda_certificatore=id_azienda_certificatore,
            data=data
        )
    
    def validate(self):
        """Validate the Certificato attributes.
        
        Returns:
            bool: True if the Certificato is valid, False otherwise.
        
        Raises:
            ValueError: If any of the attributes are invalid.
        """
        if not getattr(self, 'id_prodotto', None):
            raise ValueError("Product ID cannot be empty")
        
        if not getattr(self, 'id_azienda_certificatore', None):
            raise ValueError("Certifier company ID cannot be empty")
        
        return True
    
    @classmethod
    def from_tuple(cls, data):
        """Create a Certificato instance from a database tuple.
        
        Args:
            data (tuple): Tuple containing (id_certificato, nome_prodotto, descrizione, nome_azienda, data).
            
        Returns:
            Certificato: An instance of Certificato with partial information.
        """
        if len(data) >= 5:
            return cls(
                id_certificato=data[0],
                # Note: This doesn't include id_prodotto and id_azienda_certificatore
                # as they're not directly in the query result
                descrizione=data[2],
                data=data[4]
            )
        return None
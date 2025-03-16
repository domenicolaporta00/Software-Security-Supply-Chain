from off_chain.model.base_model import BaseModel

class Prodotto(BaseModel):
    """Model representing a Prodotto (Product) in the system.
    
    Attributes:
        id_prodotto (int): The product ID.
        nome (str): The product name.
        quantita (float): The product quantity.
        stato (int): The product state (0-4 representing different stages in the supply chain).
        data_di_inserimento (str): The timestamp when the product was inserted.
    """
    
    # Product states
    STATO_INIZIALE = 0  # Initial state (produced by agricultural company)
    STATO_TRASPORTATO_A_TRASFORMATORE = 1  # Transported to transformer
    STATO_TRASFORMATO = 2  # Transformed
    STATO_TRASPORTATO_A_RIVENDITORE = 3  # Transported to retailer
    STATO_IN_VENDITA = 4  # On sale
    
    def __init__(self, id_prodotto=None, nome=None, quantita=None, stato=None, data_di_inserimento=None):
        """Initialize a Prodotto instance.
        
        Args:
            id_prodotto (int, optional): The product ID.
            nome (str, optional): The product name.
            quantita (float, optional): The product quantity.
            stato (int, optional): The product state.
            data_di_inserimento (str, optional): The timestamp when the product was inserted.
        """
        super().__init__(
            id_prodotto=id_prodotto,
            nome=nome,
            quantita=quantita,
            stato=stato,
            data_di_inserimento=data_di_inserimento
        )
    
    def validate(self):
        """Validate the Prodotto attributes.
        
        Returns:
            bool: True if the Prodotto is valid, False otherwise.
        
        Raises:
            ValueError: If any of the attributes are invalid.
        """
        if not getattr(self, 'nome', None):
            raise ValueError("Product name cannot be empty")
        
        quantita = getattr(self, 'quantita', None)
        if quantita is not None and quantita < 0:
            raise ValueError("Product quantity cannot be negative")
        
        stato = getattr(self, 'stato', None)
        if stato is not None and not (0 <= stato <= 4):
            raise ValueError("Product state must be between 0 and 4")
        
        return True
    
    @classmethod
    def from_tuple(cls, data):
        """Create a Prodotto instance from a database tuple.
        
        Args:
            data (tuple): Tuple containing (id_prodotto, nome, quantita, stato, data_di_inserimento).
            
        Returns:
            Prodotto: An instance of Prodotto.
        """
        if len(data) >= 4:
            return cls(
                id_prodotto=data[0],
                nome=data[1],
                quantita=data[2],
                stato=data[3],
                data_di_inserimento=data[4] if len(data) > 4 else None
            )
        return None
from off_chain.model.base_model import BaseModel

class Operazione(BaseModel):
    """Model representing an Operazione (Operation) in the system.
    
    Attributes:
        id_operazione (int): The operation ID.
        id_azienda (int): The company ID that performed the operation.
        id_prodotto (int): The product ID involved in the operation.
        data_operazione (str): The timestamp when the operation was performed.
        consumo_co2 (float): The CO2 consumption of the operation.
        operazione (str): The type of operation performed.
    """
    
    def __init__(self, id_operazione=None, id_azienda=None, id_prodotto=None, 
                 data_operazione=None, consumo_co2=None, operazione=None):
        """Initialize an Operazione instance.
        
        Args:
            id_operazione (int, optional): The operation ID.
            id_azienda (int, optional): The company ID that performed the operation.
            id_prodotto (int, optional): The product ID involved in the operation.
            data_operazione (str, optional): The timestamp when the operation was performed.
            consumo_co2 (float, optional): The CO2 consumption of the operation.
            operazione (str, optional): The type of operation performed.
        """
        super().__init__(
            id_operazione=id_operazione,
            id_azienda=id_azienda,
            id_prodotto=id_prodotto,
            data_operazione=data_operazione,
            consumo_co2=consumo_co2,
            operazione=operazione
        )
    
    def validate(self):
        """Validate the Operazione attributes.
        
        Returns:
            bool: True if the Operazione is valid, False otherwise.
        
        Raises:
            ValueError: If any of the attributes are invalid.
        """
        if not getattr(self, 'id_azienda', None):
            raise ValueError("Company ID cannot be empty")
        
        if not getattr(self, 'id_prodotto', None):
            raise ValueError("Product ID cannot be empty")
        
        consumo_co2 = getattr(self, 'consumo_co2', None)
        if consumo_co2 is not None and consumo_co2 < 0:
            raise ValueError("CO2 consumption cannot be negative")
        
        if not getattr(self, 'operazione', None):
            raise ValueError("Operation type cannot be empty")
        
        return True
    
    @classmethod
    def from_tuple(cls, data):
        """Create an Operazione instance from a database tuple.
        
        Args:
            data (tuple): Tuple containing (id_operazione, id_azienda, id_prodotto, data_operazione, consumo_co2, operazione).
            
        Returns:
            Operazione: An instance of Operazione.
        """
        if len(data) >= 6:
            return cls(
                id_operazione=data[0],
                id_azienda=data[1],
                id_prodotto=data[2],
                data_operazione=data[3],
                consumo_co2=data[4],
                operazione=data[5]
            )
        return None
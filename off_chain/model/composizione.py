from off_chain.model.base_model import BaseModel

class Composizione(BaseModel):
    """Model representing a Composizione (Composition) in the system.
    
    Attributes:
        prodotto (int): The product ID.
        materia_prima (int): The raw material product ID.
    """
    
    def __init__(self, prodotto=None, materia_prima=None):
        """Initialize a Composizione instance.
        
        Args:
            prodotto (int, optional): The product ID.
            materia_prima (int, optional): The raw material product ID.
        """
        super().__init__(
            prodotto=prodotto,
            materia_prima=materia_prima
        )
    
    def validate(self):
        """Validate the Composizione attributes.
        
        Returns:
            bool: True if the Composizione is valid, False otherwise.
        
        Raises:
            ValueError: If any of the attributes are invalid.
        """
        if not getattr(self, 'prodotto', None):
            raise ValueError("Product ID cannot be empty")
        
        if not getattr(self, 'materia_prima', None):
            raise ValueError("Raw material ID cannot be empty")
        
        if getattr(self, 'prodotto') == getattr(self, 'materia_prima'):
            raise ValueError("Product cannot be its own raw material")
        
        return True
    
    @classmethod
    def from_tuple(cls, data):
        """Create a Composizione instance from a database tuple.
        
        Args:
            data (tuple): Tuple containing (prodotto, materia_prima).
            
        Returns:
            Composizione: An instance of Composizione.
        """
        if len(data) >= 2:
            return cls(
                prodotto=data[0],
                materia_prima=data[1]
            )
        return None
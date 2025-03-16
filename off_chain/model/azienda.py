from off_chain.model.base_model import BaseModel
import re  # Add this import for regex-based email validation

class Azienda(BaseModel):
    """Model representing an Azienda (Company) in the system.
    
    Attributes:
        id_azienda (int): The company ID.
        id_credenziali (int): The credentials ID associated with this company.
        tipo (str): The company type (Agricola, Trasportatore, Trasformatore, Rivenditore, Certificatore).
        nome (str): The company name.
        indirizzo (str): The company address.
        email (str): The company email address.
        created_at (str): The timestamp when the company was created.
    """
    
    VALID_TYPES = ['Agricola', 'Trasportatore', 'Trasformatore', 'Rivenditore', 'Certificatore']
    
    def __init__(self, id_azienda=None, id_credenziali=None, tipo=None, nome=None, indirizzo=None, email=None, created_at=None):
        """Initialize an Azienda instance.
        
        Args:
            id_azienda (int, optional): The company ID.
            id_credenziali (int, optional): The credentials ID associated with this company.
            tipo (str, optional): The company type.
            nome (str, optional): The company name.
            indirizzo (str, optional): The company address.
            email (str, optional): The company email address.
            created_at (str, optional): The timestamp when the company was created.
        """
        super().__init__(
            id_azienda=id_azienda,
            id_credenziali=id_credenziali,
            tipo=tipo,
            nome=nome,
            indirizzo=indirizzo,
            email=email,
            created_at=created_at
        )
    
    def validate(self):
        """Validate the Azienda attributes.
        
        Returns:
            bool: True if the Azienda is valid, False otherwise.
        
        Raises:
            ValueError: If any of the attributes are invalid.
        """
        if hasattr(self, 'tipo') and getattr(self, 'tipo') and getattr(self, 'tipo') not in self.VALID_TYPES:
            raise ValueError(f"Invalid company type: {getattr(self, 'tipo')}. Must be one of {self.VALID_TYPES}")
        
        if not hasattr(self, 'nome') or not getattr(self, 'nome'):
            raise ValueError("Company name cannot be empty")
        
        if not hasattr(self, 'indirizzo') or not getattr(self, 'indirizzo'):
            raise ValueError("Company address cannot be empty")
        
        if hasattr(self, 'email') and getattr(self, 'email'):
            email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
            if not email_pattern.match(getattr(self, 'email')):
                raise ValueError("Invalid email format")
        
        return True
    
    @classmethod
    def from_tuple(cls, data):
        """Create an Azienda instance from a database tuple.
        
        Args:
            data (tuple): Tuple containing (id_azienda, tipo, indirizzo, nome, email).
            
        Returns:
            Azienda: An instance of Azienda.
        """
        if len(data) >= 5:
            return cls(
                id_azienda=data[0],
                tipo=data[1],
                indirizzo=data[2],
                nome=data[3],
                email=data[4] if len(data) > 4 else None
            )
        elif len(data) >= 4:
            return cls(
                id_azienda=data[0],
                tipo=data[1],
                indirizzo=data[2],
                nome=data[3]
            )
        return None
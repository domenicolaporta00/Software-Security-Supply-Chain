from off_chain.model.base_model import BaseModel

class AzioneCompensativa(BaseModel):
    """Model representing an Azione Compensativa (Compensatory Action) in the system.
    
    Attributes:
        id_azione (int): The action ID.
        data (str): The timestamp when the action was performed.
        id_azienda (int): The company ID that performed the action.
        co2_compensata (float): The amount of CO2 compensated.
        nome_azione (str): The name of the compensatory action.
    """
    
    def __init__(self, id_azione=None, data=None, id_azienda=None, co2_compensata=None, nome_azione=None):
        """Initialize an AzioneCompensativa instance.
        
        Args:
            id_azione (int, optional): The action ID.
            data (str, optional): The timestamp when the action was performed.
            id_azienda (int, optional): The company ID that performed the action.
            co2_compensata (float, optional): The amount of CO2 compensated.
            nome_azione (str, optional): The name of the compensatory action.
        """
        super().__init__(
            id_azione=id_azione,
            data=data,
            id_azienda=id_azienda,
            co2_compensata=co2_compensata,
            nome_azione=nome_azione
        )
    
    def validate(self):
        """Validate the AzioneCompensativa attributes.
        
        Returns:
            bool: True if the AzioneCompensativa is valid, False otherwise.
        
        Raises:
            ValueError: If any of the attributes are invalid.
        """
        id_azienda = getattr(self, 'id_azienda', None)
        if not id_azienda or not isinstance(id_azienda, int) or id_azienda <= 0:
            raise ValueError("Company ID must be a positive integer")
        
        co2_compensata = getattr(self, 'co2_compensata', None)
        if co2_compensata is not None:
            if not isinstance(co2_compensata, (int, float)):
                raise ValueError("CO2 compensation must be a number")
            if co2_compensata <= 0:
                raise ValueError("CO2 compensation must be positive")
        
        nome_azione = getattr(self, 'nome_azione', None)
        if not nome_azione or not isinstance(nome_azione, str) or not nome_azione.strip():
            raise ValueError("Action name must be a non-empty string")
        
        data = getattr(self, 'data', None)
        if data is not None and not isinstance(data, str):
            raise ValueError("Date must be a string")
            
        return True
    
    @classmethod
    def from_tuple(cls, data):
        """Create an AzioneCompensativa instance from a database tuple.
        
        Args:
            data (tuple): Tuple containing (id_azione, data, id_azienda, co2_compensata, nome_azione).
            
        Returns:
            AzioneCompensativa: An instance of AzioneCompensativa.
        """
        if len(data) >= 5:
            return cls(
                id_azione=data[0],
                data=data[1],
                id_azienda=data[2],
                co2_compensata=data[3],
                nome_azione=data[4]
            )
        return None
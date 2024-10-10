from enum import Enum


class ActionSpot(Enum):
    BUY = 0    # Action to purchase the stock or asset
    SELL = 1   # Action to sell the stock or asset
    HOLD = 2   # Action to maintain the current position without buying or selling
    CUT = 3    # Action to reduce the position, possibly to minimize losses
    PLUS = 4   # Action to increase the position, potentially to capitalize on gains

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @classmethod
    def _missing_(cls, value):
        """
        Override the _missing_ method to handle string inputs.
        This allows instantiation using the member name as a string.
        
        Args:
            value: The value used to instantiate the Enum.
        
        Returns:
            The corresponding Enum member if a match is found.
        
        Raises:
            ValueError: If no matching member is found.
        """
        if isinstance(value, str):
            try:
                # Attempt to return the member matching the provided name
                return cls[value.upper()]
            except KeyError:
                pass  # If no matching member is found, proceed to raise ValueError
        # If not a string or no match found, defer to the superclass implementation
        return super()._missing_(value)


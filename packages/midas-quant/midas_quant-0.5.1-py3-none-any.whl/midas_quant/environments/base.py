from enum import Enum


class ActionSpot(Enum):
    BUY = 0    # Action to purchase the stock or asset
    SELL = 1   # Action to sell the stock or asset
    HOLD = 2   # Action to maintain the current position without buying or selling
    CUT = 3    # Action to reduce the position, possibly to minimize losses
    PLUS = 4   # Action to increase the position, potentially to capitalize on gains

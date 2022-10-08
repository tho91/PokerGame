# Player / Bot management file

class Player():
  """
    Class manages players in game as objects
  """

  def __init__(self, howMany, xCoord, yCoord):
    """
    contruct a player object
    param: 
    howMany: int : number of cards the player can have
    xCoord: int : the x coordinate to draw the card
    yCoord: int : the y coordinate to draw the card
    """
    self._xCoord = xCoord
    self._yCoord = yCoord
    self._handSize = howMany
    self._cardHand = []

  def getX(self):
    """
    get the x coordinate
    return: int:  the x coordinate
    """
    return self._xCoord

  def getY(self):
    """
    get the y coordinate
    return: int :the y coordinate
    """
    return self._yCoord

  def getHandSize(self):
    """
    get the number of card on player hand
    return: int:  the number of card on player hand
    """
    return self._handSize

  def getCards(self):
    """
    get the list of the card on player hand
    return: int:  the list of the card on player hand
    """
    return self._cardHand

  def setCards(self, cardList):
    """
    manually give a player a hand
    """
    self._cardHand = cardList

    

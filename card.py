#Card class file
from gamebase import ImageSprite

CARDS_TOTAL = 10
CARDSIZE_X = 83
CARDSIZE_Y = 97

class Card(ImageSprite):
    """
    Class manages card images, value and position
    """
    
    def __init__(self, x, y, dir):
        '''
        Initializes Card to a random .gif
        _layer = int, layer of sprite
        _dirFront = "" dir of image of front card
        _dirBack = "", dir of image of back card
        _face = "", determines card facings named either "Front" or "Back"
        _x = int, x value of card placement
        _y = int, y value of card placement
        _suit = "", suit of the card
        _rank = int, rank of the card
        '''
        self._layer = 1
        self._dirFront = dir
        self._dirBack = 'DECK/b.gif'
        self._face = "Front"
        self._x = x
        self._y = y
        super().__init__(x, y, self._dirFront)
        # initialize the sprite obj to be the random .gif
        name = str(dir)
        # name.removesuffix('.gif')
        # name.removeprefix('DECK/')
        # name.replace('.gif', '')
        name = name[5:]
      
        # Truncate name of file to just rank and suits
        if len(name) == 7:
            self._suit = name[2]
            self._rank = int(name[:2])
        else:
            self._suit = name[1]
            self._rank = int(name[0])


    def flip(self):
      """
      flip the card back and forth
      
      """
        # flip card face to front if back, back if front
      if self._face == "Front":
          self._face = ("Back")
          super().__init__(self._x, self._y, self._dirBack)
      else:
          self._face = "Front"
          super().__init__(self._x, self._y, self._dirFront)

    def get_suit(self):
      """
      get the string suit character
      return a suit string
      """
      return self._suit

    def get_rank(self):
      """
      get the integer value of rank
      return the rank value
      """
      return self._rank
    
    def set_rank(self, rank):
      """
      set the rank value to the card
      """
      self._rank = int(rank)

    def __repr__(self):
      """
      print the string name of the card object
      """
      return self._dirFront

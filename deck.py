# Card deck file

import random
from card import Card
from datetime import datetime

CARDS_TOTAL = 10
CARDSIZE_X = 83
CARDSIZE_Y = 97

class Deck():
    """
    Create a deck of card and deal cards and draw cards
    """
    def __init__(self):
        """
        Construct the deck of cards
        """
        self._directs = []  # All 52 cards
        self._centerCards = []  # the cards in the middle (face-up)
        self._drawnCards = []  # blacklist
        
        # Create whole deck of 52 cards
        for suit in ['c', 'd', 'h', 's']:
            for i in range(2, 15):
                dir = "DECK/" + str(i) + suit + ".gif"
                # adding card to deck
                self._directs.append(dir)

        #class variable for cards placement    
        self._width = 800
        self._height = 600

        #random generator
        random.seed(datetime.now())

    def dealFlop(self):
      """
      display the 3 cards in the middle
      """
      # Place 3 cards in the center, face up
      centerX = self._width / 2 - (CARDSIZE_X * 2) + 150
      centerY = self._height / 2 + 50
      centerCards = 3
      self.drawHands(centerCards, centerX, centerY, self._centerCards)

    def drawHands(self, howMany, setX, setY, cardList, flipOver=False):
      """
      draw the cards
      param:
      howMany: int : number of card to draw
      setX: int : x coordinate to draw
      setY: int : y coordinate to draw
      cardList: list: the list of the card to draw
      flipOver: boolean : the flag to check if the card is face up or down
      """
      # get a random card from the deck and give to hand of player or bot
      for i in range(howMany):
          if len(self._directs) == 0:  # Keep for debugging purposes
              print("NO MORE CARDS!!!!!")
              return

          # Assume first card in top of deck is shuffled, and is picked as random card value
          randCard = self._directs[0]

          # take the first card of the randomized deck
          # add card to table
          card = Card(setX + (i * CARDSIZE_X), setY, randCard)
          if flipOver:
              card.flip()
          cardList.append(card)

          # take out the used dir
          self._directs.pop(0)

          # add the used to the used cards list
          self._drawnCards.append(randCard)
            
    # Basically draw_hands but for the center, adds + 1 card to center
    def addToCenter(self):
      """
      add 1 more care to the middle after deal flop

      """
      # Place 3 cards in the center, face up
      centerX = self._width / 2 - (CARDSIZE_X * 2) + 150
      centerY = self._height / 2 + 50

      randCard = self._directs[0]
      # take the first card of the randomized deck
      # add card to table
      card = Card(centerX + (len(self._centerCards) * CARDSIZE_X), centerY, randCard)

      # Add to centerCards for rendering to the pile
      self._centerCards.append(card)

      # take out the used dir
      self._directs.pop(0)

      # add the used to the used cards list
      self._drawnCards.append(randCard)

    def getCenterCards(self):
      """
      get the list of the cards in the middle
      return: list : the list of the cards in the middle
      """
      return self._centerCards
    
    def getDirectCards(self):
      """
      get the string of name of the card
      return: string : name of the cards
      """
      return self._directs
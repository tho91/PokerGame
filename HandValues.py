#HandValue file

class HandValues():
  """
  Handle the calculation for the cards in hands
  """
  
  def __init__(self, cards):
    """
    contruct the handvalue object to calculate the hand
    param:
    cards: list : the list of 7 cards from the game
    """

    # sort cards by the rank from low to high
    self.cards = self.sortCards(cards[:])
    self._handValue = 0
    self._rankTotal = 0
  

  def checkHand(self):
    """
    check the handvalue from highest to lowest and set the value for the hands by calling all other method to check the poker hand and return the value
    return: int:  the value of the hand 
    """

    if self.royalFlush():
      self._handValue += 10000
      print("ITS A ROYALFLUSH")

    elif self.straightFlush():
      self._handValue += self._rankTotal + 8000
      print("ITS A SRAIGHTFLUSH")
 
    elif self.fourKind():
      self._handValue = self._rankTotal + 7000
      print("ITS A FOUR OF A KIND")

    elif self.fullHouse():
      self._handValue = self._rankTotal + 6000
      print("ITS A FULLHOUSE")
      
    elif self.flush():
      self._handValue = self._rankTotal + 5000
      print("ITS A FLUSH")
      
    elif self.straight():
      self._handValue = self._rankTotal + 4000
      print("ITS A STRAIGHT")

    elif self.threeKind():
      self._handValue = self._rankTotal + 3000
      print("ITS A THREE OF A KIND")
   
    elif self.twoPair():
      self._handValue = self._rankTotal + 2000
      print("ITS A TWO PAIR")
   
    elif self.pair():
      self._handValue = self._rankTotal + 1000
      print("ITS A PAIR")

    elif self.highCard():
      self._handValue = self._rankTotal + 200
      print("ITS A HIGH CARD")

    return self._handValue


  def royalFlush(self):
    """
    check if the hand is royal flush
    return: boolean
    """
    # check if the hands is straight flush and the last card is Ace
    # remove duplicates as RF may have dupe in hand, took code from straight()
    cardsCopy = self.cards[:] # copy over list
    handLen = len(cardsCopy)
    for i in range(handLen):
      # 0 - cardhand
      if i < handLen:
        for j in range(handLen):
          # 0 - card hand again to compare
          if j < handLen:
            if i != j and cardsCopy[i].get_rank() == cardsCopy[j].get_rank():
              cardsCopy.pop(j)
              handLen = handLen - 1

    # Check if it has preceding qualities of straightflush already
    # and the ends are the absolute highest cards
    if self.straightFlush() and cardsCopy[len(cardsCopy)-1].get_rank() == 14 \
      and cardsCopy[len(cardsCopy)-2].get_rank() == 13 \
      and cardsCopy[len(cardsCopy)-3].get_rank() == 12:
      return True
    return False


  def straightFlush(self):
    """
    check if the hand is straight flush
    return: boolean
    """
    # create list for cards that have the same suit
    h = []
    c = []
    d = []
    s = []
    suitList = []
    straightFlush = False

    # check same-suit
    for i in range(len(self.cards)):
      # create a new card var and add it to correct list
      if self.cards[i].get_suit() == "h":
          h.append(self.cards[i])
      if self.cards[i].get_suit() == "c":
          c.append(self.cards[i])
      if self.cards[i].get_suit() == "d":
          d.append(self.cards[i])
      if self.cards[i].get_suit() == "s":
          s.append(self.cards[i])

    # create a temp list for suit that have more than 5 
    if len(h) >=5:   
      suitList = h[:]
    elif len(c) >=5:   
      suitList = c[:]
    elif len(d) >=5:   
      suitList = d[:]
    elif len(s) >=5:
      suitList = s[:]
    
    #special case for Ace 2 3 4 5
    #A = 14, so A is always the last cards in the list
    #while 2 3 4 5 shoud be the first 4 cards in the list
    if len(suitList) > 0:
      if suitList[len(suitList)-1].get_rank() == 14 \
      and suitList[0].get_rank() == 2 \
      and suitList[1].get_rank() == 3 \
      and suitList[2].get_rank() == 4 \
      and suitList[3].get_rank() == 5:
        #set the value of the hand to the lowest rank value
        self._rankTotal = 5
        return True

    # if flush does exist, then check for straight
    for i in range(len(suitList)-4):
        if suitList[i].get_rank() + 1 == suitList[i+1].get_rank() \
        and suitList[i+1].get_rank() + 1 == suitList[i+2].get_rank() \
        and suitList[i+2].get_rank() + 1 == suitList[i+3].get_rank() \
        and suitList[i+3].get_rank() + 1 == suitList[i+4].get_rank():
          self._rankTotal = suitList[i+4].get_rank() 
          straightFlush = True
    return straightFlush


  def fourKind(self):
    """
    check if the hand is four of a kind
    return: boolean
    """
    #loop through the hands from index 0 to 3
    #check if the rank of 4 consecutive cards is the same
    for i in range(len(self.cards)-3):
      if self.cards[i].get_rank() == self.cards[i+1].get_rank() == self.cards[i+2].get_rank() == self.cards[i+3].get_rank():
        num = self.cards[i].get_rank()
        self._rankTotal = num * 4
        return True
    return False


  def fullHouse(self):
    """
    check if the hand is full house
    return: boolean
    """
    #check if the hand has 2 pair and 3 of a kind
    if self.twoPair() and self.threeKind():
      #use multiplyer to increase the value of 3 kinds
      #in case the hand has high pair
      # Example: 5 5 5 2 2 > 4 4 4 A A but ranktotal = 19 < 40
      self._rankTotal += (self.threeKindvalue * 3) + (self.twoPairValue - (int(self.threeKindvalue * 2/3)))
      return True
    else:
      return False
    

  def flush(self):
    """
    check if the hand is flush
    return: boolean
    """
    # create a counter for suit
    h = 0
    c = 0
    d = 0
    s = 0
    
    # locals don't work on replit so we gotta cope without DRY principles
    conditionMet = False
    for i in range(len(self.cards)):
      # print("FLUSH SUITS", h, c, d, s)
      if self.cards[i].get_suit() == "h":
          h += 1
      if self.cards[i].get_suit() == "c":
          c += 1
      if self.cards[i].get_suit() == "d":
          d += 1
      if self.cards[i].get_suit() == "s":
          s += 1

      # if any of the suits have 5 cards
      if h == 5 or c == 5 or d == 5 or s == 5:
        # remove a suit card in case there are more than 5 suited cards to get the highest rank suit
        self._rankTotal = self.cards[i].get_rank()
        if self.cards[i].get_suit() == "h":
            h -= 1
        if self.cards[i].get_suit() == "c":
            c -= 1
        if self.cards[i].get_suit() == "d":
            d -= 1
        if self.cards[i].get_suit() == "s":
            s -= 1
        conditionMet = True
    return conditionMet
      

  def straight(self):
    """
    check if the hand is straight
    return: boolean
    """
    # for straight, remove dupes into a cloned list and check
    cardsCopy = self.cards[:] # copy over list
    handLen = len(cardsCopy)
    for i in range(handLen):
      # 0 - cardhand
      if i < handLen:
        for j in range(handLen):
          # 0 - card hand again to compare
          if j < handLen:

            #compare 2 different cards
            if i != j and cardsCopy[i].get_rank() == cardsCopy[j].get_rank():

              #remove duplicate cards
              cardsCopy.pop(j)
              handLen = handLen - 1

    #  A, 2, 2, 3, 4, 5, 8 
    #special case for Ace 2 3 4 5
    if cardsCopy[len(cardsCopy)-1].get_rank() == 14 \
    and cardsCopy[0].get_rank() == 2 \
    and cardsCopy[1].get_rank() == 3 \
    and cardsCopy[2].get_rank() == 4 \
    and cardsCopy[3].get_rank() == 5:
      self._rankTotal = 5
      return True

    #loop through index 0 to 2
    #check if the rank of 5 consecutive cards increase by 1
    isStraight = False
    for i in range(len(cardsCopy)-4):
      if cardsCopy[i].get_rank() + 1 == cardsCopy[i+1].get_rank() \
      and cardsCopy[i+1].get_rank() + 1 == cardsCopy[i+2].get_rank() \
      and cardsCopy[i+2].get_rank() + 1 == cardsCopy[i+3].get_rank() \
      and cardsCopy[i+3].get_rank() + 1 == cardsCopy[i+4].get_rank():
        self._rankTotal = cardsCopy[i+4].get_rank() 
        isStraight = True
    return isStraight


  def threeKind(self):
    """
    check if the hand is three of a kind
    return: boolean
    """
    if not self.pair():
      return False

    # this variable use for fullhouse
    self.threeKindvalue = 0
    #check if 3 consecutive ascending cards have the same value
    for i in range(len(self.cards)-2):
      if self.cards[i].get_rank() == self.cards[i+1].get_rank() == self.cards[i+2].get_rank():
        self._rankTotal = self.cards[i].get_rank() * 3
        self.threeKindvalue = self.cards[i].get_rank()
        return True
    return False


  def twoPair(self):
    """
    check if the hand is two pair
    return: boolean
    """
    maxPair = 0 #pair counter
    self.twoPairValue = 0

    cardsCopy = self.cards[:] # copy over list
    handLen = len(cardsCopy)
    totalPairs = []

    # displace found pairs into another list
    for i in range(handLen):
      # 0 - cardhand
      if i < handLen:
        for j in range(handLen):
          # 0 - card hand again to compare
          # print("CARDS", i, j)
          if j < handLen:
            if i != j and cardsCopy[i].get_rank() == cardsCopy[j].get_rank():
              # put pairs found into a list and pop it out
              totalPairs.append({"Pair1" : cardsCopy[i], "Pair2" :  cardsCopy[j]})
              cardsCopy.pop(i)
              cardsCopy.pop(j - 1)
              handLen = len(cardsCopy)
              maxPair += 1
              
    if maxPair >= 2:
        # Take two complete pairs' value and add to rank total from list dictionary
        lenTotalPairs = len(totalPairs)   
        self.twoPairValue += totalPairs[lenTotalPairs - 2]["Pair1"].get_rank() * 2
        self._rankTotal += totalPairs[lenTotalPairs - 1]["Pair1"].get_rank() * 2
        return True
    return False


  def pair(self):
    """
    check if the hand is a pair
    return: boolean
    """
    #check if the rank of 2 consecutive cards is the same
    for i in range(len(self.cards) -1):
      if self.cards[i].get_rank() == self.cards[i+1].get_rank():
        self._rankTotal = self.cards[i].get_rank() * 2
        return True

    return False


  def highCard(self):
    """
    return the high card rank if other is false
    """
    #return the last card with the highest rank
    self._rankTotal = self.cards[6].get_rank()
    return self._rankTotal


  def sortCards(self, cardsList):
    """
    sort the card
    return: list of sorted cards from low to high
    """
    # sorting the rank from lowest to highest rank
    sorted_list = sorted(cardsList, key=lambda card: card.get_rank())
    return sorted_list 
    
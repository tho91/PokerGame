
#CardGame file

import pygame
import random
from datetime import datetime
from gamebase import GameBase, TextSprite
from deck import Deck
from card import Card
from Player import Player
from HandValues import HandValues

# Card size constants
CARDSIZE_X = 83
CARDSIZE_Y = 97

class CardGame(GameBase):
    """
    Handle the poker game
    """

    # Poker game with repeatable rounds (until player has 0 in bank)
    MIN_WAGER = 20
    def __init__(self, width, height, plrWins=0, botWins=0, currentBank=1000):
        """
        Initializes Poker card game
        shuffle_sound = Sound, sound for shuffling
        cardflip_sound = Sound, sound for flipping cards
        _width = int, width of screen
        _height = int, height of screen
        _deck = Deck, deck object to manage cards
        _player = Player, user as the object Player
        _bot = Player, bot as the object player
        _pot = int, pot of money at stake
        _plrWins = int, total round wins of the player
        _botWins = int, total round wins of the bot
        _bank = int, current money the user has
        _lostGame = bool, condition if player went bankrupt
        _roundEnded = bool, condition for round ends (halts inputs)
        _waituserInput = bool, buffer for taking in one input
        """
        # Initialize the PokerGame with superclass GameBase
        super().__init__(width, height)
        pygame.mixer.init()
        self.shuffle_sound = pygame.mixer.Sound("ShuffleDeal.mp3")
        self.cardflip_sound = pygame.mixer.Sound("cardflip.mp3")

        #window size
        self._width = width
        self._height = height
        self._deck = Deck()
        
        # Player's cards handed out (face-up)
        self._player = Player(2, 250, self._height - 75)          
        self._bot = Player(2, 775, 75 + CARDSIZE_Y)
        self._pot = 0

        # Round-based system, restore previous wins and data
        self._plrWins = plrWins
        self._botWins = botWins

        # player's money
        self._bank = currentBank

        self._lostGame = False
        self._roundEnded = False
        self._waitUserInput = False

        # shuffle the cards
        random.seed(datetime.now())
        random.shuffle(self._deck.getDirectCards())
        self.startGame()


    def startGame(self):
        """
        Initializes a new game by drawing bot and player 2 cards. Flips the bot's card to prevent player from seeing their hand.
        Also contains driver code for testing specific cases in a comment block below
        """
        # Give player 2 cards, face up
        self._deck.drawHands(self._player.getHandSize(), self._player.getX(), self._player.getY(),   self._player.getCards())

        # Give bot 2 cards, face down
        botFlip = True
        self._deck.drawHands(self._bot.getHandSize(), self._bot.getX(), self._bot.getY(), self._bot.getCards(), botFlip)

        
             
        """
        ## TEST DRIVER PLAYER ##
        playerX = self._player.getX()
        playerY = self._player.getY()
        card1 = Card(playerX + (0 * CARDSIZE_X), playerY, "DECK/12d.gif")
        card2 = Card(playerX + (1 * CARDSIZE_X), playerY, "DECK/3s.gif")
        
        ## TEST DRIVER CENTER
        centerX = self._width / 2 - (CARDSIZE_X * 2)
        centerY = self._height / 2 + 50
        card3 = Card(centerX + (0 * CARDSIZE_X), centerY, "DECK/7s.gif")
        card4 = Card(centerX + (1 * CARDSIZE_X), centerY, "DECK/9h.gif")
        card5 = Card(centerX + (2 * CARDSIZE_X), centerY, "DECK/13h.gif")
        card6 = Card(centerX + (3 * CARDSIZE_X), centerY, "DECK/13s.gif")
        card7 = Card(centerX + (4 * CARDSIZE_X), centerY, "DECK/2s.gif")
        
        ## TEST DRIVER BOT ##
        botX = self._bot.getX()
        botY = self._bot.getY()
        card8 = Card(botX + (0 * CARDSIZE_X), botY, "DECK/4h.gif")
        card9 = Card(botX + (1 * CARDSIZE_X), botY, "DECK/11c.gif")

        presetPlayer = [card1, card2]
        presetCenter = [card3, card4, card5, card6, card7]
        presetBot = [card8, card9]
        self._player._cardHand = presetPlayer
        self._deck._centerCards = presetCenter
        self._bot._cardHand = presetBot
        """
        
        


    def keyDown(self, key):
        """
        Handles key presses and calls poker game choice options
        """

        # do not accept inputs if game does not permit it
        # prioritize quitting in front so it doesnt go through other game buttons
        if key == pygame.K_x and self._lostGame:
            print("Quitting program!")
            pygame.quit()

        # Player must be active and round going to check, fold or bet
        if not self._roundEnded and not self._lostGame: 
          if key == pygame.K_1: # Checks with current stakes
              self.check()
          if key == pygame.K_2: # Raise the pot then call check
              self.raiseBet()
              self.check()
          if key == pygame.K_3: # Fold, aka you lose round
              self.fold()

        # Restart round, but only if you folded or lost round
        if key == pygame.K_4 and self._roundEnded and not self._lostGame: 
            print("New round!")
            self.__init__(self._width, self._height, self._plrWins, self._botWins, self._bank)
            self.checkLost()

        # Unblock wait user input after key use
        self._waitUserInput = False


    def update(self):
        """
        Updates game display sprites and waits for a response, similar to a turn-based game
        """
      
        # Return if waiting for user input
        if not self._waitUserInput:
            super().update()

            # Draw player cards
            for card in self._player.getCards():
                self.add(card)

            # Draw botcards
            for card in self._bot.getCards():
                self.add(card)

            # Draw centercards
            for card in self._deck.getCenterCards():
                self.add(card)   
            
            # Text label configurations
            labelSize = 40

            botText = "Bot"
            botX = self._width - 375
            botY = 40
            self.drawText(botText, botX, botY, labelSize)

            #self.drawInstruction()
            # instructions text box
            instrText = "Press 1 to check, 2 to raise, and 3 to fold!!!!"
            instrX = self._width / 2 - 300 
            instrY = self._height / 2 + 100
            self.drawText(instrText, instrX, instrY, labelSize)

            #self.drawPlayerName()
            # playername text box
            plrText = "Player"
            plrX = 275
            plrY = self._height - 25
            self.drawText(plrText, plrX, plrY, labelSize)

            #self.drawPot()
            # pot text box
            potText = "Pot:"
            potX = self._width / 2 - 75
            potY = self._height / 2 - 125
            self.drawText(potText, potX, potY, labelSize)

            # min wager text box
            wagerText = "Minimum wager to play is $" + str(self.MIN_WAGER)
            wagerX = 10
            wagerY = 60
            self.drawText(wagerText, wagerX, wagerY, labelSize)

            # Refresh pot amount and bank layers since it update constantly
            refreshLayers = 2
            super().clearLayer(refreshLayers)

            # pot amount text box
            potAmntText = "$" + str(self._pot)
            potAmntX = self._width / 2 - 75
            potAmntY = self._height / 2 - 75
            self.drawText(potAmntText, potAmntX, potAmntY, labelSize, refreshLayers)
                
            # bank text box
            bankText = "Player bank: $" + str(self._bank)
            bankX = 10
            bankY = 30
            self.drawText(bankText, bankX, bankY, labelSize, refreshLayers)

            # player score text box
            playerWin = "Player Score: " + str(self._plrWins)
            playerWinX = 50
            playerWinY = 450
            self.drawText(playerWin, playerWinX, playerWinY, 30)

            # bot score text box
            botWin = "Bot Score: " + str(self._botWins)
            botWinX = 50
            botWinY = 550
            self.drawText(botWin, botWinX, botWinY, 30)

            # Wait for next user input action
            self._waitUserInput = True


    def checkLost(self, wager=20):
        """
        Checks if player lost, called within showdown() if player has no more money 
        """

        # Check if player has enough to put down a wager, 
        # if not consider they lost
        if self._bank < wager:
          print("PLAYER LOST!!!")
          loseText = "You lost all your money! Press X to quit the game."
          loseX = 200
          loseY = self._height / 2
          self.drawText(loseText, loseX, loseY, 50)
          self._lostGame = True

          # also disable gamemode inputs
          self._roundEnded = True 


    def check(self):
      """
      Draws flop first if called and then adds one each time until 5, in which checking will be a showdown and a round-ender
      """

      # Draw cards on center
      if len(self._deck.getCenterCards()) < 3:  # change to use get function

        # Deal three if first check
        self._deck.dealFlop()

      elif len(self._deck.getCenterCards()) == 3 :
        # Deal the fourth card (+1) on 2nd check
        self._deck.addToCenter()

      elif len(self._deck.getCenterCards()) == 4 :
        # Deal the fifth card (+1) on 3rd check
        self._deck.addToCenter()

      elif len(self._deck.getCenterCards()) == 5 :
        #Reveal all cards (basically just the bot's since others are already)
        self._roundEnded = True
        self.combineCards()
        self.showdown()
        

    def raiseBet(self):
      """
      Raises pot based off user input, bot always matches wager. Assumes player goes all in if not enough money to wager anymore.
      """

      # If less than wager, just go all in and set bank to 0
      if self._bank <= self.MIN_WAGER:
        self._pot += self._bank * 2
        self._bank = 0
        print("All in.")
        return 
      
      addThis = 0
      while addThis < self.MIN_WAGER:
        #Check for input error
        try:
          addThis = int(input("Add money to pot: "))
          if addThis < self.MIN_WAGER:
            print("Minimun wager is $20.")
            raise ValueError 
          if self._bank - addThis < 0:
            print("Bet cannot exceed bank amount.")
            raise ValueError 
        except ValueError:
            addThis = 0
            print("Input Error. Please try again.")      

      # calculate the pot and player bank after raise
      self._bank -= addThis
      self._pot += addThis * 2


    def fold(self):
        """
        Folds and ends the game, giving bot an automatic win, and display the restart option
        """

        print("Round Ended!!!!!!")
        self._roundEnded = True
        self._botWins += 1
        self.drawRestartText()


    def combineCards(self):
      """
      Combines center and player cards and forms player's and bot's hand values to compare for winner of a round
      """

      # add the player cards and center cards into one list and calculate the hand value
      self._player.getCards().extend(self._deck.getCenterCards())
      self._playerHandValue = HandValues(self._player.getCards())

      # add the bot cards and center cards into one list and calculate the hand value
      self._bot.getCards().extend(self._deck.getCenterCards())
      self._botHandValue = HandValues(self._bot.getCards())

    def showdown(self):
      """
      Forces both player and bot to reveal hands and determine winner by measuring hand value. Breaks ties by highcard for card comparisons less than a straight.
      """

      # Show off all cards on deck and determine winner
      for card in (self._bot.getCards()): # this one too
        card.flip()
      for card in self._deck.getCenterCards():
        card.flip()
  
      # Showdown
      print("SHOWDOWN!!!")
      print("PLAYER HAND VALUE: ")
      playerValue = self._playerHandValue.checkHand()
      print()

      print("BOT HAND VALUE: ")
      botValue = self._botHandValue.checkHand()

      #create a local list for player and bot cards to check for tie
      playerHand = self._player.getCards()
      botHand = self._bot.getCards()

      # Sort player and bot hands by rank to compre for tie breakers
      playerHand = sorted(playerHand, key=lambda card: card.get_rank())
      botHand = sorted(botHand, key=lambda card: card.get_rank())

      # print(playerValue, "<PLAYER VS BOT>", botValue) TEST TEST TEST
      playerWinText = "THE PLAYER WINS!"
      botWinText = "THE BOT WINS!"

      # Assume it's a tie at first
      winnerText = "THERE IS A TIE!"
    
      if playerValue > botValue:
        # Reward player for winning
        winnerText = playerWinText
        self._bank += self._pot
        self._plrWins += 1

      #tie does not need to check if player and bot have straight and up 
      # because they both use 5 cards already
      elif playerValue == botValue and playerValue < 3500:
        # Showdown tie handler
        # go from highest to lowest card, 6 to 1
        print("HANDS ARE SAME! DETERMINING HIGHEST CARDS AS WINNER...")

        #loop in reverse to check for higher rank in player and bot hands
        for card in range(6, 1, -1):
          print("CARDVAL", playerHand[card].get_rank(),  botHand[card].get_rank())
          if playerHand[card].get_rank() > botHand[card].get_rank():
            # Reward player for winning
            winnerText = playerWinText
            self._bank += self._pot
            self._plrWins += 1
            break
          elif playerHand[card].get_rank() < botHand[card].get_rank():
            # Reward bot for winning
            winnerText = botWinText
            self._botWins += 1
            break         
      elif playerValue < botValue:
        # Reward bot for winning
        winnerText = botWinText
        self._botWins += 1

      # if it truly is a tie, refund pot
      if winnerText == "THERE IS A TIE!":
        self._bank += int(self._pot / 2)

      # winner text label
      winnerTextX = self._width / 2 - 200
      winnerTextY = self._height / 2 - 200
      self.drawText(winnerText, winnerTextX, winnerTextY, 60, 3)      
      self.drawRestartText()

    def drawText(self, text, renderX, renderY, \
         textSize=40, layer=0, textColor=(0, 0, 0), bkgColor=(255,255,255)):
      """
      Draws a text label with the given parameters and adds to the sprite renderer
      """

      # Draws a text box
      textFont = pygame.font.SysFont('freesanbold.ttf', textSize)
      textBox = textFont.render(text, True, (0, 0, 0), (255,255,255))
      rect = textBox.get_rect()
      self._display.blit(textBox, rect)
      textSprite = TextSprite(renderX, renderY, textBox)
      textSprite._layer = layer
      self.add(textSprite)

    def drawRestartText(self):
      """
      draw the restart text
      """
      # Make a text label for restarts since its called multiple times
      restartText = "Press 4 to restart a new round."
      restartX = self._width / 2 - 200
      restartY = self._height / 2
      restartLayer = 4
      self.drawText(restartText, restartX, restartY, 50, restartLayer)


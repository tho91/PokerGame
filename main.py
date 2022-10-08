# Final Project Group 10
# Created by Anthony Chen, Thien Ho
# We (Anthony Chen, Thien Ho) do hereby certify that I/we have derived no assistance for this project or examination from any sources whatever, whether oral, written, or in print.

# Import the pygame module
from cardGame import CardGame


# Initialize pygame
# Define constants for the screen width and height
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

def main():
  """
  Driver file, runs the game at given screen width and height    
  """

  print('WELOME TO THE POKER CLUB')
  game = CardGame(SCREEN_WIDTH, SCREEN_HEIGHT)
  game.run()
    
main()

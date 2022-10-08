# GameBase file

import pygame

class GameBase:
   """
    Class manages image sprites
   """

   def __init__(self, width, height):
      """
      Contruct the game
      Handles sprite rendering and game update/events.
      _width = int, width of the screen
      _height = int, height of screen
      _display = Display, the window of the screen in pygame
      _clock = Clock, tracks frames per second
      _framesPerSecond = int, amount of frames per second
      _sprites = LayeredUpdates, contains layers of sprites
      _ticks = int, tracks in-game tick per update loop
      _background = Image, renders the poker table in the background
      """
      pygame.init()
      self._width = width
      self._height = height
      self._display = pygame.display.set_mode((self._width, self._height))
      self._clock = pygame.time.Clock()
      self._framesPerSecond = 9999
      self._sprites = pygame.sprite.LayeredUpdates()
      self._ticks = 0
      pygame.key.set_repeat(0)
      self.background = pygame.image.load("table.jpg")

  
   def mouseButtonDown(self, x, y):
      """
      Passes mouse click function, meant to be handled/overridden by subclass
      """
      return
 
   def keyDown(self, key) :
      """
      Passes keyDown events to subclass that overrides it
      """
      return
    
   def update(self) :
      """
      Updates all sprites
      """
      self._sprites.update()
    
   def draw(self) :
      """
      Draws all sprites from _display
      """
      self._sprites.draw(self._display)
    
   def add(self, sprite) :
      """
      Adds sprite object into _sprites to be rendered
      """
      self._sprites.add(sprite)

   def clearLayer(self, layer):
      """
      Clears all sprites from a specfic layer
      """
      self._sprites.remove_sprites_of_layer(layer_nr=layer)
        
   def getTicks(self):
      """
      Returns amount of ticks per update() cycle as an int
      """
      return self._ticks
        
   def quit(self) :
      """
      Quits and crashes the program
      """
      pygame.quit()        
    
   def run(self):
      """
      Detects for events and runs an update function to 
      render all sprites and displays as well as any activity
      """
      while True:
         for event in pygame.event.get() :
            if event.type == pygame.QUIT :
               self.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN :                    
               self.mouseButtonDown(event.pos[0], event.pos[1])
            elif event.type == pygame.KEYDOWN :
               self.keyDown(event.key)
         self.update()
         WHITE = (255, 255, 255)
         self._display.fill(WHITE)
         self._display.blit(self.background, (0,0))
         self.draw()
         pygame.display.update()
         self._clock.tick(self._framesPerSecond)
         self._ticks += 1


class ImageSprite(pygame.sprite.Sprite):
    """
    Class manages image sprites
    """

    def __init__(self, x, y, filename) :
      """
      Loads/renders image ready to be added to gameBase
      image = Image, image in converted pixels
      rect = Rect, rectangle to draw/display image
      """
      super().__init__()
      self.loadImage(x, y, filename)
      #self._layer = 1

    def loadImage(self, x, y, filename) :
      """ 
      Converts file directory name into pixels to be rendered
      """
      img = pygame.image.load(filename).convert()
      #WHITE = (255, 255, 255)
      #img.set_colorkey(WHITE)
      self.image = img
      self.rect = self.image.get_rect() # returns object Rect
      self.rect.x = x
      self.rect.y = y - self.rect.height
     
    def moveBy(self, dx, dy) :
      """
      Moves sprite drawing by dx and dy.
      """
      self.rect.x += dx
      self.rect.y += dy


class TextSprite(
   pygame.sprite.Sprite):
   """
    Class manages text sprites
   """

   def __init__(self, x, y, text):
      """
      Loads text by blitting the text itself as a pixel onto the 
      scene
      image = Image, the text as pixels
      rect = Rect, the rectangle to draw the text onto
      """
      super().__init__()
      self.loadImage(x, y, text)

   def loadImage(self, x, y, text):
      """
      Text is already converted to pygame-readable drawings, so just set it as image and set the place to draw
      """
      img = text # Text is already converted, so we can just set it equal
      self.image = img
      # self._layer = 1 # overlap text on all sprites
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y - self.rect.height

   def moveBy(self, dx, dy):
      """
      Moves text label to dx and dy
      """
      self.rect.x += dx
      self.rect.y += dy


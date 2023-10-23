import sys
import pygame
import random
import time
import math
from elements import *
from pygame.locals import *
import PIL 
from PIL import Image
from PIL import ImageFilter

class App:
  def __init__(self): 
    self.fps = 60
    self.clock = pygame.time.Clock()
    self.screen = None

    self.mousedown = False
    self.pause = False

    self.width = 2000
    self.height = 2000
    

    self.psize = 25
    self.numparts = 0
    self.run = True
    self.faulty_key = None
    self.faulty_move_key = None

    self.board = Board(self,self.width,self.height,self.psize)
    self.tempboard = Board(self,self.width,self.height,self.psize)

    self.tempboard = {}

    self.draw_pixel_type = Sand
    self.pixel_draw_size = (((self.width+self.height)//2)//self.psize)//100
    self.pixel_draw_size = 3

 

  def update(self):
    mouse_pos = pygame.mouse.get_pos()

    
    # UPDATE BOARD
    if not self.pause:

      max_height = math.ceil(self.board.height/self.psize)
      max_width = math.ceil(self.board.width/self.psize)

      #for y in range(0,max_height+1):
      #  for x in range(0,max_width+1):
      #self.tempboard = Board(self,self.width,self.height,self.psize)

      for y in range(0,max_height+1):
        x_list = []
        for x in range(0,max_width+1):
          x_list.append(x)
        random.shuffle(x_list)
        for x in x_list:
          position = (x,max_width-y)
          pixel = self.board.get_item(position)
          if not pixel == self.board.none_type_object:
            if pixel.time < self.board.current_update:
              pixel.move(self.board)
              pixel.set_time(self.board.current_update)
        



    #for position, pixel in self.tempboard.items():
    #  self.tempboard.get_item(position).move(self.board)

    #self.board = Board(self,self.width,self.height,self.psize)
    #for k,v in self.tempboard.items():
    #  self.board.set_item(k,v)
    
    # EVENTS 
    ev = pygame.event.get()
    for event in ev:
      if event.type == QUIT:
        pygame.quit() 

      if event.type == pygame.MOUSEBUTTONDOWN:
        self.mousedown = True

      if event.type == pygame.MOUSEBUTTONUP:
        self.mousedown = False

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          self.pause = not self.pause
        if event.key == pygame.K_1:
          self.draw_pixel_type = Sand
        if event.key == pygame.K_2:
          self.draw_pixel_type = Water
        if event.key == pygame.K_3:
          self.draw_pixel_type = Rock
        if event.key == pygame.K_4:
          self.draw_pixel_type = Lava
        if event.key == pygame.K_5:
          self.draw_pixel_type = Wood
        if event.key == pygame.K_6:
          self.draw_pixel_type = Steam
        if event.key == pygame.K_7:
          self.draw_pixel_type = Acid
        if event.key == pygame.K_0:
          self.draw_pixel_type = None



      
      #place pixels
      if self.mousedown == True:
        check_spots = []
        d = self.pixel_draw_size

        if 1:
          for i in range(-d,d):
            for j in range(-d,d):
              check_spots.append((i,j))
        if 0:
            check_spots.append((0,0))


        mx = int(mouse_pos[0] / self.psize)
        my = int(mouse_pos[1] / self.psize)

        #print(mx,my)

        for each_spot in check_spots:
          relative_spot = (mx-each_spot[0],my-each_spot[1])

          if relative_spot[0] >= 0 and relative_spot[0] < self.width and relative_spot[1] >= 0 and relative_spot[1] < self.height:
            if self.draw_pixel_type == None:
              p = self.board.get_item(relative_spot)
              del p
              self.board.set_item(relative_spot,None)
            else:
              if self.board.get_item(relative_spot) == self.board.none_type_object:
                pixel = self.draw_pixel_type()
                pixel.set_position(relative_spot, self.board)
                self.numparts += 1

    self.board.current_update += 1


   
  def draw(self, screen):
    self.screen.fill((0, 0, 0))
    for position, value in self.board.items():
      if not value == self.board.none_type_object:
        pixel = position
        color = value.color
        pygame.draw.rect(self.screen, color, (position[0]*self.psize, position[1]*self.psize, self.psize, self.psize))
      
    pygame.display.flip()
    
   
  def init(self):
    pygame.init()
    self.screen = pygame.display.set_mode((self.width, self.height));
 


class Element:
  def __init__(self):
    self.time = 0
    self.creation_time = -1

  def set_time(self, time):
    self.time = time
  def type(self):
    return type(self)

class Pixel(Element):
  def __init__(self):
    super().__init__()
    self.color = None
    self.position = None

    self.move_positions = None


    self.check_spots = None

    self.time_convertion = None
    self.weight = 0
    self.heat = 0
    self.reactions = []

  def get_position(self):
    return self.position

  def set_position(self, position, board):
    if self.creation_time == -1:
      self.creation_time = board.current_update
    board.remove_item(self.position)
    self.position = position
    board.set_item(self.position, self)

  def update(self, board):
    pass  

  def swap(self, target, board):
    self_pos = self.position
    target_pos = target.position

    board.set_item(self_pos, target)
    target.position = self_pos
    board.set_item(target_pos, self)
    self.position = target_pos

    self.set_time(board.current_update)
    target.set_time(board.current_update)

    

  def move(self, board):
    if self.time >= board.current_update:
      pass
    xpos = self.position[0]
    ypos = self.position[1]

    randomized_checkspots = []
    print (self.time, board.current_update)

    for each_list in self.check_spots:
      random.shuffle(each_list)

      for each_spot in each_list:
        randomized_checkspots.append(each_spot)

    found_spot = None
    for each_spot in randomized_checkspots:
      relative_spot = (xpos-each_spot[0],ypos-each_spot[1])
      target_item = board.get_item(relative_spot)

      if relative_spot[0] >= 0 and relative_spot[0] <= board.width/board.psize  and relative_spot[1] >= 0 and relative_spot[1] <= board.height/board.psize :
        if target_item == board.none_type_object:
          found_spot = relative_spot
          break
        else:
          for self_reaction in self.reactions:
            if isinstance(target_item, self_reaction["element"]):
              for target_reaction in target_item.reactions:
                if isinstance(self, target_reaction["element"]):
                  if target_reaction["result"] != None:
                    px = target_reaction["result"]()
                    px.set_position(target_item.position, board)
                    px.set_time(board.current_update)
                  else:
                    board.set_item(target_item.position, None)
                  break

              if self_reaction["result"] != None:
                p = self_reaction["result"]()
                p.set_position(self.position, board)
                p.set_time(board.current_update)
              else:
                board.set_item(self.position, None)
              
              return
          if target_item.weight < self.weight:
            self.swap(target_item, board)
      else:
        break

    if self.creation_time != -1 and self.time_convertion != None and found_spot == None:
      if board.current_update-self.creation_time > self.time_convertion["time"]:
        if self.time_convertion['chance'] > random.randint(1,1000)/1000:
          if self.time_convertion["element"] != None:
            p = self.time_convertion["element"]()
            p.set_position(self.position, board)
          else:
            board.set_item(self.position, None)
          return
        else:
          board.set_item(self.position, None)
          return
    if found_spot != None:
      self.set_position(found_spot,board)
    #if found_spot == None:
    #  e = self.set_position((xpos,ypos),board)
    
    



# Pixel Types


  


class Board:
  def __init__(self,app,width,height,psize):
    self._board = []
    #self._board_reference = {}

    self.none_type_object = None

    for y in range(height):
      templist = []
      for x in range(width):
        templist.append(self.none_type_object)
      self._board.append(templist)

    self.width = width
    self.height = height

    self.app = app
    self.current_update = 0

    self.psize = psize

  def init_array(self):
    pass
    
  #def get_board_reference(self):
  #  return self._board_reference.items()

  def values(self):
    return self._board

  def items(self):
    templist = []

    max_height = math.ceil(self.height/self.psize)
    max_width = math.ceil(self.width/self.psize)

    for y in range(0,max_height+1):
      for x in range(0,max_width+1):
        position = (max_width-x,max_height-y)
        pixel = self.get_item(position)
        if not pixel == self.none_type_object:
          templist.append((position,pixel))
    #templist.reverse()
    return templist
    #return self._board.items()

  def set_item(self,key,value):
    #if self._board_reference.get(key):
    #  pass 
    #  print ("invalid %s" % str(key))
    #self._board_reference[key] = (value)
    self._board[key[1]][key[0]] = value

  def get_item(self,key):
    #return self._board.get(key)
    return self._board[key[1]][key[0]]

  def remove_item(self,key):
    try:
      self.set_item(key, self.none_type_object)
    except TypeError:
      pass
    #try:
    #  del self._board_reference[key]
    #except KeyError:
    #  pass
    

if __name__ == "__main__":
  app = App()
  app.init()

  while True:
    start_time = time.time()
    app.update()
    app.draw(app.screen)
    app.clock.tick(app.fps)
    fps = app.fps - (time.time()-start_time)*app.fps
    #print ("fps: %s" % fps)
from main import Pixel
import random

class ImmovableSolid(Pixel):
  def __init__(self):
    super().__init__()
    self.check_spots = []


class MoveableSolid(Pixel):
  def __init__(self):
    super().__init__()
    self.check_spots = [[(0,-1)],[(-1,-1),(1,-1)]]

class Liquid(Pixel):
  def __init__(self):
    super().__init__()
    self.check_spots = [[(0,-1)],[(-1,-1),(1,-1)],[(1,0),(-1,0)]]

class Gas(Pixel):
  def __init__(self):
    super().__init__()
    self.check_spots = [[(0,1),(1,1),(-1,1)],[(-1,0),(1,0)]]



# Pixel Materials

class Wood(ImmovableSolid):
  def __init__(self):
    super().__init__()
    self.color = random.choice([(130, 91, 48),(135, 95, 51)])
    self.weight = 1000000
    self.heat = 0

    self.reactions = [{"element": Acid, "result": None}]


class Sand(MoveableSolid):
  def __init__(self):
    super().__init__()
    self.color = random.choice([(235, 235, 164),(217, 217, 154),(207, 207, 147)])
    self.weight = 30
    self.heat = 0

    self.reactions = [{"element": Acid, "result": None}]

class Rock(MoveableSolid):
  def __init__(self):
    super().__init__()
    self.color = random.choice([(131, 124, 143),(131, 124, 143),(134, 128, 150)])
    self.weight = 30
    self.heat = 0

    self.reactions = [{"element": Acid, "result": None}]

class Water(Liquid):
  def __init__(self):
    super().__init__()
    self.color = random.choice([(67, 137, 156),(67, 136, 156),(67, 135, 156)])
    self.weight = 10
    self.heat = 0

    self.reactions = [{"element": Lava, "result": Steam}]

class Lava(Liquid):
  def __init__(self):
    super().__init__()
    self.color = random.choice([(245, 100, 10),(245, 100, 9),(245, 100, 8)])
    self.weight = 20
    self.heat = 100

    self.reactions = [{"element": Water, "result": Rock}]

class Steam(Gas):
  def __init__(self):
    super().__init__()
    self.color = random.choice([(154, 156, 154),(157, 158, 153)])
    self.weight = 1
    self.heat = 10
    self.time_convertion = {"element": Water, "time": random.randint(1,400) + 200, "chance": 0.5}

class Acid(Liquid):
  def __init__(self):
    super().__init__()
    self.color = random.choice([(86, 231, 80),(86, 232, 81)]) 
    self.heat = 0

    self.reactions = [{"element": Rock, "result": AerosoleAcid},{"element": Sand, "result": AerosoleAcid},{"element": Wood, "result": AerosoleAcid}]

class AerosoleAcid(Gas):
  def __init__(self):
    super().__init__()
    self.color = random.choice([(144, 237, 140)])
    self.weight = 0.97
    self.heat = 10

    self.time_convertion = {"element": Acid, "time": random.randint(1,400) + 200, "chance": 0.1}



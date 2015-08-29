import time

from ev3.lego import MediumMotor
from ev3.lego import LargeMotor
from ev3.lego import InfraredSensor
from ev3.lego import TouchSensor

PUTTING = 'putting'
GETTING = 'getting'
STOPPING = 'stopping'

# generic decorator for reverting task_state to None after arm servomotor single run
def revert_task_state_to_none_after_call(func):
  def inner(*args, **kwargs):
    func(*args, **kwargs)
    slf = args[0]
    setattr(slf, 'task_state', None)
  return inner

class Arm():
  """ Class Arm represents build from LEGO Mindstorms arm for catching and moving cans of beer """

  def __init__(self, port='A', speed=100, **kwargs):
    self.port = port
    self.speed = speed
    self.test_direction = 1
    self.motor = MediumMotor(port=self.port)
    self.motor.reset()
    self.task_state = None

  @revert_task_state_to_none_after_call
  def get(self):
    self.task_state = GETTING
    self.speed = 100
    self.motor.run_forever(self.speed, regulation_mode=False)

  @revert_task_state_to_none_after_call
  def put(self):
    self.task_state = PUTTING
    self.speed = -50
    self.motor.run_forever(self.speed, regulation_mode=False)

  @revert_task_state_to_none_after_call
  def stop(self):
    self.task_state = STOPPING
    self.motor.stop()

  def test(self):
    while True:
      if self.test_direction == -1:
        self.put()
      else:
        self.get()
      self.test_direction *= -1
      raw_input("Press enter")
    self.motor.stop()


class Track():
  """ Class Track represents caterpillar track for moving beerbot """

  def __init__(self, port, speed=100, **kwargs):
    self.port = port
    self.speed = speed
    self.motor = LargeMotor(port=self.port)
    self.motor.reset()

  def move(self, speed):
    self.motor.run_forever(self.speed, regulation_mode=False)   

  def stop(self):
    self.motor.stop()


class Touch():
  """ Class Touch represents sensor for counting putting and getting requests """

  def __init__(self, port):
    self.port = port
    self.sensor = TouchSensor(port=self.port)

  def is_pushed(self):
    return self.sensor.is_pushed
    

class Infrared():
  """ Class Infrared represents "eye-liked" sensor to seek a distance """

  def __init__(self, port):
    self.port = port
    self.sensor = InfraredSensor(port=self.port)

  def seek(self):
    while True:
      ret = self.sensor.seek
      time.sleep(1)
      print ret

  def prox(self):
    while True:
      ret = self.sensor.prox
      time.sleep(1)
      print ret

class BeerBot():
  """ Object of this class represents single working beerbot :)
      this class was made due to provide a simple api from CLI 
  """

  def __init__(self, **kwargs):
    self.arm = Arm(port='A')
    self.track_left = Track(port='B')
    self.track_right = Track(port='C')
    self.infrared_sensor = Infrared(port='4')
    self.touch_sensor = Touch(port='1')

  def go(self, time=1):
    self.track_left.motor.run_forever(self.track_left.speed, regulation_mode=False) 
    self.track_right.motor.run_forever(self.track_righ.speed, regulation_mode=False)
    time.sleep(time)
    self.track_right.motor.stop()

  def stop(self):
    self.arm.motor.stop()
    self.track_left.motor.stop()
    self.track_right.motor.stop()

  def get(self):
    self.arm.get()

  def put(self):
    self.arm.put()

  def left(self, time=1):
    self.track_right.motor.run_forever(self.track_right.speed, regulation_mode=False)
    time.sleep(time)
    self.track_right.motor.stop()

  def right(self, time=1):
    self.track_left.motor.run_forever(self.track_left.speed, regulation_mode=False)
    time.sleep(time)
    self.track_left.motor.stop()

  def seek(self):
    self.infrared_sensor.seek()

  def prox(self):
    self.infrared_sensor.prox()

  def pos(self):
    if self.touch_sensor.is_pushed:
      print "Beerbot is free."
    else :
      print "Beerbot is loaded."




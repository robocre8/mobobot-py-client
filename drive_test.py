from mobobot_client import MoboBotClient
import time

robot = MoboBotClient()

robot.connect("mobobot.local", 8888, 0.018)
robot.start_heartbeat()

v = 0.1
w = 0.5

robot.writeRobotVel(0.0, 0.0)


while True:
  # w*=-1.0
  time.sleep(2.0)
  robot.writeRobotVel(v, 0.0)
  time.sleep(5.0)
  robot.writeRobotVel(0.0, 0.0)
  time.sleep(2.0)
  robot.writeRobotVel(0.0, w)
  time.sleep(5.0)
  robot.writeRobotVel(0.0, 0.0)

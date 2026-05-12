from mobobot_client import MoboBotClient
import time

robot = MoboBotClient()

robot.connect("mobobot.local", 8888, 0.018)
robot.start_heartbeat()

v = 0.1
w = 0.5

time.sleep(1.0)
robot.writeRobotVel(0.0, 0.0)
time.sleep(1.0)
robot.writeServo1Angle(0)


for _ in range(5):
  # w*=-1.0
  time.sleep(1.0)
  robot.writeServo1Angle(-30)
  time.sleep(1.0)
  robot.writeRobotVel(v, 0.0)
  time.sleep(6.0)
  robot.writeRobotVel(0.0, 0.0)
  time.sleep(1.0)
  robot.writeServo1Angle(0)
  time.sleep(1.0)
  robot.writeServo1Angle(-30)
  time.sleep(1.0)
  robot.writeRobotVel(0.0, w)
  time.sleep(6.0)
  robot.writeRobotVel(0.0, 0.0)
  time.sleep(1.0)
  robot.writeServo1Angle(0)

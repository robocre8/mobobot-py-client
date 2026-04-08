from texabot_client import TexaBotClient
import time

robot = TexaBotClient()

robot.connect("texabot.local", 8888, 0.018)
robot.start_heartbeat()

v = 0.1
w = 0.5

robot.writeCmdVel(0.0, 0.0)


while True:
  # w*=-1.0
  time.sleep(2.0)
  robot.writeCmdVel(v, 0.0)
  time.sleep(5.0)
  robot.writeCmdVel(0.0, 0.0)
  time.sleep(2.0)
  robot.writeCmdVel(0.0, w)
  time.sleep(5.0)
  robot.writeCmdVel(0.0, 0.0)

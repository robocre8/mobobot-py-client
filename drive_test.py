from educre8bot_client import EduCre8BotClient
import time

robot = EduCre8BotClient()

robot.connect("educre8bot.local", 8888, 0.018)
robot.start_heartbeat()
time.sleep(2.0)

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

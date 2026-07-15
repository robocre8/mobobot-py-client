from educre8bot_client import EduCre8BotClient
import time

robot = EduCre8BotClient()

robot.connect("educre8bot.local", 8888, 0.018)
robot.start_heartbeat()
time.sleep(2.0)

robot.driveFor(robot.FORWARD, 300)
time.sleep(1.0)
robot.turnFor(robot.LEFT, 90)
time.sleep(1.0)

robot.driveFor(robot.FORWARD, 300)
time.sleep(1.0)
robot.turnFor(robot.LEFT, 90)
time.sleep(1.0)

robot.driveFor(robot.FORWARD, 300)
time.sleep(1.0)
robot.turnFor(robot.LEFT, 90)
time.sleep(1.0)

robot.driveFor(robot.FORWARD, 300)
time.sleep(1.0)
robot.turnFor(robot.LEFT, 90)

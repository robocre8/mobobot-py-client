from educre8bot_client import EduCre8BotClient
import time

robot = EduCre8BotClient()

try:
  robot.connect("educre8bot.local", 8888, 0.018)
  robot.start_heartbeat()
  time.sleep(2.0)
  # robot.setWheelRadiusParam(0.034)
  # robot.setWheelDistanceParam(0.170)

  print("[SUCCESS]: PROGRAM STARTED RUNNING")

  #--- GENERATED BLOCK CODE -----
  robot.setGripPercent(45)
  for _ in range(4):
    robot.gripperActionOpen()
    time.sleep(2)
    robot.gripperActionGrip()
    time.sleep(1)
    robot.driveFor(robot.FORWARD, 400)
    time.sleep(1)
    robot.turnFor(robot.LEFT, 90)
    time.sleep(1)
  robot.gripperActionOpen()
  robot.stop()
  #--- GENERATED BLOCK CODE -----

except Exception as e:
  print("[ERROR]:", e)

finally:
  print("[CLEANUP]: STOPPING AND EXITING PROGRAM SAFELY")
  try:
      robot.stop()
  except:
      pass


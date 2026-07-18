from educre8bot_client import EduCre8BotClient
import time

robot = EduCre8BotClient()

try:
  robot.connect("educre8bot.local", 8888, 0.018)
  robot.start_heartbeat()
  time.sleep(2.0)

  print("[SUCCESS]: PROGRAM STARTED RUNNING")

  #--- GENERATED BLOCK CODE -----
  for _ in range(2):
    time.sleep(3)
    robot.writeServoAngle(45)
    robot.rgbOn(255, 0, 0)
    robot.buzzerOn()
    time.sleep(3)
    robot.writeServoAngle(7)
    robot.rgbOn(0, 0, 0)
    robot.buzzerOff()
    time.sleep(3)
    robot.writeServoAngle(-45)
    robot.rgbOn(0, 0, 255)
    robot.buzzerOn()
    time.sleep(3)
    robot.writeServoAngle(0)
    robot.rgbOn(0, 0, 0)
    robot.buzzerOff()
  #--- GENERATED BLOCK CODE -----

except Exception as e:
  print("[ERROR]:", e)

finally:
  print("[CLEANUP]: STOPPING AND EXITING PROGRAM SAFELY")
  try:
      robot.stop()
  except:
      pass


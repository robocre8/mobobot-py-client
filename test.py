from mobobot_client import MoboBotClient
import time

robot = MoboBotClient()

robot.connect("mobobot.local", 8888, 0.018)
robot.start_heartbeat()
time.sleep(2.0)


while True:
  robot.buzzerOn()

  time.sleep(2.0)
  robot.rgbOn(255, 0, 0)
  # robot.writeServo1Angle(0)
  robot.writeServo2Angle(0)
  print("sonar: ", robot.readSonar())
  print("line1: ", robot.readLineSensor1())
  print("line2: ", robot.readLineSensor2())

  time.sleep(2.0)
  robot.rgbOn(0, 255, 0)
  # robot.writeServo1Angle(90)
  robot.writeServo2Angle(90)
  print("sonar: ", robot.readSonar())
  print("line1: ", robot.readLineSensor1())
  print("line2: ", robot.readLineSensor2())

  robot.buzzerOff()

  time.sleep(2.0)
  robot.rgbOn(0, 0, 255)
  # robot.writeServo1Angle(0)
  robot.writeServo2Angle(0)
  print("sonar: ", robot.readSonar())
  print("line1: ", robot.readLineSensor1())
  print("line2: ", robot.readLineSensor2())

  time.sleep(2.0)
  robot.rgbOff()
  # robot.writeServo1Angle(-90)
  robot.writeServo2Angle(-90)
  print("sonar: ", robot.readSonar())
  print("line1: ", robot.readLineSensor1())
  print("line2: ", robot.readLineSensor2())

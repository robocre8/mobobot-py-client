## MoboBot Python Client Live Coding Library
Python UDP Interface Client Library for MoboBot.

> NOTE: It works with the MoboBot Firmware
> It currently connects to SSID: mobobot1234, PASSWORD: mobobot1234

#

## Install
- you'll need to pip install the pyserial library
  ```shell
    pip3 install mobobot-client   //linux or mac
  ```
  OR
  ```shell
    pip install mobobot-client  //windows
  ```

#

## Uninstall
- you'll need to pip install the pyserial library
  ```shell
    pip3 uninstall mobobot-client   //linux or mac
  ```
  ```shell
    pip uninstall mobobot-client  //windows
  ```

#

## example code 1
```python
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
```

#

## example code 2
```python
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
```

#
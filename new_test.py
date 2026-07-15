from mobobot_client import MoboBotClient
import time

robot = MoboBotClient()

robot.connect("mobobot.local", 8888, 0.018)
robot.start_heartbeat()
time.sleep(2.0)

# while True: 
#   print(robot.wheel_radius_param_val, robot.wheel_dist_param_val)
#   robot.setWheelRadiusParam(0.034)
#   robot.setWheelDistanceParam(0.165)
#   # robot.setTurnVel(10)
#   time.sleep(2.0)

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

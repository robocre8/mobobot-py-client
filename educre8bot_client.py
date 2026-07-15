import socket
import struct
from time import sleep, time
from math import pi
import threading


class EduCre8BotClient:

    def __init__(self):

        self.START_BYTE = 0xAA
        self.READ_DATA = 0x01
        self.WRITE_SERVO_ANGLE = 0x02
        self.WRITE_GRIPPER_ANGLE = 0x03
        self.WRITE_GRIPPER_DIST = 0x04
        self.WRITE_BUZZER = 0x05
        self.WRITE_LED = 0x06
        self.WRITE_RGB_LED = 0x07
        self.WRITE_MOTOR_VEL = 0x08
        self.WRITE_MOTOR_PWM = 0x09
        self.WRITE_CMD_VEL = 0x0A
        self.SET_WHEEL_ODOM_PARAMS = 0x0B
        self.CLEAR_CONTROLLER_DATA = 0x0C
        self.SET_CONTROLLER_CMD_TIMEOUT = 0x0D
        self.SET_UDP_CONN_TIMEOUT = 0x0E
        self.UDP_HEART_BEAT = 0x0F
        self.RESET_PARAMS = 0x10
        self.SET_WHEEL_RADIUS = 0x11
        self.SET_WHEEL_DISTANCE = 0x12


        self.sock: socket.socket | None = None
        self.addr = None
        self.timeout = 0.2
        self.heartbeat_running = True

        self._lock = threading.Lock()


        self.sonar_val: float = 0.0
        self.tof_val: float = 0.0
        self.line_sensor_val: float = 0.0
        self.tl_val: float = 0.0
        self.tr_val: float = 0.0
        self.yaw_val: float = 0.0
        self.dist_val: float = 0.0
        self.color_sensor_val: float = 0.0
        self.wheel_radius_param_val: float = 0.0
        self.wheel_dist_param_val: float = 0.0
        self.max_motor_speed_val: float = 0.0

        self.is_pwm_mode: bool = False

        #---------------------------------
        self.FORWARD = 1
        self.BACKWARD = -1
        self.FRONT = 0
        self.LEFT = 1
        self.RIGHT = -1

        self.percent_gripper_open: int = 100
        self.percent_drive_speed: int = 30
        self.percent_turn_speed: int = 10
        self.drive_vel: float = 0.15
        self.turn_vel: float = 0.5
        


    # ------------------ CONNECT ------------------
    def connect(self, ip: str, port: int = 8888, timeout: float = 0.2):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(timeout)
        
        self.addr = (ip, port)

        sleep(3.0)
        for _ in range(10):
            success = self.clearControllerData()

            if success:
                print("MoboBot Connected Successfully")
                return
            sleep(0.1)

        self.disconnect()
        raise RuntimeError("Could not connect to MoboBot, Try Again")


    def disconnect(self):
        if self.sock:
            self.sock.close()
            self.sock = None


    def start_heartbeat(self, heartbeat_interval:float = 1.0, sensor_read_interval: float = 0.1):
        def loop():
            heartBeatInterval = heartbeat_interval
            sensorReadInterval = sensor_read_interval

            heartBeatTime = time()
            sensorReadTime = time()
            while self.heartbeat_running:
                currentTime = time()
                if (currentTime - heartBeatTime) > heartBeatInterval :
                    self.udpHeartBeat()
                    heartBeatTime = time()

                if (currentTime - sensorReadTime) > sensorReadInterval :
                    success, sensor_data = self.readData()

                    if success:
                        with self._lock:
                            self.sonar_val = sensor_data[0]
                            self.tof_val = sensor_data[1]
                            self.line_sensor_val = sensor_data[2]
                            self.tl_val = sensor_data[3]
                            self.tr_val = sensor_data[4]
                            self.yaw_val = sensor_data[5]
                            self.dist_val = sensor_data[6]
                            self.color_sensor_val = sensor_data[7]
                            self.wheel_radius_param_val = sensor_data[8]
                            self.wheel_dist_param_val = sensor_data[9]
                            self.max_motor_speed_val = sensor_data[10]

                    sensorReadTime = time()

        threading.Thread(target=loop, daemon=True).start()

    def stop_heartbeat(self):
        self.heartbeat_running = False


    # ------------------ PACKET ------------------

    def _send_packet(self, cmd: int, payload: bytes = b""):

        if self.sock is None:
            raise RuntimeError("UDP not connected")

        length = len(payload)

        packet = bytearray([self.START_BYTE, cmd, length])
        packet.extend(payload)

        checksum = sum(packet) & 0xFF
        packet.append(checksum)

        self.sock.sendto(packet, self.addr)


    def _read_floats(self, count: int):

        if self.sock is None:
            raise RuntimeError("UDP not connected")

        try:
            data, _ = self.sock.recvfrom(128)

            if len(data) != 4 * count:
                return False, tuple([0.0] * count)

        except socket.timeout:
            return False, tuple([0.0] * count)

        return True, struct.unpack("<" + "f" * count, data)


    # ------------- GENERIC FUNCTIONS ------------------

    def write_data1(self, cmd: int, val: float):
        payload = struct.pack("<f", val)
        self._send_packet(cmd, payload)

    def read_data1(self, cmd: int):
        self._send_packet(cmd)
        success, (val,) = self._read_floats(1)
        return success, val

    def write_data2(self, cmd: int, a: float, b: float):
        payload = struct.pack("<ff", a, b)
        self._send_packet(cmd, payload)

    def write_data3(self, cmd: int, a: float, b: float, c: float):
        payload = struct.pack("<fff", a, b, c)
        self._send_packet(cmd, payload)

    def read_data11(self, cmd: int):
        self._send_packet(cmd)
        success, vals = self._read_floats(11)
        return success, vals
    
    def constrain(self, data: int, min_val: int, max_val: int):
        return max(min_val, min(data, max_val))
    
    def map(self, x: int, in_min: int, in_max: int, out_min: int, out_max: int):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

    # ------------------ SEND FUNCTIONS ------------------

    def writeServoAngle(self, angle_deg: int):
        angle = self.constrain(angle_deg, -90, 90)
        self.write_data1(self.WRITE_SERVO_ANGLE, float(angle))

    def writeGripperAngle(self, angle_deg: int):
        angle = self.constrain(angle_deg, 0, 75)
        self.write_data1(self.WRITE_GRIPPER_ANGLE, float(angle))

    def writeGripperDist(self, dist_mm: int):
        dist = self.constrain(dist_mm, 15, 55)
        self.write_data1(self.WRITE_GRIPPER_DIST, float(dist))

    def buzzerOn(self):
        self.write_data1(self.WRITE_BUZZER, 1.0)

    def buzzerOff(self):
        self.write_data1(self.WRITE_BUZZER, 0.0)

    def ledOn(self):
        self.write_data1(self.WRITE_LED, 1.0)

    def ledOff(self):
        self.write_data1(self.WRITE_LED, 0.0)

    def rgbOn(self, r_pwm: int, g_pwm: int, b_pwm: int):
        r_val = self.constrain(r_pwm, 0, 255)
        g_val = self.constrain(g_pwm, 0, 255)
        b_val = self.constrain(b_pwm, 0, 255)
        self.write_data3(self.WRITE_RGB_LED, float(r_val), float(g_val), float(b_val))

    def rgbOff(self):
        self.write_data3(self.WRITE_RGB_LED, 0.0, 0.0, 0.0)

    def writeMotorPwm(self, l_pwm: int, r_pwm: int):
        self.is_pwm_mode = True
        self.write_data2(self.WRITE_MOTOR_PWM, l_pwm, r_pwm)

    def writeMotorVel(self, wl: float, wr: float):
        self.is_pwm_mode = False
        self.write_data2(self.WRITE_MOTOR_VEL, wl, wr)
    
    def writeRobotVel(self, v: float, w: float):
        self.is_pwm_mode = False
        self.write_data2(self.WRITE_CMD_VEL, v, w)

    def setWheelOdomParams(self, R_mm: int, L_mm: int):
        self.write_data2(self.SET_WHEEL_ODOM_PARAMS, float(R_mm), float(L_mm))
    
    def clearControllerData(self):
        success, _ = self.read_data1(self.CLEAR_CONTROLLER_DATA)
        return success
    
    def setControllerCmdTimeout(self, timeout_ms: int):
        self.write_data1(self.SET_CONTROLLER_CMD_TIMEOUT, float(timeout_ms))

    def setUdpConnTimeout(self, timeout_ms: int):
        self.write_data1(self.SET_UDP_CONN_TIMEOUT, float(timeout_ms))
    
    def udpHeartBeat(self):
        self.write_data1(self.UDP_HEART_BEAT, 0.0)

    def resetParams(self):
        success, _ = self.read_data1(self.RESET_PARAMS)
        return success

    def setWheelRadiusParam(self, wheel_radius: float):
        self.write_data1(self.SET_WHEEL_RADIUS, wheel_radius)
    
    def setWheelDistanceParam(self, wheel_dist: float):
        self.write_data1(self.SET_WHEEL_DISTANCE, wheel_dist)

    def stop(self):
        if self.is_pwm_mode:
            self.writeMotorPwm(0, 0)
        else:
            self.writeMotorVel(0.0, 0.0)

    # ------------------ READ DATA FUNCTIONS ------------------

    def readData(self):
        success, vals = self.read_data11(self.READ_DATA)
        return success, tuple(round(v, 4) for v in vals)

    def readSonar(self) -> int:
        with self._lock:
            return int(self.sonar_val)
        
    def readTOF(self) -> int:
        with self._lock:
            return int(self.tof_val)
        
    def readLineSensorVal(self) -> int:
        with self._lock:
            return self.line_sensor_val
        
    def readLeftMotorAnglePos(self) -> float:
        with self._lock:
            return self.tl_val
    
    def readRightMotorAnglePos(self) -> float:
        with self._lock:
            return self.tr_val
        
    def readRobotTurn(self) -> float:
        with self._lock:
            return self.yaw_val
        
    def readRobotDist(self) -> float:
        with self._lock:
            return self.dist_val
        
    def readColorSensorVal(self) -> int:
        with self._lock:
            return int(self.color_sensor_val)
        
    def readWheelRadiusParam(self) -> float:
        with self._lock:
            return self.wheel_radius_param_val
        
    def readWheelDistParam(self) -> float:
        with self._lock:
            return self.wheel_dist_param_val
        
    def readMaxMotorSpeedParam(self) -> float:
        with self._lock:
            return self.max_motor_speed_val
    
    # ------------------ HIGH-LEVEL FUNCTIONS ------------------

    def readLineSensorArray(self) -> list[int]:
        data = self.readLineSensorVal()
        data = self.constrain(data, 0, 255)
        bit_array = [(data >> i) & 1 for i in reversed(range(8))]
        return bit_array[-5:]
    
    def isLineDetected(self, sensor_num) -> bool:
        num = self.constrain(sensor_num, 0, 4)
        data = self.readLineSensorArray()
        if data[num]:
            return True
        else:
            return False

    def readRobotDist_mm(self) -> int:
        return int(self.readRobotDist()*1000.0)
    
    def readRobotTurn_deg(self) -> int:
        return int(self.readRobotTurn()*180/pi)
    
    def setGripperOpenPercent(self, percent):
        self.percent_gripper_open = percent

    def gripperActionOpen(self):
        open_dist_mm = self.map(self.percent_gripper_open, 0, 100, 15, 55)
        self.writeGripperDist(open_dist_mm)

    def gripperActionClose(self):
        self.writeGripperDist(15)
    
    def setDriveSpeedPercent(self, percent):
        self.percent_drive_speed = percent

    def setTurnSpeedPercent(self, percent):
        self.percent_turn_speed = percent

    def setDriveVel(self):
        # max_drive_vel = self.max_motor_speed_val * self.wheel_radius_param_val
        max_drive_vel = 10.0 * self.wheel_radius_param_val
        self.drive_vel = round((max_drive_vel*self.percent_drive_speed)/100.0, 3)

    def setTurnVel(self):
        # max_drive_vel = self.max_motor_speed_val * self.wheel_radius_param_val
        max_drive_vel = 10.0 * self.wheel_radius_param_val
        max_turn_vel = (max_drive_vel*2) / self.wheel_dist_param_val
        self.turn_vel = round((max_turn_vel*self.percent_turn_speed)/100.0, 3)

    def drive(self, direction):
        dir = 0.0
        if direction >= 0 :
            dir = 1.0
        else:
            dir = -1.0
        
        self.setDriveVel()
        self.writeRobotVel(dir*self.drive_vel, 0.0)
    
    def driveFor(self, direction, dist_mm):
        dir = 0.0
        dist = self.readRobotDist_mm()
        if direction >= 0 :
            dir = 1.0
        else:
            dir = -1.0

        self.setDriveVel()
        while abs(self.readRobotDist_mm() - dist) < dist_mm :
            self.writeRobotVel(dir*self.drive_vel, 0.0)
            sleep(0.05)

        self.stop()

    def turn(self, direction):
        dir = 0.0
        if direction >= 0 :
            dir = 1.0
        else:
            dir = -1.0

        self.setTurnVel()
        self.writeRobotVel(0.0, dir*self.turn_vel)

    def turnFor(self, direction, turn_deg):
        dir = 0.0
        angle = self.readRobotTurn_deg()
        if direction >= 0 :
            dir = 1.0
        else:
            dir = -1.0

        self.setTurnVel()
        while abs(self.readRobotTurn_deg() - angle) < turn_deg :
            self.writeRobotVel(0.0, dir*self.turn_vel)
            sleep(0.05)

        self.stop()

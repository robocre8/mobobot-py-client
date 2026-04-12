import socket
import struct
from time import sleep, time
from math import pi
import threading


class TexaBotClient:

    def __init__(self):
        self.START_BYTE = 0xAA
        self.WRITE_SERVO1_ANGLE = 0x01
        self.WRITE_SERVO2_ANGLE = 0x02
        self.WRITE_BUZZER = 0x03
        self.WRITE_RGB = 0x04
        self.WRITE_MOTOR_VEL = 0X05
        self.WRITE_MOTOR_PWM = 0X06
        self.WRITE_CMD_VEL = 0x07
        self.SET_WHEEL_ODOM_PARAMS = 0X08
        self.GET_WHEEL_ODOM_PARAMS = 0X09
        self.READ_SONAR = 0x0A
        self.READ_LINE_SENSOR1 = 0x0B
        self.READ_LINE_SENSOR2 = 0x0C
        self.READ_MOTOR_STATES = 0X0D
        self.READ_ODOM_DATA = 0X0E
        self.READ_ALL_SENSORS = 0X0F
        self.CLEAR_CONTROLLER_DATA = 0X10
        self.SET_CONTROLLER_CMD_TIMEOUT = 0X11
        self.SET_UDP_CONN_TIMEOUT = 0X12
        self.GET_UDP_CONN_TIMEOUT = 0X13
        self.UDP_HEART_BEAT = 0X14


        self.sock: socket.socket | None = None
        self.addr = None
        self.timeout = 0.2
        self.heartbeat_running = True

        self._lock = threading.Lock()


        self.sonar_read: int = 0

        self.line_sensor1_read: int = 0
        self.line_sensor2_read: int = 0

        self.left_wheel_angle_read: float = 0.0
        self.right_wheel_angle_read: float = 0.0

        self.robot_angle_read: float = 0.0
        self.robot_dist_read: float = 0.0

        self.is_pwm_mode: bool = False
        


    # ------------------ CONNECT ------------------
    def connect(self, ip: str, port: int = 8888, timeout: float = 0.2):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(timeout)
        
        self.addr = (ip, port)

        sleep(3.0)
        for _ in range(10):
            success = self.clearControllerData()
            if success:
                print("TexaBot Connected Successfully")
                return
            sleep(0.1)

        self.disconnect()
        raise RuntimeError("Could not connect to TexaBot, Try Again")


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
                    success, sensor_data = self.readAllSensors()

                    if success:
                        with self._lock:
                            self.sonar_read = int(sensor_data[0])
                            
                            self.line_sensor1_read = int(sensor_data[1])
                            self.line_sensor2_read = int(sensor_data[2])

                            self.left_wheel_angle_read = sensor_data[3]
                            self.right_wheel_angle_read = sensor_data[4]
                            self.robot_angle_read = sensor_data[5]
                            self.robot_dist_read = sensor_data[6]

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

    def read_data2(self, cmd: int):
        self._send_packet(cmd)
        success, vals = self._read_floats(2)
        return success, vals

    def write_data3(self, cmd: int, a: float, b: float, c: float):
        payload = struct.pack("<fff", a, b, c)
        self._send_packet(cmd, payload)

    def read_data4(self, cmd: int):
        self._send_packet(cmd)
        success, vals = self._read_floats(4)
        return success, vals

    def read_data7(self, cmd: int):
        self._send_packet(cmd)
        success, vals = self._read_floats(7)
        return success, vals

    # ------------------ GENARL FUNCTIONS ------------------

    def writeServo1Angle(self, angle_deg: int):
        self.write_data1(self.WRITE_SERVO1_ANGLE, float(angle_deg))

    def writeServo2Angle(self, angle_deg: int):
        self.write_data1(self.WRITE_SERVO2_ANGLE, float(angle_deg))

    def writeBuzzer(self, pwm: int):
        self.write_data1(self.WRITE_BUZZER, float(pwm))

    def writeRGB(self, r_pwm: int, g_pwm: int, b_pwm: int):
        self.write_data3(self.WRITE_RGB, float(r_pwm), float(g_pwm), float(b_pwm))

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
    
    def getWheelOdomParams(self):
        success, vals = self.read_data2(self.GET_WHEEL_ODOM_PARAMS)
        return success, tuple(round(v, 4) for v in vals)

    def readLeftWheelAngle(self) -> int:
        with self._lock:
            return int(self.left_wheel_angle_read*180/pi)
    
    def readRightWheelAngle(self) -> int:
        with self._lock:
            return int(self.right_wheel_angle_read*180/pi)
        
    def readRobotDist(self) -> int:
        with self._lock:
            return int(self.left_wheel_angle_read*1000)
        
    def readRobotAngle(self) -> int:
        with self._lock:
            return int(self.left_wheel_angle_read*180/pi)
    
    def readAllSensors(self):
        success, vals = self.read_data7(self.READ_ALL_SENSORS)
        return success, tuple(round(v, 4) for v in vals)
    
    def clearControllerData(self):
        success, _ = self.read_data1(self.CLEAR_CONTROLLER_DATA)
        return success
    
    def setControllerCmdTimeout(self, timeout_ms: int):
        self.write_data1(self.SET_CONTROLLER_CMD_TIMEOUT, float(timeout_ms))

    def setUdpConnTimeout(self, timeout_ms: int):
        self.write_data1(self.SET_UDP_CONN_TIMEOUT, float(timeout_ms))

    def getUdpConnTimeout(self):
        success, timeout_ms = self.read_data1(self.GET_UDP_CONN_TIMEOUT)
        return success, int(timeout_ms)
    
    def udpHeartBeat(self):
        self.write_data1(self.UDP_HEART_BEAT, 0.0)
    
    # ------------------ HIGH-LEVEL FUNCTIONS ------------------

    def buzzerOn(self):
        self.writeBuzzer(1)
    
    def buzzerOff(self):
        self.writeBuzzer(0)

    def buzzerBeep(self, beep_time_ms: int):
        self.writeBuzzer(beep_time_ms)

    def rgbOn(self, r: int, g: int, b: int):
        self.writeRGB(r, g, b)

    def rgbOff(self):
        self.writeRGB(0, 0, 0)

    def readSonar(self) -> int:
        with self._lock:
            return self.sonar_read
        
    def readLineSensor1(self) -> int:
        with self._lock:
            return self.line_sensor1_read
        
    def readLineSensor2(self) -> int:
        with self._lock:
            return self.line_sensor2_read
        
    def stop(self):
        if self.is_pwm_mode:
            self.writeMotorPwm(0, 0)
        else:
            self.writeMotorVel(0.0, 0.0)
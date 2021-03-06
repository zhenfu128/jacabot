#! /usr/bin/env/python3

import time
import RPi.GPIO as GPIO
import rospy
# from geometry_msgs.msg import Twist


"""Defining of minimum and maximum values of PWM"""
_min_speed = 0
MIN_SPEED  = _min_speed
_max_speed = 100  
MAX_SPEED  = _max_speed

"""Defined pins of motors"""
# PWA     = 17
# AI1     = 27
# AI2     = 22
# PWB     = 18
# BI1     = 24
# BI2     = 23
# freq    = 100
# standby = 25 

class Motor:
    MAX_SPEED = _max_speed

    def __init__(self, pwm_pin, pin_one, pin_two, freq, name):
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.name    = name
        self.pwm_pin = pwm_pin
        self.pin_one = pin_one
        self.pin_two = pin_two
        self.freq    = freq

        GPIO.setup(self.pin_one, GPIO.OUT)
        GPIO.setup(self.pin_two, GPIO.OUT)
        GPIO.setup(self.pwm_pin, GPIO.OUT)

        self.my_pwm = GPIO.PWM(self.pwm_pin, self.freq)
        self.last_pwm = 0
        self.my_pwm.start(self.last_pwm)

        print("{} has been initialized.".format(self.name))

    def standby(self, standby_pin, standby_state=True):
        """Turn on/Turn off standby mode of motor driver"""
        self.standby_pin = standby_pin

        GPIO.setup(self.standby_pin, GPIO.OUT)

        if standby_state is False:
            GPIO.output(self.standby_pin, False)
        else:
            GPIO.output(self.standby_pin, True)
        
    def setSpeed(self, speed):
        """The direction of operation of the motors depends 
            on the value of the positive and negative speed"""
        if speed < 0:
            speed = -speed
            GPIO.output(self.pin_one, False)
            GPIO.output(self.pin_two, True)
        else:
            GPIO.output(self.pin_one, True)
            GPIO.output(self.pin_two, False)

        if speed > MAX_SPEED:
            speed = MAX_SPEED
        
        if speed != self.last_pwm:
            self.my_pwm.ChangeDutyCycle(speed)
            self.last_pwm = speed

    def brake(self, speed):
        GPIO.output(self.pin_one, True)
        GPIO.output(self.pin_two, True)

        if speed != self.last_pwm:
            self.my_pwm.ChangeDutyCycle(speed)
            self.last_pwm = speed



class Driver:
    def __init__(self):

        rospy.init_node('driver')

        self._last_received = rospy.get_time()
        self._timeout = rospy.get_param('~timeout', 2)
        self._rate = rospy.get_param('~rate', 10)
        self._max_speed = rospy.get_param('~max_speed', 0.5)
        self._wheel_base = rospy.get_param('~wheel_base', 0.09)

        # Assign pins to motors. These may be distributed
        # differently depending on how you've built your robot
        self.right_motor = Motor(pwm_pin=17, pin_one=27, pin_two=22, freq=100, name="Left motor")
        self.right_motor.standby(standby_pin=25, standby_state=True)
        self.left_motor  = Motor(pwm_pin=18, pin_one=23, pin_two=24, freq=100, name="Right motor")
        self.left_motor.standby(standby_pin=25, standby_state=True)

        self._left_speed_percent = 0
        self._right_speed_percent = 0

        # Setup subscriber for velocity twist message
        rospy.Subscriber(
            'cmd_vel', Twist, self._velocity_received_callback)

    def _velocity_received_callback(self, message):
        """Handle new velocity command message."""

        self._last_received = rospy.get_time()

        # Extract linear and angular velocities from the message
        linear = message.linear.x
        angular = message.angular.z

        # Calculate wheel speeds in m/s
        left_speed = linear - angular*self._wheel_base/2
        right_speed = linear + angular*self._wheel_base/2

        # Ideally we'd now use the desired wheel speeds along
        # with data from wheel speed sensors to come up with the
        # power we need to apply to the wheels, but we don't have
        # wheel speed sensors. Instead, we'll simply convert m/s
        # into percent of maximum wheel speed, which gives us a
        # duty cycle that we can apply to each motor.
        self._left_speed_percent = (100 * left_speed/self._max_speed)
        self._right_speed_percent = (100 * right_speed/self._max_speed)

    def run(self):
        """The control loop of the driver."""

        rate = rospy.Rate(self._rate)

        while not rospy.is_shutdown():
            # If we haven't received new commands for a while, we
            # may have lost contact with the commander-- stop
            # moving
            delay = rospy.get_time() - self._last_received
            if delay < self._timeout:
                self._left_motor.setSpeed(self._left_speed_percent)
                self._right_motor.setSpeed(self._right_speed_percent)
            else:
                self._left_motor.setSpeed(0)
                self._right_motor.setSpeed(0)

            rate.sleep()


def main():
    driver = Driver()

    # Run driver. This will block
    driver.run()

    GPIO.cleanup()

def test():
    right_motor = Motor(pwm_pin=17, pin_one=27, pin_two=22, freq=100, name="Left motor")
    right_motor.standby(standby_pin=25, standby_state=True)
    time.sleep(0.5)
    left_motor  = Motor(pwm_pin=18, pin_one=23, pin_two=24, freq=100, name="Right motor")
    left_motor.standby(standby_pin=25, standby_state=True)
    time.sleep(0.5)
    while True:
        left_motor.setSpeed(MAX_SPEED)
        right_motor.setSpeed(MAX_SPEED)


if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        print("CTRL-C: Terminating program.")
        GPIO.cleanup()
        exit()
    except Exception as error:
        print(error)
        print("Unexpected error:")
        GPIO.cleanup()
    finally:
        GPIO.cleanup()
        exit()
exit()

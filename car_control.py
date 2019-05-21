#encoding: utf-8
import RPi.GPIO as GPIO
import time
from car import Car
from car_servo import Car_Servo
# 设定速度，满电时速度太快，图像处理速度跟不上
# 直行快一点，转向慢一点
speed1 = 100          # 直行速度
speed2 = 100          # 拐弯速度
#angle = 90
# # 轮子定义
# backMotorinput1 = 12   #后轮1
# backMotorinput2 = 11   #后轮2

car = Car()
car_servo = Car_Servo()

# frontMotorinput1 = 18    #前轮1


# backMotorEn = 12    #使能端口1
# frontMotorEn = 16    #使能端口2


# GPIO.setmode(GPIO.BOARD)                         # 设置模式
# GPIO.setup(backMotorinput1,GPIO.OUT)             # 此端口为输出模式
# GPIO.setup(backMotorinput2,GPIO.OUT)             # 此端口为输出模式
# GPIO.setup(frontMotorinput1,GPIO.OUT)            # 此端口为输出模式
# GPIO.setup(frontMotorinput2,GPIO.OUT)            # 此端口为输出模式
# GPIO.setup(backMotorEn,GPIO.OUT)
# GPIO.setup(frontMotorEn,GPIO.OUT)
# 将控制小车运动封装为函数
# backMotorPwm = GPIO.PWM(backMotorEn,100)         # 配置PWM
# backMotorPwm.start(0)                            # 开始输出PWM
# 当使能端口输入低电压时，电机驱动板将不对电机输出电流，电机将不工作。
# 当使能端口输入高电压时，让前轮转向电机正常工作。
# 向前走
# def set_duty_cycle(self, duty = 40):
#         '''
#         Set duty of the pwm
#         '''
#         self.duty=duty
#         if self.duty <0 :
#             self.pwmIN1.ChangeDutyCycle(0)
#             self.pwmIN2.ChangeDutyCycle(-self.duty)
#         else :
#             self.pwmIN1.ChangeDutyCycle(self.duty)
#             self.pwmIN2.ChangeDutyCycle(0) 
def car_move_forward():
    car.set_duty_cycle(speed1)

    # GPIO.ChangeDutyCycle(backMotorinput1,40)
    # GPIO.output(backMotorinput2,GPIO.LOW)
    # backMotorPwm.ChangeDutyCycle(speed1)         # 改变PWM占空比，参数为占空比
# 向后退
def car_move_backward():
    car.set_duty_cycle(-speed1)

    # GPIO.output(backMotorinput1,GPIO.LOW)
    # GPIO.output(backMotorinput2,GPIO.HIGH)
    # backMotorPwm.ChangeDutyCycle(speed2)
# 左拐
def car_turn_left(angle):
    car.set_duty_cycle(speed2)
    print (angle)
    car_servo.set_angle(angle)





    # GPIO.output(frontMotorEn,GPIO.HIGH)    # 当使能端口输入高电压时，让前轮转向电机正常工作。
    # GPIO.output(frontMotorinput1,GPIO.HIGH)
    # GPIO.output(frontMotorinput2,GPIO.LOW)
    # GPIO.output(backMotorinput1,GPIO.HIGH)
    # GPIO.output(backMotorinput2,GPIO.LOW)
    # backMotorPwm.ChangeDutyCycle(speed2)
# 右拐    
def car_turn_right(angle):
    car.set_duty_cycle(speed2)
    print (angle)
    
    car_servo.set_angle(angle)


    # GPIO.output(frontMotorEn,GPIO.HIGH)    # 当使能端口输入高电压时，让前轮转向电机正常工作。
    # GPIO.output(frontMotorinput1,GPIO.LOW)
    # GPIO.output(frontMotorinput2,GPIO.HIGH)
    # GPIO.output(backMotorinput1,GPIO.HIGH)
    # GPIO.output(backMotorinput2,GPIO.LOW)
    # backMotorPwm.ChangeDutyCycle(speed2)
# 
def carbackleft():
    GPIO.output(frontMotorEn,GPIO.HIGH)    # 当使能端口输入高电压时，让前轮转向电机正常工作。
    GPIO.output(frontMotorinput1,GPIO.HIGH)
    GPIO.output(frontMotorinput2,GPIO.LOW)
    GPIO.output(backMotorinput1,GPIO.LOW)
    GPIO.output(backMotorinput2,GPIO.HIGH)
    backMotorPwm.ChangeDutyCycle(speed2)
# 
#def carbackRight():
#    GPIO.output(frontMotorEn,GPIO.HIGH)    # 当使能端口输入高电压时，让前轮转向电机正常工作。
#    GPIO.output(frontMotorinput1,GPIO.LOW)
#    GPIO.output(frontMotorinput2,GPIO.HIGH)
#    GPIO.output(backMotorinput1,GPIO.LOW)
#    GPIO.output(backMotorinput2,GPIO.HIGH)
#    backMotorPwm.ChangeDutyCycle(speed2)
# 清除
def clean_GPIO():
    GPIO.cleanup()
    backMotorPwm.stop()                          # 停止输出PWM
# 前轮回正函数
#def car_turn_straight():
#    GPIO.output(frontMotorEn,GPIO.LOW)    # 当使能端口输入低电压时，电机驱动板将不对电机输出电流，电机将不工作。
#    time.sleep(0.05)
# 停止
def car_stop():
    car.set_duty_cycle(0)
    #GPIO.output(backMotorinput1,GPIO.LOW)
    #GPIO.output(backMotorinput2,GPIO.LOW)
    #GPIO.output(frontMotorEn,GPIO.LOW)

if __name__ == '__main__':
    car_turn_straight()
    car_move_forward()
    time.sleep(10)
    clean_GPIO()

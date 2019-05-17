#!/usr/bin/python
#coding: utf8
import RPi.GPIO as GPIO
import time
import sys
import threading
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
import json
import signal
import atexit
import os
import socket

GPIO.setmode(GPIO.BOARD)#设置GPIO口模式

#设置舵机pin脚接口
engine_x =38#水平舵机
engine_y =37#垂直舵机
#舵机初始化
GPIO.setup(engine_x,GPIO.OUT,initial=False)
GPIO.setup(engine_y,GPIO.OUT,initial=False)
#设置PWM信号频率
px=GPIO.PWM(engine_x,60)
py=GPIO.PWM(engine_y,60)
px.start(0)
py.start(0)


#定义socket类型
raspiServer=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#定义socket类型，网络通信
raspiServer.bind(('',8266))

#设置超声波pin脚接口
fasong  =36
jieshou =40
#管脚模式
GPIO.setup(fasong,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(jieshou,GPIO.IN)
class Info:
	@staticmethod
	def p(message):
		print 'Info: '+message 


#--------------------------------------------电机---------------------------------------------

#Wheel封装的单个车轮的所有可能操作
class Wheel:
	pins ={'a':[11,12],'b':[13,15]}
	def __init__(self,name):
		self.name = name
		print "name=",name
		self.pin = Wheel.pins[self.name]
		GPIO.setup(self.pin[0],GPIO.OUT)
		GPIO.setup(self.pin[1],GPIO.OUT)
		self.stop()
	def st(self):
		print 'ss'
	def forward(self):
		Info.p('wheel ' + self.name + ' is forwarding')
		GPIO.output(self.pin[0],GPIO.LOW)
		GPIO.output(self.pin[1],GPIO.HIGH)
	def stop(self):
		GPIO.output(self.pin[0],False)
		GPIO.output(self.pin[1],False)
	def back(self):
		Info.p('wheel ' +self.name + ' is backing')
		GPIO.output(self.pin[0],GPIO.HIGH)
		GPIO.output(self.pin[1],GPIO.LOW)
#Car组合四个轮子所有可能操作		
class Car:
	wheel=[Wheel('a'),Wheel('b')] 
	@staticmethod
	def init():
		GPIO.setmode(GPIO.BOARD)
		Info.p('initialize the smart car ....')		
		Info.p('Smart car is ready to fly!')
	@staticmethod
	def forward():
		Info.p('go straight forward')
		for wheel in Car.wheel:
			wheel.forward()
	@staticmethod
	def back():
		Info.p('go straight back')
		for wheel in Car.wheel:
			wheel.back()
	@staticmethod
	def left():
		print 'left'
		Info.p('turn left ')
		Car.wheel[0].forward()	
		Car.wheel[1].back()
	@staticmethod
	def right():
		print 'right'
		Info.p('turn left ')
		Car.wheel[1].forward()	
		Car.wheel[0].back()
	@staticmethod
	def stop():
		Info.p('turn left ')
		Car.wheel[0].stop()	
		Car.wheel[1].stop()	
	@staticmethod
	def stop():
		Info.p('try to stop the car ...')
		for wheel in Car.wheel:
			wheel.stop()	
#关闭GPIO接口
def close_car():
    global stop_status
    stop_status = 1
    GPIO.cleanup()
#--------------------------------------------舵机自由角度模式---------------------------------------------
#右转
def rightEngine():
 #for i in range(0,181,10):
 while(True):
  print 'rightEngine'
  global stop_status
  print 'right'
  if stop_status==1:break
  px.ChangeDutyCycle(12.5/180)
  time.sleep(0.03)#等待20ms周期结束                      
  px.ChangeDutyCycle(0)                 
  #time.sleep(0.07)#每次移动后停止的时间  
#左转 
def leftEngine():
 #for i in range(181,0,-10):
 while(True):
  print 'leftEngine'
  global stop_status
  if stop_status==1:break
  px.ChangeDutyCycle(2.5+10*220/ 180) 
  time.sleep(0.03)#等待20ms周期结束                      
  px.ChangeDutyCycle(0)                 
  #time.sleep(0.07)#每次移动后停止的时间 
#向上
def upwardEngine():
 #for i in range(181,0,-10):
 while(True):
  print 'upwardEngine'
  global stop_status
  if stop_status==1:break
  global stop_status
  py.ChangeDutyCycle(2.5+10/ 180) 
  time.sleep(0.03)#等待20ms周期结束                      
  py.ChangeDutyCycle(0)                 
  time.sleep(0)#每次移动后停止的时间
#向下
def downEngine():
 #for i in range(0,181,10):
 while(True):
  print 'downEngine'
  global stop_status
  if stop_status==1:break
  global stop_status
  py.ChangeDutyCycle(2.5+10*220/ 180) 
  time.sleep(0.03)#等待20ms周期结束
  py.ChangeDutyCycle(0)	
  time.sleep(0)#每次移动后停止的时间
 
#--------------------------------------------舵机固定角度模式---------------------------------------------
#固定左边
def fixedLeft():
  print 'fixedLeft'
  px.ChangeDutyCycle(12.2)#设置脉宽比
  time.sleep(0.45)#等待20ms周期结束                      
  px.ChangeDutyCycle(0)
#固定右边
def fixedright():
  print 'fixedright'
  px.ChangeDutyCycle(2.2)#设置脉宽比
  time.sleep(0.45)#等待20ms周期结束                      
  px.ChangeDutyCycle(0)
  
#固定中间
def fixedCenter():
  print 'fixedCenter'
  px.ChangeDutyCycle(6.7)#设置脉宽比
  py.ChangeDutyCycle(6.4)#设置脉宽比
  time.sleep(0.45)#等待20ms周期结束                      
  px.ChangeDutyCycle(0)                    
  py.ChangeDutyCycle(0) 
  
#--------------------------------------------超声波---------------------------------------------
#打开超声波
def openUltrasonic(conn):
 print 'openUltrasonic'
 while (True):
  GPIO.output(fasong,GPIO.HIGH)
  time.sleep(0.000015)
  GPIO.output(fasong,GPIO.LOW)
  print '发送成功'
 while not GPIO.input(jieshou):
  pass
 t1= time.time()
 while GPIO.input(jieshou):
  pass
 t2=time.time()
 print "接收超声波完毕"
 distance= (t2-t1)*340/2
 conn.send(distance)
  
#关闭超声波
def shudownUltrasonic():
 print 'shudownUltrasonic'
 global stop_Ultrasonic
 stop_Ultrasonic=1
  
global conn
def initSocket():
 global stop_status
 global stop_Ultrasonic
 print 'listening on 8266'
 #步骤3：开始TCP监听
 while 1:
  raspiServer.listen(1)#监听
  print '监听程序中……'
  while 1:
   print("正在等待……")
   conn,addr=raspiServer.accept()
   print ('connect by',addr)
   while 1:
    manager=conn.recv(258).replace('\n','')#接收数据
    if not manager:
     break
    print manager
    if manager=='0X01':
	 stop_status=0
	 client=threading.Thread(target=Car.forward())
	 client.setDaemon(True)
	 client.start()
    elif manager=='0X10':
     Car.stop()
    elif manager=='0X02':
	 stop_status=0
	 client=threading.Thread(target=Car.back())
	 client.setDaemon(True)
	 client.start()
    elif manager=='0X20':
     Car.stop()
    elif manager=='0X03':
	 stop_status=0
	 print 'left'
	 client=threading.Thread(target=Car.left())
	 client.setDaemon(True)
	 client.start()
    elif manager=='0X30':
     Car.stop()
    elif manager=='0X04':
	 stop_status=0
	 client=threading.Thread(target=Car.right())
	 client.setDaemon(True)
	 client.start()
    elif manager=='0X40':
     Car.stop()
    #舵机
    elif manager=='0X05':
     stop_status=0
     client = threading.Thread(target = upwardEngine)
     client.setDaemon(True)
     client.start()
    elif manager=='0X50':
     print 'stop server'
     stop_status=1
    elif manager=='0X06':
     stop_status=0
     client = threading.Thread(target = downEngine)
     client.setDaemon(True)
     client.start()     
    elif manager=='0X60':
     print 'stop server'
     stop_status=1
    elif manager=='0X07':
     stop_status=0	
     client = threading.Thread(target = leftEngine)
     client.setDaemon(True)
     client.start()
    elif manager=='0X70':
     print 'stop server'
     stop_status=1       
    elif manager=='0X08':
     stop_status=0
     client = threading.Thread(target = rightEngine)
     client.setDaemon(True)
     client.start() 
    elif manager=='0X80':
     print 'stop server'
     stop_status=1 	 
	#自由
    elif manager=='0X09':
     client = threading.Thread(target = fixedLeft)
     client.setDaemon(True)
     client.start()    
    elif manager=='0X0A':
     client = threading.Thread(target = fixedright)
     client.setDaemon(True)
     client.start()
	#复位
    elif manager=='0XA1':
     client = threading.Thread(target = fixedCenter)
     client.setDaemon(True)
     client.start()
	#超声波
    elif manager=='0XA2':
     #stop_Ultrasonic=0
     #client = threading.Thread(target = openUltrasonic,args=(conn,))
     #client.setDaemon(True)
     #client.start()
     conn.send('a')	 
    elif manager=='0X2A':
     stop_Ultrasonic=1
	 
    else:
     print 'error'	
   conn.close()

client=threading.Thread(target=initSocket)

atexit.register(raspiServer.close)

if __name__ == '__main__':
 print 'this is python!'

 initSocket()

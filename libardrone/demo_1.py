# Python AR.Drone 2.0
#
# Copyright (C) 2013 Quadeare <lacrampe.florian@gmail.com>
# Twitter : @quadeare

from pygame import *  
import pygame
import libardrone
import threading
import time
from subprocess import call

import signal 
import sys

import ctypes
from sdl2 import *

#--disable-input-events

#Define joystick centre deadzone
xDeadZone = 0
yDeadZone = 0
zDeadZone = 0

class video(threading.Thread):
    """Video class to launch media flux"""
    def __init__(self, nom = ''):
        threading.Thread.__init__(self)
        self.process = None
    def run(self):
        print "Video"
        call(["ffplay", "http://192.168.1.1:5555/"])
    def stop(self):
        call(["killall", "ffplay"])
        if self.process is not None:
            self.process.terminate()
            self.process = None

class controle(threading.Thread):
    """Control class (to control the drone)"""
    def __init__(self, nom = ''):
        threading.Thread.__init__(self)
        self._stopevent = threading.Event( )
    def stop(self):
        self._stopevent.set( )
    def run(self):

        """We call pygame (to use controler)"""

        #pygame.init()
        SDL_Init( SDL_INIT_JOYSTICK )
        
        """Launch drone class"""
        drone = libardrone.ARDrone(True)
        clock = pygame.time.Clock()
        running = True

        """Set up and init joystick"""
        #j=joystick.Joystick(0) 
        #j.init()

        gGameController = SDL_JoystickOpen( 0 )

        move_forward = 0
        move_backward = 0
        move_left = 0
        move_right = 0
        yaw_left = 0
        yaw_right = 0
        turn = 0
        xvalue = 0
        yvalue = 0
        zvalue = 0
        event = SDL_Event()
        time_1 = time.time()
        while running:
            #for event in pygame.event.get():
            while SDL_PollEvent(ctypes.byref(event)) != 0:
                                
                if event.type == SDL_JOYBUTTONDOWN:
                    
                    # takeoff
                    #if SDL_JoystickGetButton (gGameController, 7) == 1:
		    if event.jbutton.button == 7:
                        print "Take Off !"
                        drone.takeoff()
                    
                    # Land
                    elif event.jbutton.button == 2:
                        print "Land !"
                        drone.land()

                    # Stop and land
                    elif event.jbutton.button == 6:
                        print "Stop and Land !"
                        drone.land()
                        running = False
                    
		    # Altitude UP
                    elif event.jbutton.button == 3:
                        print "Altitude UP"
                        drone.speed = 1
                        drone.move_up()

                    # Altitude Down
                    elif event.jbutton.button == 0:
                        print "Altitude Down"
                        drone.speed = 1
                        drone.move_down()

                    # Emmergency
                    elif event.jbutton.button == 1:
                        print "Emergency !"
                        drone.reset()
                        
                if event.type == SDL_JOYBUTTONUP:
                    # Altitude UP
                    if event.jbutton.button == 3 :
                        print "Altitude UP STOP !"
                        drone.speed = 0
                        drone.hover()
                    # Altitude Down
                    elif event.jbutton.button == 0:
                        print "Altitude Down STOP !"
                        drone.speed = 0
                        drone.hover()
                          
                            
                #if event.type == pygame.JOYAXISMOTION:
                if event.type == SDL_JOYAXISMOTION:

                    '''
                    xvalue = SDL_JoystickGetAxis(gGameController, 0) / 32768.0
                    yvalue = SDL_JoystickGetAxis(gGameController, 1) / 32768.0
                    zvalue = SDL_JoystickGetAxis(gGameController, 3) / 32768.0
                    '''
                    if event.jaxis.axis == 0:
                        xvalue = event.jaxis.value / 32768.0
                    elif event.jaxis.axis == 1:
                        yvalue = event.jaxis.value / 32768.0
                    elif event.jaxis.axis == 3:
                        zvalue = event.jaxis.value / 32768.0                        
                    '''
                    if xvalue < -xDeadZone :
                        xDir = -1
                    elif xv > xDeadZone :
                        xDir = 1
                    else :
                        xDir = 0

                    if yv < -yDeadZone :
                        yDir = -1
                    elif yv > yDeadZone :
                        yDir = 1
                    else :
                        yDir = 0

                    if zv < -zDeadZone :
                        zDir = -1
                    elif zv > zDeadZone :
                        zDir = 1
                    else :
                        zDir = 0
                    '''

                    # Axis 0 / Roll

                    if xvalue < 0:
                        if round(xvalue*-1,1) != move_left:
                            # Axis 0 / Left
                            print "Axis 0 / Left"
                            print "Speed" + " : " + str(round(xvalue*-1,1))
                            move_left = round(xvalue*-1,1);
                            drone.speed = round(xvalue*-1,1)
                            drone.move_left()
                    elif xvalue > 0:
                        if round(xvalue,1) != move_right:
                            # Axis 0 / Right
                            print "Axis 0 / Right"
                            print "Speed" + " : " + str(round(xvalue,1))
                            move_right = round(xvalue,1)
                            drone.speed = round(xvalue,1)
                            drone.move_right()
                        
                    # Axe 1 / Pitch

                    if yvalue < 0:
                        if round(yvalue*-1,1) != move_forward:
                            # Axis 1 / Forward
                            print "Axis 1 / Forward"
                            print "Speed" + " : " + str(round(yvalue*-1,1))
                            move_forward = round(yvalue*-1,1)
                            drone.speed = round(yvalue*-1,1)
                            drone.move_forward()
                    elif yvalue > 0:
                        if round(yvalue,1) != move_backward:
                            # Axis 1 / Backward
                            print "Axis 1 / Backward"
                            print "Speed" + " : " + str(round(yvalue,1))
                            move_backward = round(yvalue,1)
                            drone.speed = round(yvalue,1)
                            drone.move_backward()

                    #Axis 3 / Yaw

                    if zvalue < 0:
                        if round(zvalue*-1,1) != yaw_left:
                            # Axis 3 / Yaw left
                            print "Axis 3 / Yaw left"
                            print "Speed" + " : " + str(round(zvalue*-1,1))
                            yaw_left = round(zvalue*-1,1)
                            drone.speed = round(zvalue*-1,1)
                            drone.turn_left()
                    elif zvalue > 0:
                        if round(zvalue,1) != yaw_right:
                            # Axis 3 / Yaw right
                            print "Axis 3 / Yaw right"
                            print "Speed" + " : " + str(round(zvalue,1))
                            yaw_right = round(zvalue,1)
                            drone.speed = round(zvalue,1)
                            drone.turn_right()
                    
                    '''    
                    # Axis 3 / Yaw
                    if round(zvalue*1,0) > 0:
                        if round(zvalue*1,0) != turn:
                            # Axis 3 / Yaw Right
                            print "Axis 3 / Yaw Right" + " : " + str(round(zvalue*1,0))
                            turn = round(zvalue*1,0)
                            drone.speed = 1
                            drone.turn_right()
                    elif round(zvalue*-1,0) > 0:
                        if round(zvalue*-1,0) != turn:
                            # Axe 3 / Yaw left
                            print "Axis 3 / Yaw Left" + " : " + str(round(zvalue*-1,0))
                            turn = round(zvalue*-1,0)
                            drone.speed = 1
                            drone.turn_left()
                    elif round(zvalue*1,0) == 0:
                        if round(zvalue*1,0) != turn:
                            # Axe 3 / Stop Yaw
                            print "Axis 3 / Stop Yaw" + " : " + str(round(zvalue*1,0))
                            turn = round(zvalue*1,0)
                            drone.speed = 0
                            drone.hover()
                    '''
                    time_2 = time.time()
                    time_diff = (time_2 - time_1)*1000
                    print time_diff
                    time_1 = time_2
            clock.tick(10000)
        print "Shutting down...",
        drone.reset()
        drone.halt()
        video.stop()
        print "Ok."
        quit()

    
if __name__ == '__main__':
    try:
        # Control
        controle = controle('Thread Controle')
        controle.start()
        time.sleep(5)
        # Video
        video = video('Thread Video')
        video.start()
    except (KeyboardInterrupt, SystemExit):
        cleanup_stop_thread();
        sys.exit()

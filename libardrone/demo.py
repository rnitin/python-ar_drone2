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
        pygame.init()

        """Launch drone class"""
        drone = libardrone.ARDrone(True)
        clock = pygame.time.Clock()
        running = True

        """Set up and init joystick"""
        j=joystick.Joystick(0) 
        j.init()
        
        move_forward = 0
        move_backward = 0
        move_left = 0
        move_right = 0
        turn = 0
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    
                    # takeoff
                    if event.button == 7:
                        print "Take Off !"
                        drone.takeoff()
                    # Land
                    elif event.button == 6:
                        print "Land !"
                        drone.land()
                    # Stop and land
                    elif event.button == 10: #pending
                        print "Stop and Land !"
                        drone.land()
                        running = False
                    # Altitude UP
                    elif event.button == 3:
                        print "Altitude UP"
                        drone.speed = 1
                        drone.move_up()
                    # Altitude Down
                    elif event.button == 0:
                        print "Altitude Down"
                        drone.speed = 1
                        drone.move_down()
                    # Emmergency
                    elif event.button == 1:
                        print "Emergency !"
                        drone.reset()
                        
                    # Anim : Boom !	#pending
                    elif event.button == 0:
                        print "Anim : Boom !"
                        drone.event_boom()
                        
                    # Anim : Turnarround !	#pending
                    elif event.button == 4:
                        print "Anim : Turnarround !"
                        drone.event_turnarround()  

                    # Anim : Yaw Shake !	#pending
                    elif event.button == 9:
                        print "Anim : Yaw Shake !"
                        drone.event_yawshake()
                        
                    # Anim : Yaw Dance !	#pending
                    elif event.button == 8:
                        print "Anim : Yaw Dance !"
                        drone.event_yawdance()
                        
                    # Anim : ThetaMixed !	#pending
                    elif event.button == 5:
                        print "Anim : ThetaMixed !"
                        drone.event_thetamixed()
                        
                        
                if event.type == pygame.JOYBUTTONUP:
                    # Altitude UP
                    if event.button == 3:
                        print "Altitude UP STOP !"
                        drone.speed = 0
                        drone.hover()
                    # Altitude Down
                    elif event.button == 0:
                        print "Altitude Down STOP !"
                        drone.speed = 0
                        drone.hover()
                    
                            
                if event.type == pygame.JOYAXISMOTION:
                    # Axis 0 / Left - Right
                    if event.axis == 0:
                        if event.value < 0:
                            if round(event.value*-1,1) != move_left:
                                # Axis 0 / Left
                                print "Axis 0 / Left"
                                print "Speed" + " : " + str(round(event.value*-1,1))
                                move_left = round(event.value*-1,1);
                                drone.speed = round(event.value*-1,1)
                                drone.move_left()
                        elif event.value > 0:
                            if round(event.value,1) != move_right:
                                # Axis 0 / Right
                                print "Axis 0 / Right"
                                print "Speed" + " : " + str(round(event.value,1))
                                move_right = round(event.value,1)
                                drone.speed = round(event.value,1)
                                drone.move_right()
                        
                    # Axe 1 / Forward - Backward
                    elif event.axis == 1:
                        if event.value < 0:
                            if round(event.value*-1,1) != move_forward:
                                # Axis 1 / Forward
                                print "Axis 1 / Forward"
                                print "Speed" + " : " + str(round(event.value*-1,1))
                                move_forward = round(event.value*-1,1)
                                drone.speed = round(event.value*-1,1)
                                drone.move_forward()
                        elif event.value > 0:
                            if round(event.value,1) != move_backward:
                                # Axis 1 / Backward
                                print "Axis 1 / Backward"
                                print "Speed" + " : " + str(round(event.value,1))
                                move_backward = round(event.value,1)
                                drone.speed = round(event.value,1)
                                drone.move_backward()
                        
                    # Axis 3 / Yaw
                    elif event.axis == 3:
                        if round(event.value*1,0) > 0:
                            if round(event.value*1,0) != turn:
                                # Axis 3 / Yaw Right
                                print "Axis 3 / Yaw Right" + " : " + str(round(event.value*1,0))
                                turn = round(event.value*1,0)
                                drone.speed = 1
                                drone.turn_right()
                        elif round(event.value*-1,0) > 0:
                            if round(event.value*-1,0) != turn:
                                # Axe 3 / Yaw left
                                print "Axis 3 / Yaw Left" + " : " + str(round(event.value*-1,0))
                                turn = round(event.value*-1,0)
                                drone.speed = 1
                                drone.turn_left()
                        elif round(event.value*1,0) == 0:
                            if round(event.value*1,0) != turn:
                                # Axe 3 / Stop Yaw
                                print "Axis 3 / Stop Yaw" + " : " + str(round(event.value*1,0))
                                turn = round(event.value*1,0)
                                drone.speed = 0
                                drone.hover()
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

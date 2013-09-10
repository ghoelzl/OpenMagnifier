# Copyright 2011-2013 Guenther Hoelzl (ghoelzl@gmail.com)
#
# This file is part of OpenMagnifier
#
# OpenMagnifier is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenMagnifier is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OpenMagnifier.  If not, see <http://www.gnu.org/licenses/>.

import subprocess
import re
import pygame.camera

class Camera:
    
    MOVE_LEFT = 0
    MOVE_RIGHT = 1
    MOVE_UP = 2
    MOVE_DOWN = 3
    ZOOM_IN = 4
    ZOOM_OUT = 5
    MOVE_HOME = 6
    MOVE_CENTER = 7
    
    CAMERA = ["HD Webcam C615", "HD Webcam C910", "Webcam C905"]
    CAMERA_WIDTH = 1920
    CAMERA_HEIGHT = 1080
    
    COLORFILTER = ["none", "red", "blue", "green", "inv", "invred", "invblue", "invgreen"]

    def __init__(self):
        # default values
        self.camera = None
        self.video_device = 0
        self.code = ''
        self.video_width_source = Camera.CAMERA_WIDTH
        self.video_height_source = Camera.CAMERA_HEIGHT
        self.autofocus = True
        self.focus = 100
        self.playing = False
        self.colorfilternr = 0
        self.override_check_camera = False
        self.frames_to_snapshot = 0
        self.reset_view()
        pygame.camera.init()
        
    def reset_view(self):
        self.zoom_horizontal = self.video_width_source
        self.zoom_vertical = self.video_height_source
        self.offset_horizontal = 0
        self.offset_vertical = 0   
        
    def setup_camera(self):
        self.camera = pygame.camera.Camera("/dev/video"+str(self.video_device),
                                           (self.video_width_source, self.video_height_source))
        self.camera.start()   
   
    def get_image(self):
        # take new picture every second, when no action
        # if self.changes_left == 0:
        if self.frames_to_snapshot == 0:
            if self.camera:
                self.image = self.camera.get_image()
                # apply colorfilter
                if self.colorfilternr != 0:
                    pixel_array = pygame.surfarray.pixels3d(self.image)                    

                    if self.colorfilternr >= 4:   
                        pixel_array[:,:,0] = 255 - pixel_array[:,:,0]
                        pixel_array[:,:,1] = 255 - pixel_array[:,:,1]      
                        pixel_array[:,:,2] = 255 - pixel_array[:,:,2]                        
                    if self.colorfilternr in [1, 5]:
                        pixel_array[:,:,1] /= 4
                        pixel_array[:,:,2] /= 4
                    elif self.colorfilternr in [2, 6]:   
                        pixel_array[:,:,0] /= 4
                        pixel_array[:,:,2] /= 4
                    elif self.colorfilternr in [3,7]:   
                        pixel_array[:,:,0] /= 4
                        pixel_array[:,:,1] /= 4                
                    del pixel_array
            else: 
                self.image = pygame.Surface((self.video_width_source,
                                            self.video_height_source))    
            self.frames_to_snapshot = self.framerate             
        self.frames_to_snapshot -= 1
        #else:                                       
        #self.change_view_parameter()
        self.update_cropfilter()
        #self.changes_left -= 1

        cropped_image = pygame.Surface((self.zoom_horizontal, self.zoom_vertical))
        cropped_image.blit(self.image, (0,0), (self.left, self.top, self.zoom_horizontal, self.zoom_vertical))  
        image_scaled = pygame.transform.smoothscale(cropped_image, (self.window_x_size, self.window_y_size))        
        return image_scaled
           
    def set_window(self, x_size, y_size):
        self.window_x_size = x_size
        self.window_y_size = y_size
        if self.playing == True:
            self.update_cropfilter()
            
    def set_framerate(self, framerate):
        self.framerate = framerate

    def check_camera(self):        
        if self.override_check_camera == True:
            return            
        command = "v4l2-ctl --list-devices"
        try:
            output = subprocess.check_output(command, shell=True)
            result = re.search("HD Webcam C615.*\n.*/dev/video(.)", output)
            if result == None:
                raise IOError()
            self.video_device = result.group(1)
            self.code = Camera.CAMERA[0]
        except subprocess.CalledProcessError:
            raise IOError()
            
    def get_config(self):
        values = ({
            'videodevice':self.video_device, 
            'videowidthsource':self.video_width_source,
            'videoheightsource':self.video_height_source,
            'focus':self.focus,
            'zoomhorizontal':self.zoom_horizontal,
            'zoomvertical':self.zoom_vertical,
            'offsethorizontal':self.offset_horizontal,
            'offsetvertical':self.offset_vertical,
            'framerate':self.framerate,
            'overridecheckcamera':self.override_check_camera
            })
        return values
        
    def set_config(self, dictionary):
        if dictionary.has_key('videodevice'):
            self.video_device = dictionary['videodevice'];
        if dictionary.has_key('videowidthsource'):
            self.video_width_source = int(dictionary['videowidthsource']);
        if dictionary.has_key('videoheightsource'):
            self.video_height_source = int(dictionary['videoheightsource']);
        if dictionary.has_key('focus'):
            self.focus = int(dictionary['focus']);
        if dictionary.has_key('zoomhorizontal'):
            self.zoom_horizontal = int(dictionary['zoomhorizontal']);
        if dictionary.has_key('zoomvertical'):
            self.zoom_vertical = int(dictionary['zoomvertical']);
        if dictionary.has_key('offsethorizontal'):
            self.offset_horizontal = int(dictionary['offsethorizontal']);
        if dictionary.has_key('offsetvertical'):
            self.offset_vertical = int(dictionary['offsetvertical']);
        if dictionary.has_key('framerate'):
            self.framerate = int(dictionary['framerate']);
        if dictionary.has_key('overridecheckcamera'):
            self.override_check_camera = dictionary['overridecheckcamera'] == 'True';            
                                                        
    def update_cropfilter(self):
        
        if self.zoom_horizontal <= 40:
            self.zoom_horizontal = 40           
        elif self.zoom_horizontal > self.video_width_source:
            self.zoom_horizontal = self.video_width_source                              
                                
        self.zoom_vertical = (self.zoom_horizontal * 
            self.window_y_size)/self.window_x_size;
        
        # eventually adapt to new screen size 
        if self.zoom_vertical > self.video_height_source:
            self.zoom_vertical = self.video_height_source
            self.zoom_horvertical = (self.zoom_vertical * 
            self.window_x_size)/self.window_y_size;

        # eventually adjust horizontal offset
        minValue = -(self.video_width_source-self.zoom_horizontal)/2
        maxValue = (self.video_width_source-self.zoom_horizontal)/2
        if self.offset_horizontal < minValue:
            self.offset_horizontal = minValue       
        elif self.offset_horizontal > maxValue:
            self.offset_horizontal = maxValue           

        # eventually adjust vertical offset     
        minValue = -(self.video_height_source-self.zoom_vertical)/2
        maxValue = (self.video_height_source-self.zoom_vertical)/2
        if self.offset_vertical < minValue:
            self.offset_vertical = minValue         
        elif self.offset_vertical > maxValue:
            self.offset_vertical = maxValue

        self.top =   self.video_height_source/2 - self.offset_vertical - self.zoom_vertical/2;  
        if self.top < 0:
            self.top = 0
        self.left =   self.video_width_source/2 - self.offset_horizontal - self.zoom_horizontal/2;  
        if self.left < 0:
            self.left = 0
    
    def is_af(self):
        return self.autofocus
        
    def toggle_af(self):
        self.autofocus = not self.autofocus
        if self.code == Camera.CAMERA[0]:            
            command = "v4l2-ctl -d "+self.video_device+" -c focus_auto="
            if self.autofocus:
                command += "1"
            else:
                command += "0"            
            try:
                subprocess.check_output(command, shell=True)
                if not self.autofocus:
                    self.change_focus(0)
            except subprocess.CalledProcessError:
                raise IOError()

    def get_focus(self):
        return self.focus        
        
    def change_focus(self, delta):
        self.focus += delta
        if self.focus < 10:
            self.focus = 10
        elif self.focus > 200:
            self.focus = 200

        if self.code == Camera.CAMERA[0]:            
            command = "v4l2-ctl -d "+self.video_device+" -c focus_absolute="
            command += str(self.focus)
            try:
                subprocess.check_output(command, shell=True)
            except subprocess.CalledProcessError:
                raise IOError()

    def change_view(self, action):
        #if self.changes_left > 0:
        #    return
        #self.action = action      
        #self.changes_left = 5  
        self.inc_horizontal = (int) (self.zoom_horizontal * 0.05)
        self.inc_vertical = (int) (self.zoom_vertical * 0.05)
        if action == Camera.MOVE_RIGHT:
            self.offset_horizontal -= self.inc_horizontal
        elif action == Camera.MOVE_LEFT:
            self.offset_horizontal += self.inc_horizontal
        elif action == Camera.MOVE_UP:            
            self.offset_vertical += self.inc_vertical
        elif action == Camera.MOVE_DOWN:
            self.offset_vertical -= self.inc_vertical    
        elif action == Camera.ZOOM_IN:
            self.zoom_horizontal = (int) (self.zoom_horizontal / 1.05)
        elif action == Camera.ZOOM_OUT:    
            self.zoom_horizontal = (int) (self.zoom_horizontal * 1.05)
        elif action == Camera.MOVE_HOME:           
            self.offset_horizontal = 10000 
            
    def change_colorfilter(self, increment):
        if increment == 0:
            self.colorfilternr = 0
        elif increment == 1:
            self.colorfilternr += 1
            if self.colorfilternr >= len(self.COLORFILTER):
                self.colorfilternr = 0
        else:
            self.colorfilternr -= 1
            if self.colorfilternr < 0:
                self.colorfilternr = len(self.COLORFILTER)-1
                     
 

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
#===============================================================
# Copyright 2017 Dimitris Chloupis
#================================================================
#################################################################
#
# MORPHEAS
#=================================================================
# Morpheas is a GUI API for Blender addons that takes advantage of
# BGL module that gives access to Blender OpenGL content. In turn
# this allows the user to control and manipulate the Blender GUI
# in an extreme level. Morpheas try to make this whole process
# more easy.
#################################################################
#
# Installation
#----------------------------------------------------------------
# Installation is very simple all you have to do is copy this file
# to the same as your addon. You also need to have png.py in the
# same folder a module  that is  part of the PyPNG project, which
#  enables Morpheas to load PNG files.
##################################################################
#
# Documentation
#----------------------------------------------------------------
# Documentation is included in the source file because its far
# more useful to learn how Morpheas works by examining its code.
# I tried to make my intentions in code as obvious as possible
# together with providing detailed comments
#################################################################
#================================================================


import bpy,blf
from bgl import *
from  . import png
import pdb

# The Morph is extremely essential in Morpheas. It provides the base
# class that all other morph classes are inherit from. In this class is
# the most basic functionality of GUI elements that are called
# "Morphs". Specific functionality is defined on specific subclasses
# of this class

class Morph:
    # global variable for the definition of the default folder where
    # the PNG files which are used as textures are located
    texturePath = "media/graphics/"

    # texture: This is the name of the texture file without the extension
    # name: a Morph can have a name for easier identification
    # texturePath: this is instance based and it will overide the class variable
    # of the same name if it's not None or else it will use that
    # onLeftAction, onRightAction etc define classes that execute specific actions when the appropriate
    # event is triggered by the morph. These classes are only required to have onLeftClick , onRightClick, onMouse in
    # etc with a single argument being the morph that is handling the event
    def __init__(self, texture= None, width = 100, height = 100, position =[0,0], color = [1.0,1.0,1.0,1.0], name= 'noname',
                 onLeftClickAction = None , onRightClickAction = None, onMouseInAction = None, onMouseOutAction = None, texturePath = None):

        # pdb.set_trace()
        self.width = width
        self.height = height
        self.position = position
        self.color = color
        self.children =[]
        self.handlesMouseDown = False
        self.handlesEvents = False
        self.handlesMouseOver = False
        self.bounds = [self.position[0],self.position[1],self.position[0]+self.width, self.position[1]+self.height]
        self._is_hidden = False
        self._parent = None
        self._world = None
        self.name = name
        self.draw_count=0
        self.textures = {}

        if texturePath is None:
            self.texturePath = Morph.texturePath
        else:
            self.texturePath = texturePath

        if texture is not None:
            self.load_texture(texture)
        self.active_texture = texture
        self.onLeftClickAction = onLeftClickAction
        self.onRightClickAction = onRightClickAction
        self.onMouseInAction = onMouseInAction
        self.onMouseOutAction = onMouseOutAction

    # this is an internal method not to be used directly by the user
    # it loads the texture, the actual displaying is handled by the
    # draw() method
    # name: is the same as texture and is the name of the PNG file
    # without the extension
    # scale: it allows to scale the texture , it only scales down
    # 1 being texture at full size
    def load_texture(self,name,scale=0.5):
        # detect the current location of the addon using Morpheas
        currentPath = __file__[0:-11]
        bpy.path.basename(currentPath)
        # create the full path of the texture to be loaded and load it
        full_path = currentPath + self.texturePath +name+'.png'
        f = png.Reader(full_path)
        f.read()
        f=f.asFloat()
        content = list(f[2])

        buf = Buffer(GL_FLOAT, [len(content), len(content[0])],content)
        # a Morph can have multiple textures if it is needed, the information
        # about those textures are fetched directly from the PNG file
        self.textures[name]={'dimensions':[f[3]['size'][0],f[3]['size'][1]],
                             'full_path': full_path, 'data': buf,
                             'is_gl_initialised': False, 'scale':scale, 'texture_id':0}
        self.width=self.textures[name]['dimensions'][0]
        self.height=self.textures[name]['dimensions'][1]
        self.activate_texture(name)


        return self.textures[name]

    # one texture can be active at the time in order to display on screen
    def activate_texture(self,name):
        self.active_texture = name
        self.width = round(self.textures[name]['dimensions'][0]* self.textures[name]['scale'])
        self.height = round(self.textures[name]['dimensions'][1]* self.textures[name]['scale'])

    # the main draw function
    def draw(self,context):
        print("draw has been called")
        if (not self.is_hidden) and ( not len(self.textures) == 0):
            # Use OpenGL to get the size of the window we can draw without overlapping with other areas

            mybuffer = Buffer(GL_INT, 4)
            glGetIntegerv(GL_VIEWPORT, mybuffer)
            World.draw_area = mybuffer
            World.draw_area_position = [mybuffer[0], mybuffer[1]]
            World.draw_area_width = mybuffer[2]
            World.draw_area_height = mybuffer[3]


            self.draw_count = self.draw_count + 1
            # pdb.set_trace()
            at = self.textures[self.active_texture]

            # load the texture to the OpenGL context
            if not at['is_gl_initialised']:

                at['texture_id'] = Buffer(GL_INT, [1])

                glGenTextures(1, at['texture_id'])

                glBindTexture(GL_TEXTURE_2D,at['texture_id'].to_list()[0])


                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, at['dimensions'][0], at['dimensions'][1], 0, GL_RGBA,GL_FLOAT, at['data'])
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                at['is_gl_initialised']= True
            else:
                glBindTexture(GL_TEXTURE_2D, at['texture_id'].to_list()[0])

            glColor4f(*self.color)
            # pdb.set_trace()
            # draw a simple rectangle with the size and scale of the Morph
            # use the active texture as texture of the rectangle
            glEnable(GL_BLEND)
            glEnable(GL_TEXTURE_2D)
            glBegin(GL_QUADS)
            glTexCoord2f(1, 1)
            glVertex2f(self.position[0],self.position[1])
            glTexCoord2f(0, 1)
            glVertex2f((self.position[0]+self.width),self.position[1])
            glTexCoord2f(0, 0)
            glVertex2f((self.position[0]+self.width), (self.position[1]+self.height))
            glTexCoord2f(1, 0)
            glVertex2f(self.position[0], (self.position[1]+self.height))


            # restore OpenGL context to avoide any conflicts
            glEnd()
            glDisable(GL_TEXTURE_2D)
            glDisable(GL_BLEND)

        if (not self.is_hidden) and len(self.children) > 0:

            for childMorph in self.children:
                childMorph.draw(context)

    # every Morph belongs to a World which is another Morph
    # acting as a general manager of the behavior of Morphs
    @property
    def world(self):

        if self._world is None and self._parent is not None:
            self._world = self.parent.world
        return self._world

    @world.setter
    def world(self,value):
        self._world = value

    # a Morph can contain another Morph, if so each morph it contains
    # is called a "children" and for each children it is the parent
    @property
    def parent(self):

        if self._parent == None and self._world != None:
            self._parent = self.world
        return self._parent

    @parent.setter
    def parent(self,value):
        self._parent = value

    @property
    def is_hidden(self):
        return self._is_hidden

    @is_hidden.setter
    def is_hidden(self,value):
        for morph in self.children:
            if morph._is_hidden != value:
                morph.is_hidden = value
        self._is_hidden = value

    # Morpheas uses relative position coordinates. Those are the position of Morph added to the position
    # of the parent and of course of the World. This method get the actual position inside the Blender
    # area that Morphs are drawn
    def getAbsolutePosition(self):

        if self.parent != None:
            return (self.parent.getAbsolutePosition()[0]+self.position[0],self.parent.getAbsolutePosition()[1]+self.position[1])
        else:
            return self.position

    # add the Morph as a child to another Morph, the other Morph becomes the parent
    def addMorph(self,morph):

        morph.parent=self
        morph.world = self.world
        self.children.append(morph)

        if self.bounds[0] > morph.bounds[0]:
            self.bounds[0] = morph.bounds[0]
        if self.bounds[1] > morph.bounds[1]:
            self.bounds[1] = morph.bounds[1]
        if self.bounds[2] < morph.bounds[2]:
            self.bounds[2] = morph.bounds[2]
        if self.bounds[3] < morph.bounds[3]:
            self.bounds[3] = morph.bounds[3]


    # upper left corner of the bounding box
    def x(self):
        return self.position[0]

    def y(self):
        return self.position[1]

   # lower right corner of the bounting box, defining the area occupied by the morph
    def x2(self):
        return self.x() + self.width

    def y2(self):
        return  self.y() + self.height

    # This is also an internal method called by the World morph, that acts as the general
    # mechanism for figuring out the type event it received and sending it to the appropriate
    # specialised method
    def onEvent(self,event,context):
        w = self.world


        w.mouse_cursor_coordinates = [(w.window_position[0] + event.mouse_region_x) - w.draw_area_position[0],
                      (w.window_position[1] + event.mouse_region_y) - w.draw_area_position[1]]


        if self.handlesEvents and not self.is_hidden:
            if event.type in {'LEFTMOUSE', 'RIGHTMOUSE'}:
                self.onMouseDown(event)
            elif event.type in {'MOUSEMOVE'}:
                self.onMouseOver(event)
        else:
            for morph in self.children:
                morph.onEvent(event,context)

    # an event when any mouse button is pressed
    def onMouseDown(self,event):

        apx1 = self.getAbsolutePosition()[0]
        apy1 = self.getAbsolutePosition()[1]
        apx2 = self.getAbsolutePosition()[0]+self.width
        apy2 = self.getAbsolutePosition()[1]+self.height
        ex = self.world.mouse_cursor_coordinates[0]
        ey = self.world.mouse_cursor_coordinates[1]
        if ex>apx1 and ex<apx2 and ey>apy1 and ey<apy2 :

            if self.handlesMouseDown :
                if event.type == 'LEFTMOUSE':
                    self.onLeftClick()
                elif event.type == 'RIGHTMOUSE':
                    self.onRightClick()

    # an event when the mouse cursor passed over the area occupied by the morph
    def onMouseOver(self, event):

        apx1 = self.getAbsolutePosition()[0]
        apy1 = self.getAbsolutePosition()[1]
        apx2 = self.getAbsolutePosition()[0] + self.width
        apy2 = self.getAbsolutePosition()[1] + self.height
        ex = self.world.mouse_cursor_coordinates[0]
        ey = self.world.mouse_cursor_coordinates[1]

        if ex > apx1 and ex < apx2 and ey > apy1 and ey < apy2:


            return self.onMouseIn()
        else:
            return self.onMouseOut()

    def onLeftClick(self):
        if self.onLeftClickAction is not None:
            return self.onLeftClickAction.onLeftClick(self)
        else:
            return self.world.event

    def onRightClick(self):
        if self.onRightClickAction is not None:
            return self.onRightClickAction.onRightClick(self)
        else:
            return self.world.event

    # an event for when the mouse enters the area of the Morph
    def onMouseIn(self):
        if onMouseInAction is not None:
            return self.onMouseInAction.onMouseIn(self)
        else:
            return self.world.event
    # an event for when the mouse exits the area of the Morph
    def onMouseOut(self):
        if onMouseOutAction is not None:
            return self.onMouseOutAction.onMouseIn(self)
        else:
            return self.world.event

# World morph is a simple morph that triggers and handles the drawing methods and event methods
# for each child morph. In order for a morph to be a child of a World it has to be added to it or
# else it wont display. There should be one World, however because a World is essentially a Morph
# a multi layer interface can use dummy morphs as containers
class World(Morph):

    # this defines whether the event send to World's onEvent method
    # has been handled by any morph. If it has not , you can use this variable
    # to make sure your modal method returns "PASS_THROUGH" so that the event
    # is passed back to Blender and you dont block user interaction
    consumedEvent=False
    # the modal operator that uses this World
    modal_operator = 0
    # the ccordinates of the mouse cursor
    mouse_cursor_coordinates = [0,0]
    window_position = [0,0]
    window_width = 300
    window_height = 300
    event = None
    draw_area = None
    draw_area_position = [0,0]
    draw_area_width = 300
    draw_area_height = 300

#    def draw(self):

#        if len(self.children) > 0:

#            for childMorph in self.children:
#                childMorph.draw()

    def addMorph(self,morph):

        morph.parent = self
        morph.world = self
        self.children.append(morph)

        if self.bounds[0] > morph.bounds[0]:
            self.bounds[0] = morph.bounds[0]
        if self.bounds[1] > morph.bounds[1]:
            self.bounds[1] = morph.bounds[1]
        if self.bounds[2] < morph.bounds[2]:
            self.bounds[2] = morph.bounds[2]
        if self.bounds[3] < morph.bounds[3]:
            self.bounds[3] = morph.bounds[3]

    def onEvent(self,event,context):
        x1 = context.area.regions[4].x
        y1 = context.area.regions[4].y
        World.window_position = (x1, y1)
        x2 = context.area.regions[4].width
        y2 = context.area.regions[4].height
        World.window_width = x2
        World.window_height = y2
        World.mouse_cursor_position = [event.mouse_region_x, event.mouse_region_y]
        World.event = event
        World.consumedEvent = False
        for morph in self.children:
            morph.onEvent(event,context)

# StringMorph is a class that defines a simple label , a piece of text of any size
# size: is the size of the font
class StringMorph(Morph):

    def __init__(self, font_id=0, text=["empty string"], x=15, y=0, size=16, dpi=72, **kargs):
        super().__init__(texture= None, **kargs)
        self.position = [x,y]
        self.size = size
        self.dpi = dpi
        self.text = text
        self.children =[]
        self.handlesMouseDown = False
        self.handlesEvents = False
        self.handlesMouseOver = False
        self.bounds = [self.position[0],self.position[1],self.position[0]+self.width, self.position[1]+self.height]
        self._is_hidden = False
        self._parent = None
        self._world = None
        self.name = "default"
        self.font_id = 0


    def draw(self):
        super().draw()
        glColor4f(*self.color)


        blf.size(self.font_id, self.size, self.dpi)
        blf.position(self.font_id, self.position[0], self.position[1], 0)
        blf.draw(self.font_id, self.text)

# a ButtonMorph is a morph that responds to an action. This is a default
# behavior for morphs, however ButtonMorph makes it a bit easier and provides
# an easy way to change the morph appearance when the mouse is hovered over
# the button
class ButtonMorph(Morph):

    def __init__(self,**kargs):
        super().__init__(**kargs)
        self.handlesMouseOver = True
        self.handlesEvents = True
        self.handlesMouseDown = True


    def onMouseIn(self):
        self.change_appearance(1)

    def onMouseOut(self):
        self.change_appearance(0)

    def change_appearance(self,value):
        if value==0:
            self.color = (1.0, 1.0, 1.0, 0.5)
        if value==1:
            self.color = (self.color[0], self.color[1], self.color[2], 1.0)
















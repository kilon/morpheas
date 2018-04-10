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
# ===============================================================
# Copyright 2017 Dimitris Chloupis
# ================================================================
#################################################################
#
# MORPHEAS
# =================================================================
# Morpheas is a GUI API for Blender addons that takes advantage of
# BGL module that gives access to Blender OpenGL content. In turn
# this allows the user to control and manipulate the Blender GUI
# in an extreme level. Morpheas try to make this whole process
# more easy.
#################################################################
#
# Installation
# ----------------------------------------------------------------
# Installation is very simple all you have to do is copy this file
# to the same folder as your addon. Morpheas comes also with its own
# distribution of PIL included to faciliate the loading of textures
##################################################################
#
# Documentation
# ----------------------------------------------------------------
# Documentation is included in this source file because its far
# more useful to learn how Morpheas works by examining its code.
# I tried to make my intentions in code as obvious as possible
# together with providing detailed comments
#################################################################
# ================================================================


import bpy, blf
from . import bgl
from . import livecoding
from .morpheas_backend import *
from .PIL import Image

import pdb
import numpy


# The Morph is extremely essential in Morpheas. It provides the base
# class that all other morph classes are inherit from. In this class is
# the most basic functionality of GUI elements that are called
# "Morphs". Specific functionality is defined on specific subclasses
# of this class. Morpheas is inspired by Morphic, a GUI that is
# also based on morphs, approaching GUI creation as a lego like process
# of assembling almost identical things together with ease and simplicity

class Morph(livecoding.LiveObject):
    # global variable for the definition of the default folder where
    # the PNG files which are used as textures are located
    texture_path = "media/graphics/"
    instances =[]
    # this is the main suspect, responsible for the creation of the morph, each keyword argument is associated
    # with an instance variable so see the comment of the relevant instance variable for more information
    def __init__(self, texture=None, width=100, height=100, position=[0, 0], color=[1.0, 1.0, 1.0, 1.0], name='noname',
                 on_left_click_action=None, on_left_click_released_action=None,
                 on_right_click_action=None, on_right_click_released_action=None,
                 on_mouse_in_action=None, on_mouse_out_action=None,
                 texture_path=None, scale=1):
        super().__init__()
        self._width = width
        self._height = height
        self._position = position

        # one may ask why color in a morph with a texture. None the less color can affect not only the color of the
        # active texture but also its transparency . Color is a list of floats following the RGBA ( red, green, blue
        # and alpha (transparency). [ r , g , b, alpha ]
        self.color = color

        # essentially these variables enable and disable the handling of specific events. If events are disabled
        # they are ignored by this morph but they do pass to its children. If none handles them as well, the event
        # is passed back to Blender through world's consumed_event instance variable. For more info about this , see
        # World comments
        self.handles_mouse_down = False
        self.handles_events = False
        self.handles_mouse_over = False
        self.handles_drag_drop = False


        self._is_hidden = False

        # a morph can be inside another morph. That other morph is the parent while this morph becomes the child
        self._parent = None
        self.children = []

        # a world is essentially a parent without a parent. World is a morph responsible for
        # anything that is not morph specific and general functionalities like figuring out
        # where the mouse is and what region draws at the time
        self._world = None

        # a name is an optional feature for when you want to locate a specific morph inside a world
        # and do something to it or do something with it
        self._name = name

        # this counts the amount of times the morph has been drawn. Can be useful to figure out FPS
        # and make sure Morpheas does not slow down Blender
        self.draw_count = 0

        # though only one texture can display at time , a morph can have multiple textures
        self.textures = {}

        # a morph can be scaled like any blender object. The scale is also tied to the scale of the active texture
        # the scale of the active texture depends on the dimensions of the png file
        self._scale = scale

        # this tells where to find the textures
        if texture_path is None:
            self.texture_path = Morph.texture_path
        else:
            self.texture_path = texture_path

        # drag and drop flag
        self.drag_drop = False
        self.drag_position =[]

        # active texture is the texture displaying at the time
        # only one texture can display at a time , if you want more then you have to have multiple child morphs
        # each child will have its own active texture
        self.active_texture = texture

        # these are actions which are basically simple python objects that contain an appropriate method
        # like on_left_click or on_right_click. This allows us to keep as MVC model that has the handling of
        # events seperate from Morpheas and for the user to define his own actions without having to subclass Morph
        self.on_left_click_action = on_left_click_action
        self.on_left_click_released_action = on_left_click_released_action
        self.on_right_click_action = on_right_click_action
        self.on_right_click_released_action = on_right_click_released_action
        self.on_mouse_in_action = on_mouse_in_action
        self.on_mouse_out_action = on_mouse_out_action

        self.can_draw = True

        if texture is not None:
            self.load_texture(self.active_texture, self.scale)

    # the easiest way to change the texture of the morph is to use the self.texture attribute
    # here Morpheas will return always the active texture when you read the variable
    @property
    def texture(self):
        return self.active_texture

    # if you try to set the variable and the texture is not part of the list of textures
    # morph has available , it loads the texture (Adding it to the list of textures)
    #  and makes it active. If it is available it just makes it active.
    @texture.setter
    def texture(self, name):
        if name in self.textures:
            self.activate_texture(name)
        else:
            self.load_texture(name)

            # width of the morph

    @property
    def width(self):

        if self._width < 0:
            raise ValueError("width must not be a negative value")
        else:
            return self._width

    @width.setter
    def width(self, value):
        if value < 0:
            raise ValueError("new value for width must be a positive number")
        else:
            self._width = value

    # height of the morph
    @property
    def height(self):
        if self._height < 0:
            raise ValueError("height must not be a negative value ")
        else:
            return self._height

    @height.setter
    def height(self, value):
        if value < 0:
            raise ValueError("new value for width must be a positive number")
        else:
            self._height = value

    # position is relative to its parent morph.
    @property
    def position(self):
            return self._position

    @position.setter
    def position(self, value):
        self._position = value


    # world position returns the position of the morph relative to the world it belongs too
    @property
    def world_position(self):
        if self.parent is not None:
            return [self.parent.world_position[0] + self.position[0],
                    self.parent.world_position[1] + self.position[1]]
        else:
            return [0,0]

    # world position is a read only variable
    @world_position.setter
    def world_position(self, value):
        raise ValueError("world_position is read only !")

    # absolute position is the position relative to the entire blender window
    @property
    def absolute_position(self):
        return [self.world_position[0] + self.world.draw_area[0] , self.world_position[1]+ self.world.draw_area[1] ]

    # world position is a read only variable
    @absolute_position.setter
    def absolute_position(self, value):
        raise ValueError("absolute_position is read only !")

    # bounds defines the boundary box of the morph
    @property
    def bounds(self):
        return [self.position[0], self.position[1], self.position[0] + self.width,
                       self.position[1] + self.height]
    @bounds.setter
    def bounds(self,value):
        raise ValueError("bounds is read only !")


    @property
    def mouse_over_morph(self):
        apx1 = self.world_position[0]
        apy1 = self.world_position[1]
        apx2 = self.world_position[0] + self.width
        apy2 = self.world_position[1] + self.height
        ex = self.world.mouse_position[0]
        ey = self.world.mouse_position[1]
        result = ( ex > apx1 and ex < apx2 and ey > apy1 and ey < apy2)
        return result



    # every Morph belongs to a World which is another Morph
    # acting as a general manager of the behavior of Morphs
    @property
    def world(self):

        if self._world is None and self._parent is not None:
            self._world = self.parent.world
        return self._world

    @world.setter
    def world(self, value):
        self._world = value



    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self,value):
        self._scale = value
        self.width = round(self.width * value)
        self.height = round(self.height * value)

        for morph in self.children:
            morph.scale = value

    # a Morph can contain another Morph, if so each morph it contains
    # is called a "child" and for each child it is the parent
    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def is_hidden(self):
        return self._is_hidden

    @is_hidden.setter
    def is_hidden(self, value):
        for morph in self.children:
            if morph._is_hidden != value:
                morph.is_hidden = value
        self._is_hidden = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,new_name):
        self._name = new_name


    # this is an internal method not to be used directly by the user
    # it loads the texture, the actual displaying is handled by the
    # draw() method
    # name: is the same as texture and is the name of the PNG file
    # without the extension
    # scale: it allows to scale the texture
    # 1 being texture at full size
    def load_texture(self, name, scale=1):

        # detect the current location of the addon using Morpheas
        current_path = __file__[0:-11]
        bpy.path.basename(current_path)

        # create the full path of the texture to be loaded and load it
        full_path = current_path + self.texture_path + name + '.png'
        im = Image.open(full_path)
        data = numpy.array(im)
        data = data.astype(float)
        data = numpy.divide(data,255.0)
        content = numpy.array(data).reshape(im.size[1],im.size[0]*4)
        buf = bgl.Buffer(bgl.GL_FLOAT, [len(content),len(content[0])], content)

        # a Morph can have multiple textures if it is needed, the information
        # about those textures are fetched directly from the PNG file
        self.textures[name] = {'dimensions': [im.size[0], im.size[1]],
                               'full_path': full_path, 'data': buf,
                               'is_gl_initialised': False, 'scale': scale, 'texture_id': 0}

        self.activate_texture(name)
        return self.textures[name]



    # one texture can be active at the time in order to display on screen
    def activate_texture(self, name):
        self.active_texture = self.textures[name]
        self.width = round(self.textures[name]['dimensions'][0] * self.textures[name]['scale'])
        self.height = round(self.textures[name]['dimensions'][1] * self.textures[name]['scale'])
        self.scale = self.textures[name]['scale']


    # add the Morph as a child to another Morph, the other Morph becomes the parent
    def add_morph(self, morph):

        morph.parent = self
        morph.world = self.world
        self.children.append(morph)


    # returns a child morph of a specific name of course this depend on the definition
    # of a name at the creation of Morph or after
    def get_child_morph_named(self, name):
        if len(self.children)>0:
            for child in self.children:
                if child.name == name:
                    return child
                elif child.get_child_morph_named(name) is not None:
                    return child.get_child_morph_named(name)
        else:
            return None



    # upper left corner of the bounding box
    def x(self):
        return self.position[0]

    def y(self):
        return self.position[1]

        # lower right corner of the bounting box, defining the area occupied by the morph

    def x2(self):
        return self.x() + self.width

    def y2(self):
        return self.y() + self.height

    # This is also an internal method called by the World morph, that acts as the general
    # mechanism for figuring out the type event it received and sending it to the appropriate
    # specialised method. Generally this should not be overridden by your classes unless you
    # want to override the general event behavior of the morph. For specific event override the
    # relevant methods instead.
    def on_event(self, event, context):

        if len(self.children)>0:
            for morph in self.children:
                morph.on_event(event, context)

        if self.handles_events and not self.is_hidden and not self.world.consumed_event:
            if event.type in {'LEFTMOUSE', 'RIGHTMOUSE'}:
                self.on_mouse_click(event)

            elif event.type in {'MOUSEMOVE'}:
                self.on_mouse_over(event)




    # an event when any mouse button is pressed or released
    def on_mouse_click(self, event):
        if self.mouse_over_morph:
            if self.handles_mouse_down:
                self.world.consumed_event = True
                if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                    self.on_left_click()
                if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                    self.on_left_click_released()
                if event.type == 'RIGHTMOUSE' and event.value == 'PRESS':
                    self.on_right_click()
                if event.type == 'RIGHTMOUSE' and event.value == 'RELEASE':
                    self.on_right_click_released()

    # an event when the mouse cursor passes over the area occupied by the morph
    def on_mouse_over(self, event):
        if self.drag_drop:
            offset = [self.world.mouse_position[0] - self.drag_position[0],
                      self.world.mouse_position[1] - self.drag_position[1]]
            self.position = [self.position[0] + offset[0], self.position[1] + offset[1]]
            self.drag_position = self.world.mouse_position
        if self.mouse_over_morph:
            return self.on_mouse_in()
        else:
            if self.drag_drop:
                self.drag_drop = False
            return self.on_mouse_out()

    # the following methods should be self explanatory and depend on the action classes passed to the
    # morph. These are also the methods to override if you want to treat specifc events differently inside your morph
    def on_left_click(self):
        if self.on_left_click_action is not None:
            return self.on_left_click_action.on_left_click(self)
        else:
            if not self.drag_drop:
                self.drag_drop = True
                self.drag_position = self.world.mouse_position
            return self.world.event

    def on_left_click_released(self):
        if self.on_left_click_released_action is not None:
            return self.on_left_click_released_action.on_left_click_released(self)
        else:
            if self.drag_drop:
                self.drag_drop = False
            return self.world.event

    def on_right_click(self):
        if self.on_right_click_action is not None:
            return self.on_right_click_action.on_right_click(self)
        else:
            return self.world.event

    def on_right_click_released(self):
        if self.on_right_click_released_action is not None:
            return self.on_right_click_released_action.on_right_click_released(self)
        else:
            return self.world.event

    # an event for when the mouse enters the area of the Morph
    def on_mouse_in(self):
        if self.on_mouse_in_action is not None:
            return self.on_mouse_in_action.on_mouse_in(self)
        else:
            return self.world.event

    # an event for when the mouse exits the area of the Morph
    def on_mouse_out(self):
        if self.on_mouse_out_action is not None:
            return self.on_mouse_out_action.on_mouse_in(self)
        else:
            return self.world.event


# World morph is a simple morph that triggers and handles the drawing methods and event methods
# for each child morph. In order for a morph to be a child of a World it has to be added to it or
# else it wont display. There can be more than one world. Generally this is not necessary if you want
# to create a multi layer interfaces because each morph can act as a container (parent) to other morphs (children)
# On the other hand there are cases when you want each layer to be really separate and with its own handling of events
# and drawing which make sense to have multiple worlds. The choice is up to you but remember you have to call draw
# and on_event methods for each world you have if you want that world to display and handle events for its children
# morphs.A world requires a modal operator , because only Blender's modal operators are the recommended way for handling
# Blender events and drawing on regions of internal Blender windows. As such the draw() method must be called inside the
# method associated with the modal's drawing and on_event is called on the modal method of your modal operator.
# You need to call only those two methods for Morpheas to work of course taking into account you have already
# created a world , creted the morphs and added the morphs to the world via add_morph method.
class World(Morph):
    instances = []
    def __init__(self, **kargs):

        super().__init__(**kargs)

        # this defines whether the event send to World's onEvent method
        # has been handled by any morph. If it has not , you can use this variable
        # to make sure your modal method returns {"PASS_THROUGH"} so that the event
        # is passed back to Blender and you don't block user interaction
        self.consumed_event = False

        # the modal operator that uses this World
        self.modal_operator = 0

        # the coordinates of the mouse cursor, its the same as blender mouse coordinates
        # of the WINDOW region of the internal window that has been assigned the modal
        # operator needed to draw and send events to Morpheas. Blender does not change that
        # window, so the mouse coordinates start [0,0] does not change as well
        self.mouse_position = [0, 0]

        # the absolute coordinates are different in that they do not start from the bottomn left
        # corner of the region assigned the handling of event by Blender bur rather
        # they are located at the bottom left corner of the Blender window
        # this is necessary when Morpheas draws in regions not associated by Blender with handling
        # of events to figure out exactly where the mouse is located inside the entire Blender window
        self.mouse_position_absolute = [0, 0]

        # whether mouse is inside a region that is drawing at the time
        # this is used for auto_hide feature
        self.mouse_cursor_inside = False

        # window here is the region that is associated with the handling of events and it does not change
        # this is defined by Blender. Morpheas itself gives any region that calls the on_event method
        # the ability to handle events through the World morph. Generally this should not concern you
        # because it happens automatically and does not require any additional information.
        self.window_position = [0, 0]
        self.window_width = 300
        self.window_height = 300

        # the blender event as it is
        self.event = None

        # draw area is the region at that particular time that draws the world
        # even though in blender only one region is responsible with event handling
        # for Morpheas any other region can draw graphics and receive events as well
        # this is useful when you replicate the same internal window for example when
        # you have opened multiple 3d views
        self.draw_area = [0,0,0,0]
        self.draw_area_position = [0, 0]
        self.draw_area_width = 300
        self.draw_area_height = 300
        self.draw_area_context = None

        # This feature hides the World on regions that the mouse is on top of
        # so it depends on self.mouse_cursor_inside
        self.auto_hide = True

        self._width = 2000
        self._height = 2000

        #MOpenGLCanvas is the backend of Morpheas responsible for all drawing functionality

        self.mOpenGLCanvas = MOpenGLCanvas(self)

        self.can_draw = False





    # position with coordinates that start [0,0] at the bottom of the entire Blender window
    # (not to be confused with Blender's own internal windows)
    def get_absolute_position(self):
        return [self.position[0] + self.draw_area_position[0], self.position[1] + self.draw_area_position[1]]

    #  draw depends on Morph draw, what it does additionally is the auto_hide feature
    def draw(self, context):
        self.draw_area_context = context
        if self.event is not None:
            # Use OpenGL to get the size of the region we can draw without overlapping with other areas
            mybuffer = bgl.Buffer(bgl.GL_INT, 4)
            bgl.glGetIntegerv(bgl.GL_VIEWPORT, mybuffer)
            mx = self.event.mouse_region_x
            my = self.event.mouse_region_y
            mabx = self.mouse_position_absolute[0]
            maby = self.mouse_position_absolute[1]
            self.mouse_cursor_inside = (
                    (mabx > mybuffer[0]) and (mabx < (mybuffer[0] + mybuffer[2])) and (
                    maby > mybuffer[1]) and (maby < (mybuffer[1] + mybuffer[3])))

            # if auto_hide is enabled , draw my Morphs ONLY if the mouse is located inside the area
            # that draws at the time
            if (
                    self.mouse_cursor_inside and self.auto_hide and context.area.type == "VIEW_3D" and context.region.type == "WINDOW") or not self.auto_hide:
                self.draw_area_context = context
                self.draw_area = mybuffer

                # from that extract information about the region and
                # assign it to relevant instance variables
                self.draw_area_position = [mybuffer[0], mybuffer[1]]
                self.draw_area_width = mybuffer[2]
                self.draw_area_height = mybuffer[3]

                self.mouse_position = [self.mouse_position_absolute[0] - self.draw_area[0],
                                       self.mouse_position_absolute[1] - self.draw_area[1]]

                self.mOpenGLCanvas.draw()


    # a world cannot have a world by itself and of course not a parent
    # this is why we override the Morph add_morph method
    def add_morph(self, morph):
        super().add_morph(morph)
        morph.world = self


    # again this depends on Morph on_event
    # Here we automatically set up information about which region has been
    # assigned by Blender to handle events
    def on_event(self, event, context):

        bmx = context.region.x
        bmy = context.region.y
        self.window_position = (bmx, bmy)

        self.window_width =  context.region.width
        self.window_height = context.region.height

        self.mouse_position_absolute = [event.mouse_region_x + self.window_position[0], event.mouse_region_y + self.window_position[1]]
        self.event = event

        # consume_event is reset so World does not block events that are not handled by it
        # instead those events are passed back to Blender through the {'PASS_THROUGH'} return
        # so you need to check out this variable and if it is False you need to make sure
        # the modal method of your modal operator (needed for Morpheas to work)
        # returns {'PASS_THROUGH'} if you want your user to interact with
        # a Morpheas GUI and Blender at the same time or else you will have an angry user hunting you down in forums

        self.consumed_event = False

        for morph in self.children:
            morph.on_event(event, context)




# StringMorph is a class that defines a simple label , a piece of text of any size
# size: is the size of the font
class TextMorph(Morph):
    instances = []
    def __init__(self, font_id=0, text="empty string",size=16, dpi=72, **kargs):
        super().__init__(texture=None, **kargs)
        self.size = size
        self.dpi = dpi
        self.text = text
        self.font_id = font_id
        self.text_lines = self.text.splitlines()


    def draw(self):
        self.text_lines = self.text.splitlines()
        if (not self.is_hidden):
            bgl.glColor4f(*self.color)
            blf.size(self.font_id, self.size, self.dpi)
            for x in range(0,len(self.text_lines)):
                blf.position(self.font_id, self.position[0], self.position[1] + (self.size*x*(-1)), 0)
                blf.draw(self.font_id, self.text_lines[x])


# a ButtonMorph is a morph that responds to an action. This is a default
# behavior for morphs, however ButtonMorph makes it a bit easier and provides
# an easy way to change the morph appearance when the mouse is hovering over
# the button
class ButtonMorph(Morph):
    instances = []
    def __init__(self, hover_glow_mode=True, **kargs):
        super().__init__(**kargs)
        self.handles_mouse_over = True
        self.handles_events = True
        self.handles_mouse_down = True

        # hover glow mode will make the button semi transparent if the mouse is outside its boundaries
        self.hover_glow_mode = hover_glow_mode

    def on_mouse_in(self):
        if self.hover_glow_mode:
            self.change_appearance(1)

    def on_mouse_out(self):
        if self.hover_glow_mode:
            self.change_appearance(0)

    def change_appearance(self, value):

        if value == 0:
            self.color = (self.color[0], self.color[1], self.color[2], 0.8)
        if value == 1:
            self.color = (self.color[0], self.color[1], self.color[2], 1.0)
















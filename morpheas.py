
import bpy,blf
from bgl import *
from cyclops import png
import pdb

class Morph:

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
            self.texturePath = "media/graphics/"
        else:
            self.texturePath = texturePath

        if texture is not None:
            self.load_texture(texture)
        self.active_texture = texture
        self.onLeftClickAction = onLeftClickAction
        self.onRightClickAction = onRightClickAction
        self.onMouseInAction = onMouseInAction
        self.onMouseOutAction = onMouseOutAction


    def load_texture(self,name,scale=0.5):
        currentPath = __file__[0:-11]
        bpy.path.basename(currentPath)
        full_path = currentPath + self.texturePath +name+'.png'
        f = png.Reader(full_path)
        f.read()
        f=f.asFloat()
        content = list(f[2])
        buf = Buffer(GL_FLOAT, [len(content), len(content[0])],content)

        self.textures[name]={'dimensions':[f[3]['size'][0],f[3]['size'][1]],
                             'full_path': full_path, 'data': buf,
                             'is_gl_initialised': False, 'scale':scale, 'texture_id':0}
        self.width=self.textures[name]['dimensions'][0]
        self.height=self.textures[name]['dimensions'][1]
        self.activate_texture(name)


        return self.textures[name]

    def activate_texture(self,name):
        self.active_texture = name
        self.width = round(self.textures[name]['dimensions'][0]* self.textures[name]['scale'])
        self.height = round(self.textures[name]['dimensions'][1]* self.textures[name]['scale'])


    def draw(self):
        if (not self.is_hidden) and ( not len(self.textures) == 0):
            self.draw_count = self.draw_count + 1
            # pdb.set_trace()
            at = self.textures[self.active_texture]
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



            glEnd()
            glDisable(GL_TEXTURE_2D)
            glDisable(GL_BLEND)

        if (not self.is_hidden) and len(self.children) > 0:

            for childMorph in self.children:
                childMorph.draw()

    @property
    def world(self):

        if self._world is None and self._parent is not None:
            self._world = self.parent.world
        return self._world

    @world.setter
    def world(self,value):
        self._world = value

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

    def getAbsolutePosition(self):

        if self.parent != None:
            return (self.parent.getAbsolutePosition()[0]+self.position[0],self.parent.getAbsolutePosition()[1]+self.position[1])
        else:
            return self.position


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



    def x(self):
        return self.position[0]

    def y(self):
        return self.position[1]

    def x2(self):
        return self.x() + self.width

    def y2(self):
        return  self.y() + self.height

    def onEvent(self,event):
        op = self.world.modal_operator
        self.world.cursor_cor = [(op.window_position[0] + event.mouse_region_x) - op.draw_window_position[0],
                      (op.window_position[1] + event.mouse_region_y) - op.draw_window_position[1]]


        if self.handlesEvents and not self.is_hidden:
            if event.type in {'LEFTMOUSE', 'RIGHTMOUSE'}:
                self.onMouseDown(event)
            elif event.type in {'MOUSEMOVE'}:
                self.onMouseOver(event)
        else:
            for morph in self.children:
                morph.onEvent(event)


    def onMouseDown(self,event):

        apx1 = self.getAbsolutePosition()[0]
        apy1 = self.getAbsolutePosition()[1]
        apx2 = self.getAbsolutePosition()[0]+self.width
        apy2 = self.getAbsolutePosition()[1]+self.height
        ex = self.world.cursor_cor[0]
        ey = self.world.cursor_cor[1]
        if ex>apx1 and ex<apx2 and ey>apy1 and ey<apy2 :

            if self.handlesMouseDown :
                if event.type == 'LEFTMOUSE':
                    self.onLeftClick()
                elif event.type == 'RIGHTMOUSE':
                    self.onRightClick()

    def onMouseOver(self, event):

        apx1 = self.getAbsolutePosition()[0]
        apy1 = self.getAbsolutePosition()[1]
        apx2 = self.getAbsolutePosition()[0] + self.width
        apy2 = self.getAbsolutePosition()[1] + self.height
        ex = self.world.cursor_cor[0]
        ey = self.world.cursor_cor[1]

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

    def onMouseIn(self):
        if onMouseInAction is not None:
            return self.onMouseInAction.onMouseIn(self)
        else:
            return self.world.event

    def onMouseOut(self):
        if onMouseOutAction is not None:
            return self.onMouseOutAction.onMouseIn(self)
        else:
            return self.world.event

class World(Morph):

    consumedEvent=False
    modal_operator = 0
    cursor_cor = [0,0]
    event = None

    def draw(self):

        if len(self.children) > 0:

            for childMorph in self.children:
                childMorph.draw()

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

    def onEvent(self,event):
        World.event = event
        self.consumedEvent = False
        for morph in self.children:
            morph.onEvent(event)

class StringMorph(Morph):

    def __init__(self, font_id=0, text=["empty string"], x=15, y=0, size=16, dpi=72, **kargs):
        # if not texture is None:
        #     self.width = round(ccr[texture][2]/scale)
        #     self.height = round(ccr[texture][3]/scale)
        #     self.textureCoordinates = CyclopsSkinCoordinatesAbsolute[texture]
        # else:
        #     self.width = len(text)*size
        #     self.height = size
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
















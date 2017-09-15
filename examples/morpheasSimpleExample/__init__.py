import bpy
import bgl
import blf
from .morpheas import *
import pdb

bl_info={
"name": "MorpheasSimpleExample",
"description": "This is a simple example of a Morpheas GUI with one button",
"author": "Kilon ",
"version": (1, 0, 0, 0),
"blender": (2, 77, 0),
"location": "View3D",
"wiki_url": "http://www.kilon-alios.com",
"category": "Object"}

# this class is defining the action performed when the button is clicked
class AButtonAction:
    def onLeftClick(morph):
        print("the button has been clicked")
        morph.texture = "buttonClickedIcon"

def draw_callback_px(self, context):
   #draw the morphs
   self.world.draw(context)


class ModalDrawOperator(bpy.types.Operator):
    """Draw a line with the mouse"""
    bl_idname = "view3d.morpheas_test"
    bl_label = "Morpeas Test"
    
    def __init__(self):
         self.world = None
         self.window_position = (0,0)
         
    def modal(self, context, event):
         context.area.tag_redraw()
         # we pass the event to the World and we let it handle it
         #pdb.set_trace()
         self.world.onEvent(event,context)
         if self.world.consumedEvent: # this checks whether Morpheas used the event or not
            return {'RUNNING_MODAL'}
         else:
            return {'PASS_THROUGH'}

    def invoke(self, context, event):
        # create the world
        self.world = World()
        # we add to World our modal operator because Morpheas uses its context
        # to retrieve infomation about the window and its areas
        self.world.modal_operator = self
        # we create a button with a texture named buttonIcon.png , which Morpheas
        # expects to find inside the subfolder media/graphics
        # we also add our action class, which Morpheas expects it to have a onLeftClick(mopth)
        # morph here represent the morph that has been assigned the action
        self.abutton = ButtonMorph(texture="buttonIcon",onLeftClickAction = AButtonAction)
        # we add the button to the World
        self.world.addMorph(self.abutton)

      
        if context.area.type == 'VIEW_3D':
            # the arguments we pass the the callback
            args = (self, context)
            # Add the region OpenGL drawing callback
            # draw in view space with 'POST_VIEW' and 'PRE_VIEW'
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')

            self.mouse_path = []

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(ModalDrawOperator)


def unregister():
    bpy.utils.unregister_class(ModalDrawOperator)

if __name__ == "__main__":
    register()

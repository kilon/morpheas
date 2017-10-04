import bpy
import bgl
import blf
from .morpheas import *
import pdb

bl_info={
"name": "MorpheasExamples",
"description": "This is a collection of examples of  Morpheas GUI API ",
"author": "Kilon ",
"version": (0, 0, 0, 1),
"blender": (2, 79, 0),
"location": "View3D",
"wiki_url": "http://www.kilon-alios.com",
"category": "Object"}

# this class is defining the action performed when the button is clicked
class AButtonAction:
    def on_left_click(morph):
        # user has clicked the button, so lets make it glow
        morph.texture = "button_glow"

        # and also display the instructions text
        text= morph.world.get_child_morph_named("instructions")
        text.is_hidden = False

def draw_callback_px(self, context):
   #draw the morphs
   self.world.draw(context)


class MorpheasExample1(bpy.types.Operator):
    bl_idname = "view3d.morpheas_example_1"
    bl_label = "Morpeas Example 1"
    
    def __init__(self):
         self.world = None
         self.window_position = (0,0)
         
    def modal(self, context, event):
         context.area.tag_redraw()

         # pressing ESC key will exit
         if event.type in {'ESC'}:
             self.report({'WARNING'}, "ESC key has been pressed, example terminated")

             # this removes the draw handle so nothing is drawn in the viewport
             bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
             return {'CANCELLED'}

         # we pass the event to the World and we let it handle it
         self.world.on_event(event,context)

         # this checks whether Morpheas used the event or not
         if self.world.consumed_event:
            return {'RUNNING_MODAL'}
         # if it did not use the event we return the event back to blender to handle it
         # this way we don't block normal user action
         else:
            return {'PASS_THROUGH'}

    def initialise_world(self):
        # create the world
        self.world = World()

        # we add to World our modal operator because Morpheas uses its context
        # to retrieve infomation about the window and its areas
        self.world.modal_operator = self

        # we create a button with a texture named buttonIcon.png , which Morpheas
        # expects to find inside the subfolder media/graphics
        # we also add our action class, which Morpheas expects it to have a on_left_click(morph), signature
        # morph here represent the morph that has been assigned the action
        # hover glow mode is disabled so it does not make the button semi transperent when the mouse is outside
        # its boundaries
        abutton = ButtonMorph(texture="button_no_glow", hover_glow_mode=False, on_left_click_action=AButtonAction,
                              name = "button")

        # we add the button to the World
        self.world.add_morph(abutton)

        # ok let's add some text too for instructions
        text = TextMorph(text="You destroyed me !!! What's wrong with you man !!! Press ESC to exit ", size= 30,
                         position = [50,300], name= "instructions")
        text.is_hidden = True

        # and add it to our world
        self.world.add_morph(text)


    def invoke(self, context, event):

        self.initialise_world()
      
        if context.area.type == 'VIEW_3D':
            # the arguments we pass the draw callback
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

class MorpheasExamplesPanel(bpy.types.Panel):

    # Creates a Panel in the scene context of the properties editor"""
    bl_label = "MorpheasExamples"
    bl_idname = "Morpheas_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Morpheas"
    bl_context = "objectmode"

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("view3d.morpheas_example_1")


def register():
    bpy.utils.register_class(MorpheasExample1)
    bpy.utils.register_class(MorpheasExamplesPanel)



def unregister():
    bpy.utils.unregister_class(MorpheasExample1)
    bpy.utils.unregister_class(MorpheasExamplesPanel)

if __name__ == "__main__":
    register()

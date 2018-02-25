from . import livecoding
import sys, pdb
import bpy

class Playground(livecoding.LiveObject):
    instances = []
    def __init__(self):
        super().__init__()
        self.enabled = True
        self.executed_once = False
        self.execution_counter=0

    def event_loop_started(self):
        morpheas = sys.modules['cyclops']
        world_instance = morpheas.CyclopsModalDrawOperator.world
        if world_instance.event is not None:
            return True
        else:
            return False

    def main_loop(self):
        self.enabled = True
        if self.enabled and self.event_loop_started():
            self.execute_playground()

    def execute_playground(self):
        #self.execute_once(4)
        #print("executing")
        morpheas = sys.modules['cyclops']
        cm = morpheas.CyclopsModalDrawOperator

        world_instance = morpheas.CyclopsModalDrawOperator.world
        debug_button = world_instance.get_child_morph_named("debug_button")

        panel = world_instance.get_child_morph_named("central_panel")
        union_button = world_instance.get_child_morph_named("booleans_union_button")
        #pdb.set_trace()
        difference_button = world_instance.get_child_morph_named("booleans_difference_button")
        intersect_button = world_instance.get_child_morph_named("booleans_intersect_button")

        #print(world_instance)
        log = world_instance.get_child_morph_named("log")

        log.text = "debug: {} hello  again log: {}".format(debug_button.is_hidden,log.is_hidden)


        debug_button.is_hidden = not cm.dev_mode
        log.is_hidden = not cm.dev_mode


        #panel.position = [0,150]
        #log.position = [10,800]
        #debug_button.position = [10,650]


        #print()
        return

    def execute_once(self,counter):
        if self.execution_counter == counter:
            self.execute_once_actions()
            self.executed_once = True
            self.execution_counter = self.execution_counter + 1
        return

    def execute_once_actions(self):
        instances= sys.modules['cyclops.morpheas'].ButtonMorph.instances
        return instances

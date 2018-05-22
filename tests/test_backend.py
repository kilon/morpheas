from .. import backend,core

def run(logger):
    moglcanvas = TestMOpenGLCanvas.__init__(logger)
    moglcanvas.run()

class TestMOpenGLCanvas():
    instances=[]

    def __init__(self,logger):
        self.__class__.instances.append(self)
        self.world = core.World()
        self.canvas = backend.MOpenGLCanvas(self.world)
        self.log = logger

    def run(self):
        return


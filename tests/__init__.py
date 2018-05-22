from . import test_backend, test_core
def run(loger):
    test_backend.run(loger)
    test_core.run(loger)
    return

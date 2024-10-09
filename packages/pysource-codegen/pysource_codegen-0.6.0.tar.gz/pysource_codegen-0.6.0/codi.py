from inline_snapshot import snapshot, createRecorder, Trace


# basic building blocks:
# - createRecorder, to wrap functions or other objects and to record the accesses/calls
# - Trace, to represent the calls which where made.
#   The lambda would be called with some special objects to create the DSL


def external_function(arg):
    return arg + 1


def test_function():
    mocked_external_function, recorder = createRecorder(external_function)

    recorder.save(
        snapshot(
            Trace(
                lambda external_function: [
                    external_function(5) == 6,
                    external_function(2) == 3,
                ]
            )
        )
    )

    mocked_external_function(5)
    mocked_external_function(2)


# the concept could also be extended to classes (and maybe modules)


class external_class:
    def __init__(self, value):
        self.value = value

    def add(self, value):
        return self.value + value

    def sub(self, value):
        return self.value - value


def test_class():
    mocked_class, recorder = createRecorder(external_class)

    recorder.save(
        snapshot(
            Trace(
                lambda external_class: [
                    v1 := external_class(5),
                    v1.add(2) == 7,
                    v1.sub(1) == 4,
                ]
            )
        )
    )

    c = mocked_class(5)
    c.add(2)
    c.sub(1)


from mock import patch
from importlib import import_module
from contextlib import contextmanager

@contextmanager
def record(path,trace):

    # lookup the original object
    module_path,attr=path.rsplit(".",1)
    obj=getattr(import_module(module_path),attr)

    # record access to this object
    mocked_object,recorder=createRecorder(obj)

    recorder.save(trace)
    
    # patch the original object
    with patch(path,mocked_object):
        yield


def test_something():
    with record("package.module.external_function",snapshot()):
        obj=Class(...)
        assert obj.do(...) == ...




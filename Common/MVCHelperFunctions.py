
from collections.abc import Callable
from unittest.mock import MagicMock
from typing import Any

methods_to_ignore = {'__iter__', 'replaceWidget'}


class TestableControlFunction:
    '''
        Creates a testable class function that has test arguments
        and key word arguments stored by default.

        The object will be called as normal with the underlying
        function when there is a normal function call.
    '''
    def __init__(self, func: Callable, test_args: tuple, test_kwargs: dict):
        self.func = func
        self.test_args = test_args
        self.test_kwargs = test_kwargs

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def mock_call(self, mock_controller: MagicMock):
        return self.func(mock_controller, *self.test_args, *self.test_kwargs)


def apply_method_to_mock(cls_attr: Any, mock: Callable):
    '''
        If object is an instance of a TestableControlFunction
        will call the function on the mock with test arguments.
    '''
    if isinstance(cls_attr, TestableControlFunction):
        cls_attr.mock_call(mock)


def do_all_control_method_calls(cls_obj: Any, mock: MagicMock):
    '''
        Search though the list of functions in a class
        object to find any TestableControlFunctions to
        check the types of.
    '''
    for key in dir(cls_obj):
        if hasattr(cls_obj, key):
            cls_attr = cls_obj.__getattribute__(key)
            apply_method_to_mock(cls_attr, mock)


def verify_object_field_has_mock_attributes(mock: MagicMock, field_name: str, schema: Any):
    '''
        Given that certain objects were requested from the mock,
        we verify that these attributes are present in the
        the class that we expect to extract it from.
    '''
    if field_name not in mock._mock_children:
        return

    mocked_field = mock._mock_children[field_name]
    for key in mocked_field._mock_children.keys():
        if key not in methods_to_ignore and not hasattr(schema, key):
            raise AttributeError(f"{key} required by function but not present in {field_name}")

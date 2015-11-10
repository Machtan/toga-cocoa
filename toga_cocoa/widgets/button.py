from __future__ import print_function, absolute_import, division, unicode_literals

from rubicon.objc import objc_method, get_selector

from .base import Widget
from ..libs import *
from ..utils import process_callback


def _ButtonImpl(interface):
    class ButtonImpl(NSButton):
        @objc_method('v@')
        def onPress_(self, obj):
            callback = interface.on_press
            if callback:
                process_callback(callback(interface))
    return ButtonImpl


class Button(Widget):
    """A common button
    
    Members:
    label: str, the text on the button
    on_press: Widget -> (), a callback for when the button is pressed"""
    def __init__(self, label, on_press=None):
        super(Button, self).__init__()
        self._impl = _ButtonImpl(self).alloc().init()

        self._impl.setBezelStyle_(NSRoundedBezelStyle)
        self._impl.setButtonType_(NSMomentaryPushInButton)
       
        self._impl.setTarget_(self._impl)
        self._impl.setAction_(get_selector('onPress:'))
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
        
        self.label = label
        self.on_press = on_press
    
    @property
    def label(self):
        return self._label
    
    @label.setter
    def label(self, value):
        self._label = value
        self._impl.setTitle_(at(self.label))

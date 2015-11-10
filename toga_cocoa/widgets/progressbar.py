from __future__ import print_function, absolute_import, division, unicode_literals

from ..libs import *
from .base import Widget
from toga.constants import *


class ProgressBar(Widget):
    """A progress bar widget
    
    Members:
    max, float? the maximum value of the progress bar
    value: float, the float value of the current progress
    """
    def __init__(self, max=None, value=None, display_when_stopped=False):
        super(ProgressBar, self).__init__()
        self._running = False
        self._impl = NSProgressIndicator.new()
        self._impl.setStyle_(NSProgressIndicatorBarStyle)
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self._max = 0
        self.max = max
        self._display_when_stopped = None
        self.display_when_stopped = display_when_stopped
        self.value = value
        
    
    @property
    def display_when_stopped(self):
        return self._display_when_stopped
    
    @display_when_stopped.setter
    def display_when_stopped(self, value):
        self._display_when_stopped = value
        self._impl.setDisplayedWhenStopped_(value)
        
    
    @property
    def max(self):
        return self._max
    
    @max.setter
    def max(self, value):
        if value is not None:
            self._impl.setIndeterminate_(False)
            self._impl.setMaxValue_(value)
        else:
            self._impl.setIndeterminate_(True)
        self._max = value
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        if value is not None:
            self._impl.setDoubleValue_(value)
        else:
            self.stop()

    def start(self):
        """Starts the animation of the progress bar (if running)"""
        if self._impl and not self._running:
            self._impl.startAnimation_(self._impl)
            self._running = True

    def stop(self):
        """Stops the animation of the progress bar (if running)"""
        if self._impl and self._running:
            self._impl.stopAnimation_(self._impl)
            self._running = False

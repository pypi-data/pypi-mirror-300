"""
Handling custom widget and auto templating
"""


class ZeroWidgetRegistry:
    def __init__(self):
        self.widgets = []

    def register(self, widget):
        self.widgets.append(widget)
        self.widgets.sort(key=lambda x: x.priority)

    def get_widgets(self):
        return self.widgets


zero_widget_registry = ZeroWidgetRegistry()

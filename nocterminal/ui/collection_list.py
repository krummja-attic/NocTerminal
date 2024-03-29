from __future__ import annotations

from math import floor

from bearlibterminal import terminal
from morphism import Rect, Point, Size

from nocterminal.blt import terminal_state
from .rect_view import RectView
from .label_view import LabelView
from .first_responder import FirstResponderContainerView


class SettingsListView(FirstResponderContainerView):

    def __init__(
            self,
            label_control_pairs,
            value_column_width: int = 16,
            *args, **kwargs
        ) -> None:
        self.rect_view = RectView()
        self.rect_view.fill = False
        self.scroll_indicator_view = LabelView(text="█")
        super().__init__(subviews=[self.rect_view,
                                   self.scroll_indicator_view], *args, **kwargs)

        self._min_row = 0
        self.value_column_width = value_column_width
        self.first_responder_index = None

        self.labels = [LabelView(t, align_horz='left')
                       for t, _ in label_control_pairs]
        self.values = [c for _, c in label_control_pairs]

        self.add_subviews(self.labels)
        self.add_subviews(self.values)
        self.find_next_responder()

    @property
    def can_become_first_responder(self):
        return True

    def did_become_first_responder(self):
        super().did_become_first_responder()
        self.rect_view.style = 'double'

    def did_resign_first_responder(self):
        super().did_resign_first_responder()
        self.rect_view.style = 'single'

    @property
    def min_row(self):
        return self._min_row

    @min_row.setter
    def min_row(self, new_value):
        self._min_row = new_value
        self.set_needs_layout()

    def get_is_in_view(self, y):
        return self.min_row <= y <= self.min_row + self.inner_height

    @property
    def inner_height(self):
        return self.frame.height - 3

    @property
    def scroll_fraction(self):
        """
        How far down the user has scrolled. If a negative value, no scrolling is
        possible.
        """
        try:
            return self.min_row / (len(self.labels) - self.inner_height - 1)
        except ZeroDivisionError:
            return -1

    def scroll_to(self, y):
        if self.inner_height <= 0:
            return  # metrics are garbage right now

        if y < self.min_row:
            self.min_row = y
        elif y > self.min_row + self.inner_height:
            self.min_row = max(0, min(y - self.inner_height,
                                      len(self.labels) - self.inner_height))

    def set_first_responder_in_visible_area(self):
        if self.first_responder_index and self.get_is_in_view(self.first_responder_index):
            return
        self.first_responder_container_view.set_first_responder(
            self.values[self.min_row])

    def layout_subviews(self):
        self.rect_view.apply_springs_and_struts_layout_in_superview()
        if self.scroll_fraction >= 0:
            self.scroll_indicator_view.frame = Rect(
                Point(self.bounds.width - 1, 1 +
                      floor(self.inner_height * self.scroll_fraction)),
                Size(1, 1))

        for i in range(len(self.labels)):
            is_in_view = self.get_is_in_view(i)
            if is_in_view:
                y = 1 + self.bounds.y + i - self.min_row
                self.labels[i].frame = Rect(
                    Point(self.bounds.x + 1, y),
                    Size(self.bounds.width - self.value_column_width - 2, 1))
                self.values[i].frame = Rect(
                    Point(self.bounds.x + 1 + self.bounds.width -
                          self.value_column_width - 2, y),
                    Size(self.value_column_width, 1))
            self.labels[i].is_hidden = not is_in_view
            self.values[i].is_hidden = not is_in_view

    def descendant_did_become_first_responder(self, control):
        for i in range(len(self.labels)):
            if self.values[i] == control:
                if not self.get_is_in_view(i):
                    self.first_responder_index = i
                    self.scroll_to(i)
                break

    def descendant_did_resign_first_responder(self, control):
        self.first_responder_index = None

    def terminal_read_after_first_responder(self, val, can_resign):
        if val == terminal.TK_UP:
            self.find_prev_responder()
            return True
        elif val == terminal.TK_DOWN:
            self.find_next_responder()
            return True
        # pageup/<
        elif (val == terminal.TK_PAGEUP
              or val == terminal.TK_COMMA
              and terminal_state.shift):
            self.min_row = max(0, self.min_row - self.inner_height)
            self.set_first_responder_in_visible_area()
            return True
        # pagedown/>
        elif (val == terminal.TK_PAGEDOWN
              or val == terminal.TK_PERIOD
              and terminal_state.shift):
            self.min_row = min(
                len(self.labels) - self.inner_height - 1,
                self.min_row + self.inner_height)
            self.set_first_responder_in_visible_area()
            return True


class KeyAssignedListView(SettingsListView):

    CHARACTER_SET = (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz"
        "0123456789!\"#$%?&*()_+^:'.|{}[]@")

    def __init__(self, value_controls, value_column_width=16, *args, **kwargs):
        symbols = (symbol for symbol in self.CHARACTER_SET)
        label_control_pairs = []
        for value_control in value_controls:
            label_control_pairs.append((next(symbols, " "), value_control))

        super().__init__(label_control_pairs,
                         value_column_width=value_column_width,
                         *args, **kwargs)

    def terminal_read(self, val):
        super().terminal_read(val)
        char = chr(terminal.state(terminal.TK_WCHAR))
        label_index = next((index for index, label in enumerate(self.labels)
                            if label.text == char), None)
        if label_index is not None:
            self.first_responder_container_view.set_first_responder(
                self.values[label_index])

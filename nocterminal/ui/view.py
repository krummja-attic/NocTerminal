from __future__ import annotations
from typing import *
from morphism import Point, Rect, Size

from .layout_options import LayoutOptions

if TYPE_CHECKING:
    from nocterminal.blt.context import Context
    from .screen import Screen


ZERO_RECT = Rect(Point(0, 0), Size(0, 0))


class View:

    def __init__(
            self, *,
            screen: Optional[Screen] = None,
            layout: Optional[LayoutOptions] = None,
            subviews: Optional[List[View]] = None,
            frame: Optional[Rect] = None,
            clear: bool = False,
            layer: int = 0
        ) -> None:
        self._frame: Rect = frame
        if frame is None:
            self._frame = ZERO_RECT
        self._screen: Screen = screen
        self._superview: Optional[View] = None
        self.needs_layout: bool = True
        self._bounds: Rect = self._frame.with_origin(Point(0, 0))
        self._layer = layer

        self.clear: bool = clear
        self.first_responder = None
        self.is_first_responder: bool = False
        self.is_hidden: bool = False

        self.subviews: List[View] = []
        self.add_subviews(subviews if subviews else [])

        self.layout_spec: Rect = frame
        self.layout_options: LayoutOptions = layout
        if layout is None:
            self.layout_options = LayoutOptions()

    def __str__(self) -> Callable[[], str]:
        return self.debug_string

    def __repr__(self) -> Callable[[], str]:
        return self.debug_string

    @property
    def screen(self) -> Optional[Screen]:
        if self._screen:
            return self._screen
        else:
            return self.superview.screen

    @property
    def superview(self) -> Optional[View]:
        try:
            return self._superview
        except AttributeError:
            return None

    @superview.setter
    def superview(self, value: View) -> None:
        self._superview = value

    def set_needs_layout(self, value: bool = True) -> None:
        self.needs_layout = value

    def add_subviews(self, subviews: List[View]) -> None:
        for v in subviews:
            v.superview = self
        self.subviews.extend(subviews)

    def remove_subviews(self, subviews: List[View]) -> None:
        for v in subviews:
            v.superview = None
        self.subviews = [v for v in self.subviews if v not in subviews]

    def add_subview(self, subview: View) -> None:
        self.add_subviews([subview])

    def remove_subview(self, subview: View) -> None:
        self.remove_subviews([subview])

    def perform_draw(self, ctx: Context) -> None:
        if self.is_hidden:
            return
        ctx.layer(self._layer)
        self.draw(ctx)
        for view in self.subviews:
            with ctx.translate(view.frame.origin):
                view.perform_draw(ctx)

    def draw(self, ctx: Context):
        if self.clear:
            ctx.clear_area(self.bounds)

    def perform_layout(self) -> None:
        if self.needs_layout:
            self.layout_subviews()
            self.needs_layout = False
        for view in self.subviews:
            view.perform_layout()

    def layout_subviews(self) -> None:
        for view in self.subviews:
            view.apply_springs_and_struts_layout_in_superview()

    @property
    def intrinsic_size(self) -> Optional[Size]:
        return None

    @property
    def frame(self) -> Rect:
        return self._frame

    @frame.setter
    def frame(self, value: Rect) -> None:
        if value == self._frame:
            return
        self._frame = value
        self._bounds = value.with_origin(Point(0, 0))
        self.set_needs_layout(True)

    @property
    def bounds(self) -> Rect:
        return self._bounds

    @bounds.setter
    def bounds(self, value: Rect) -> None:
        if value.origin != Point(0, 0):
            raise ValueError("Bounds is always anchored at (0, 0)")
        if value == self._bounds:
            return
        self._bounds = value
        self._frame = self._frame.with_size(value.size)
        self.set_needs_layout(True)

    @property
    def can_become_first_responder(self) -> bool:
        return False

    @property
    def contains_first_responders(self) -> bool:
        return False

    @property
    def can_resign_first_responder(self) -> bool:
        return True

    @property
    def first_responder_container_view(self) -> Optional[View]:
        if self.first_responder:
            return self
        for v in self.ancestors:
            if v.first_responder:
                return v
        return None

    def did_become_first_responder(self) -> None:
        self.set_needs_layout(True)
        self.is_first_responder = True

    def did_resign_first_responder(self) -> None:
        self.set_needs_layout(True)
        self.is_first_responder = False

    def descendant_did_become_first_responder(self, view: View) -> bool:
        pass

    def descendant_did_resign_first_responder(self, view: View) -> bool:
        pass

    def terminal_read(self, char: int) -> bool:
        return False

    @property
    def leftmost_leaf(self):

        if self.subviews:
            return self.subviews[0].leftmost_leaf
        else:
            return self

    @property
    def postorder_traversal(self):
        for v in self.subviews:
            yield from v.postorder_traversal
        yield self

    @property
    def ancestors(self):
        v = self.superview
        while v:
            yield v
            v = v.superview

    def get_ancestor_matching(self, predicate):
        v = self.superview
        for _ in self.ancestors:
            if predicate(v):
                return v
        return None

    def apply_springs_and_struts_layout_in_superview(self):
        options = self.layout_options
        spec = self.layout_spec
        superview_bounds = self.superview.bounds

        fields = [('left', 'right', 'x', 'width'),
                  ('top', 'bottom', 'y', 'height')]

        final_frame = Rect(Point(-1000, -1000), Size(-1000, -1000))

        for field_start, field_end, field_coord, field_size in fields:

            debug_string = options.get_debug_string_for_keys(
                [field_start, field_size, field_end])

            matches = (options.get_is_defined(field_start),
                       options.get_is_defined(field_size),
                       options.get_is_defined(field_end))

            if matches == (True, True, True):
                raise ValueError(
                    "Invalid spring/strut definition: {}".format(debug_string))

            if matches == (False, False, False):
                raise ValueError(
                    "Invalid spring/strut definition: {}".format(debug_string))

            elif matches == (True, False, False):
                setattr(
                    final_frame, field_coord,
                    options.get_value(field_start, self))
                # pretend that size is constant from frame
                setattr(
                    final_frame, field_size,
                    getattr(spec, field_size))

            elif matches == (True, True, False):
                setattr(
                    final_frame, field_coord,
                    options.get_value(field_start, self))
                setattr(
                    final_frame, field_size,
                    options.get_value(field_size, self))

            elif matches == (False, True, False):  # magical centering!
                size_val = options.get_value(field_size, self)
                setattr(final_frame, field_size, size_val)
                setattr(
                    final_frame, field_coord,
                    getattr(superview_bounds, field_size) / 2 - size_val / 2)

            elif matches == (False, True, True):
                size_val = options.get_value(field_size, self)
                setattr(
                    final_frame, field_coord,
                    getattr(superview_bounds, field_size) - options.get_value(field_end, self) - size_val)
                setattr(final_frame, field_size, size_val)

            elif matches == (False, False, True):
                setattr(
                    final_frame, field_coord,
                    getattr(superview_bounds, field_size) - options.get_value(field_end, self))
                # pretend that size is constant from frame
                setattr(final_frame, field_size, getattr(spec, field_size))

            elif matches == (True, False, True):
                start_val = options.get_value(field_start, self)
                end_val = options.get_value(field_end, self)
                setattr(final_frame, field_coord, start_val)
                setattr(final_frame, field_size,
                        getattr(superview_bounds, field_size) - start_val - end_val)

            else:
                raise ValueError("Unhandled case: {}".format(debug_string))

        assert(final_frame.x != -1000)
        assert(final_frame.y != -1000)
        assert(final_frame.width != -1000)
        assert(final_frame.height != -1000)
        self.frame = final_frame.floored

    def debug_string(self) -> str:
        return str('{} {!r}'.format(type(self).__name__, self.frame))

    def debug_print(self, indent=0):
        print((' ' * indent) + self.debug_string())
        for sv in self.subviews:
            sv.debug_print(indent + 2)

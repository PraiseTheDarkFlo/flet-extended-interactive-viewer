import json
from enum import Enum
from typing import Any, Optional, Union, Callable, List

from flet.core.adaptive_control import AdaptiveControl
from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import OptionalNumber, Control
from flet.core.control_event import ControlEvent
from flet.core.event_handler import EventHandler
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import ResponsiveNumber, RotateValue, ScaleValue, OffsetValue, OptionalControlEventCallable, \
    DurationValue, Number, OptionalEventCallable


class ExtendedInteractiveViewerUpdateEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.offset_x: float = d.get("offset_x")
        self.offset_y: float = d.get("offset_y")
        self.scale: float = d.get("scale")

class FletExtendedInteractiveViewer(ConstrainedControl, AdaptiveControl):
    """
    FletExtendedInteractiveViewer Control description.
    """

    def __init__(
        self,
            #special
            content: Control,
            max_scale: OptionalNumber = None,
            min_scale: OptionalNumber = None,
            scale_factor: OptionalNumber = None,
            constrained: Optional[bool] = None,
            scale_enabled: Optional[bool] = None,
            on_interaction_update: Optional[
                Callable[[ExtendedInteractiveViewerUpdateEvent], None]
            ] = None,
            #normal
            ref: Optional[Ref] = None,
            key: Optional[str] = None,
            width: OptionalNumber = None,
            height: OptionalNumber = None,
            left: OptionalNumber = None,
            top: OptionalNumber = None,
            right: OptionalNumber = None,
            bottom: OptionalNumber = None,
            expand: Union[None, bool, int] = None,
            expand_loose: Optional[bool] = None,
            col: Optional[ResponsiveNumber] = None,
            opacity: OptionalNumber = None,
            rotate: Optional[RotateValue] = None,
            scale: Optional[ScaleValue] = None,
            offset: Optional[OffsetValue] = None,
            aspect_ratio: OptionalNumber = None,
            interaction_update_interval: Optional[int] = None,
            animate_opacity: Optional[AnimationValue] = None,
            animate_size: Optional[AnimationValue] = None,
            animate_position: Optional[AnimationValue] = None,
            animate_rotation: Optional[AnimationValue] = None,
            animate_scale: Optional[AnimationValue] = None,
            animate_offset: Optional[AnimationValue] = None,
            on_animation_end: OptionalControlEventCallable = None,
            tooltip: Optional[TooltipValue] = None,
            badge: Optional[BadgeValue] = None,
            visible: Optional[bool] = None,
            disabled: Optional[bool] = None,
            data: Any = None,
            adaptive: Optional[bool] = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
            tooltip=tooltip,
            badge=badge,
            visible=visible,
            disabled=disabled,
            data=data,
        )
        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.__on_interaction_update = EventHandler(
            lambda e: ExtendedInteractiveViewerUpdateEvent(e)
        )
        self._add_event_handler(
            "interaction_update", self.__on_interaction_update.get_handler()
        )

        self.content = content
        self.scale_enabled = scale_enabled
        self.constrained = constrained
        self.max_scale = max_scale
        self.min_scale = min_scale
        self.interaction_update_interval = interaction_update_interval
        self.scale_factor = scale_factor
        self.on_interaction_update = on_interaction_update


    def before_update(self):
        super().before_update()
        assert self.__content.visible, "content must be visible"

    def _get_control_name(self):
        return "flet_extended_interactive_viewer"

    def _get_children(self):
        children = []
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    def reset(self, animation_duration: Optional[DurationValue] = None):
        self.invoke_method(
            "reset", arguments={"duration": self._convert_attr_json(animation_duration)}
        )

    def zoom(self, factor: Number):
        self.invoke_method("zoom", arguments={"factor": str(factor)})

    # min_scale
    @property
    def min_scale(self) -> float:
        return self._get_attr("minScale", data_type="float", def_value=0.8)

    @min_scale.setter
    def min_scale(self, value: OptionalNumber):
        assert value is None or value > 0, "min_scale must be greater than 0"
        self._set_attr("minScale", value)

    # max_scale
    @property
    def max_scale(self) -> float:
        return self._get_attr("maxScale", data_type="float", def_value=2.5)

    @max_scale.setter
    def max_scale(self, value: OptionalNumber):
        assert value is None or value > 0, "max_scale must be greater than 0"
        self._set_attr("maxScale", value)

    # interaction_update_interval
    @property
    def interaction_update_interval(self) -> int:
        return self._get_attr(
            "interactionUpdateInterval", data_type="int", def_value=200
        )

    @interaction_update_interval.setter
    def interaction_update_interval(self, value: Optional[int]):
        self._set_attr("interactionUpdateInterval", value)

    # content property
    @property
    def content(self) -> Control:
        """
        List of widgets to be displayed in the carousel.
        """
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # constrained
    @property
    def constrained(self) -> bool:
        return self._get_attr("constrained", data_type="bool", def_value=True)

    @constrained.setter
    def constrained(self, value: Optional[bool]):
        self._set_attr("constrained", value)

    # on_interaction_update
    @property
    def on_interaction_update(
            self,
    ) -> OptionalEventCallable[ExtendedInteractiveViewerUpdateEvent]:
        return self.__on_interaction_update.handler

    @on_interaction_update.setter
    def on_interaction_update(
            self,
            handler: OptionalEventCallable[ExtendedInteractiveViewerUpdateEvent],
    ):
        self.__on_interaction_update.handler = handler

    # scale_enabled
    @property
    def scale_enabled(self) -> bool:
        return self._get_attr("scaleEnabled", data_type="bool", def_value=True)

    @scale_enabled.setter
    def scale_enabled(self, value: Optional[bool]):
        self._set_attr("scaleEnabled", value)

    # scale_factor
    @property
    def scale_factor(self) -> float:
        return self._get_attr("scaleFactor", data_type="float", def_value=200)

    @scale_factor.setter
    def scale_factor(self, value: OptionalNumber):
        self._set_attr("scaleFactor", value)

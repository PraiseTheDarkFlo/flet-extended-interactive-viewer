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
    """
    Event triggered by `FletExtendedInteractiveViewer` whenever the user interacts with the viewer.

    Attributes:
        offset_x (float): The X offset of the content in the Interactive Viewer.
        offset_y (float): The Y offset of the content in the Interactive Viewer.
        scale (float): The scale of the content in the Interactive Viewer.

    Example:
        ```python
        def update_handler(event: ExtendedInteractiveViewerUpdateEvent):
            print(event.offset_x, event.offset_y, event.scale)

        FletExtendedInteractiveViewer(
                    content=ft.Container(width=900,height=800,gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=[ft.Colors.PINK, ft.Colors.ORANGE_700],
                    )),
                    width=400, height=250,
                    on_interaction_update=update_handler,
                )

        ```
    """
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.offset_x: float = d.get("offset_x")
        self.offset_y: float = d.get("offset_y")
        self.scale: float = d.get("scale")

class FletExtendedInteractiveViewer(ConstrainedControl, AdaptiveControl):
    """
    Flet-Extended-Interactive-Viewer is a [Flet](https://flet.dev/) control that provides multiple customization options for displaying two-dimensional content.

    Highlights:
        - **XY Scrollbars:** Synchronized scrollbars for the InteractiveViewer.
        - **XY Scrollbar Options:** Easy to customize the experience e.g. you can disable the interaction with the scrollbars or disable Y scrollbars.
        - **Panning:** Supports panning like `ft.InteractiveViewer`, with synchronized scrollbars. You can also disable panning to use only the scrollbars.
        - **Zoom:** Zoom with the mouse/touchpad or via a function call. When zooming via a function call, the zoom can be limited to the content size.
        - **Transformation data:** Provides access to the transformation applied to the content.


    Attributes:
        content (Control): The `Control` to be transformed by the `FletExtendedInteractiveViewer`.
        x_scroll_enabled (bool): Whether the Interactive Viewer should have an x_scroll_bar.

            **Default:** `True`
        y_scroll_enabled (bool): Whether the Interactive Viewer should have a y_scroll_bar.

            **Default:** `True`
        over_zoom_enabled (bool): Whether the Interactive Viewer allows the user with function calls to zoom larger than the content.

            **Default:** `False`
        interactive_scroll_enabled (bool): Whether the scrollbars should be interactive or not.

            **Default:** `True`
        pan_enabled (bool): Whether if it should be possible to move in the Interactive Viewer with panning.

            **Default:** `True`
        max_scale (float): The max possible scaling for zooming with mouse/touchpad.

            **Default:** `2.5`
        min_scale (float): The min possible scaling for zooming with mouse/touchpad.

            **Default:** `0.8`
        scale_factor (float): The amount of scale to be performed per pointer scroll.

            **Default:** `200.0`
        scale_enabled (bool): Whenever it should be possible zoome with mouse/touchpad.

            **Default:** `True`
        constrained (bool): Whether the normal size constraints at this point in the widget tree are applied to the child.

            **Default:** `True`
        on_interaction_update (Callable): Fires when the user interacts with the viewer.

            **Event Handler argument type:** `ExtendedInteractiveViewerUpdateEvent`


    Example:
        ```python
        def update_handler(event: ExtendedInteractiveViewerUpdateEvent):
            print(event.offset_x, event.offset_y, event.scale)

        FletExtendedInteractiveViewer(content=ft.Container(width=900,height=800,gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=[ft.Colors.PINK, ft.Colors.ORANGE_700],
                    )),
                    x_scroll_enabled = True,
                    y_scroll_enabled = True,
                    over_zoom_enabled = False,
                    interactive_scroll_enabled = True,
                    pan_enabled = True,
                    max_scale = 2.5,
                    min_scale = 0.8,
                    scale_factor = 0.8,
                    scale_enabled = True,
                    constrained = True,
                    on_interaction_update=update_handler,
                    )
        ```
    """

    def __init__(
        self,
            #special
            content: Control,
            x_scroll_enabled: Optional[bool] = None,
            y_scroll_enabled: Optional[bool] = None,
            over_zoom_enabled: Optional[bool] = None,
            interactive_scroll_enabled: Optional[bool] = None,
            pan_enabled: Optional[bool] = None,
            max_scale: OptionalNumber = None,
            min_scale: OptionalNumber = None,
            scale_factor: OptionalNumber = None,
            scale_enabled: Optional[bool] = None,
            constrained: Optional[bool] = None,
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
        self.x_scroll_enabled = x_scroll_enabled
        self.y_scroll_enabled = y_scroll_enabled
        self.over_zoom_enabled = over_zoom_enabled
        self.interactive_scroll_enabled = interactive_scroll_enabled
        self.pan_enabled = pan_enabled
        self.scale_enabled = scale_enabled
        self.constrained = constrained
        self.max_scale = max_scale
        self.min_scale = min_scale
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

    def get_transformation_data(self):
        """
        Gets the transformation data which is applied to the content of the Interactive Viewer.

        Returns:
            offset_x (float): The x offset of the transformation data.
            offset_y (float): The y offset of the transformation data.
            scale (float): The scale of the transformation data.

        Example:
            ```python
            fei= FletExtendedInteractiveViewer(content=ft.Container(width=900,height=800,gradient=ft.LinearGradient(
                            begin=ft.alignment.top_left,
                            end=ft.alignment.bottom_right,
                            colors=[ft.Colors.PINK, ft.Colors.ORANGE_700],
                        )))

            offset_x,offset_y,scale = fei.get_transformation_data()
            print(offset_x, offset_y, scale)
            ```
        """
        data = self.invoke_method("get_transformation_data", {}, wait_for_result=True)
        d = json.loads(data)
        offset_x: float = d.get("offset_x")
        offset_y: float = d.get("offset_y")
        scale: float = d.get("scale")
        return offset_x, offset_y, scale

    def set_transformation_data(self, offset_x: OptionalNumber = None, offset_y: OptionalNumber = None, scale: OptionalNumber = None, animation_duration: Optional[DurationValue] = None):
        """
        Sets the transformation data which is applied to the content of the Interactive Viewer.

        Attributes:
            offset_x (float): The x offset of the transformation data.

                **Default:** `0.0`

            offset_y (float): The y offset of the transformation data.

                **Default:** `0.0`
            scale (float): The scale of the transformation data.

                **Default:** `0.0`
            animation_duration (DurationValue): The duration of the animation.

                **Default:** `0`

        Example:
            ```python
            fei= FletExtendedInteractiveViewer(content=ft.Container(width=900,height=800,gradient=ft.LinearGradient(
                            begin=ft.alignment.top_left,
                            end=ft.alignment.bottom_right,
                            colors=[ft.Colors.PINK, ft.Colors.ORANGE_700],
                        )))

            fei.set_transformation_data(-100.0, -100.0, 1.0)
            ```
        """
        self.invoke_method(
            "set_transformation_data", arguments={"offSetX": self._convert_attr_json(offset_x), "offSetY": self._convert_attr_json(offset_y), "scale": self._convert_attr_json(scale), "duration": self._convert_attr_json(animation_duration)},
        )

    def reset(self, animation_duration: Optional[DurationValue] = None):
        """
        Resets the transformation done on the content of the Interactive Viewer.
        By default, the reset happens with no animation (immediately).

        Attributes:
            animation_duration (DurationValue): The duration of the animation.

                **Default:** `0`

        Example:
            ```python
            fei= FletExtendedInteractiveViewer(content=ft.Container(width=900,height=800,gradient=ft.LinearGradient(
                            begin=ft.alignment.top_left,
                            end=ft.alignment.bottom_right,
                            colors=[ft.Colors.PINK, ft.Colors.ORANGE_700],
                        )))

            fei.reset(400)
            ```
        """
        self.invoke_method(
            "reset", arguments={"duration": self._convert_attr_json(animation_duration)}
        )

    def zoom(self, factor: Number):
        """
        Zooming in or out in the Interactive Viewer.

        Arguments:
            factor (float): The zoom factor.

                Values below `1` will zoom out, values above `1` will zoom in.

        Example:
            ```python
            fei= FletExtendedInteractiveViewer(content=ft.Container(width=900,height=800,gradient=ft.LinearGradient(
                            begin=ft.alignment.top_left,
                            end=ft.alignment.bottom_right,
                            colors=[ft.Colors.PINK, ft.Colors.ORANGE_700],
                        )),
                        over_zoom_enabled = False,
                        )

            fei.zoom(1.25) #Zooms in
            ```
        """
        self.invoke_method("zoom", arguments={"factor": str(factor)})

    # pan_enabled
    @property
    def pan_enabled(self) -> bool:
        return self._get_attr("panEnabled", data_type="bool", def_value=True)

    @pan_enabled.setter
    def pan_enabled(self, value: Optional[bool]):
        self._set_attr("panEnabled", value)

    # over_zoom_enabled
    @property
    def over_zoom_enabled(self) -> bool:
        return self._get_attr("overZoomEnabled", data_type="bool", def_value=False)

    @over_zoom_enabled.setter
    def over_zoom_enabled(self, value: Optional[bool]):
        self._set_attr("overZoomEnabled", value)

    # x_scroll_enabled
    @property
    def x_scroll_enabled(self) -> bool:
        return self._get_attr("xScrollEnabled", data_type="bool", def_value=True)

    @x_scroll_enabled.setter
    def x_scroll_enabled(self, value: Optional[bool]):
        self._set_attr("xScrollEnabled", value)

    # y_scroll_enabled
    @property
    def y_scroll_enabled(self) -> bool:
        return self._get_attr("yScrollEnabled", data_type="bool", def_value=True)

    @y_scroll_enabled.setter
    def y_scroll_enabled(self, value: Optional[bool]):
        self._set_attr("yScrollEnabled", value)

    # interactive_scroll_enabled
    @property
    def interactive_scroll_enabled(self) -> bool:
        return self._get_attr("interactiveScrollEnabled", data_type="bool", def_value=True)

    @interactive_scroll_enabled.setter
    def interactive_scroll_enabled(self, value: Optional[bool]):
        self._set_attr("interactiveScrollEnabled", value)

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


    # content property
    @property
    def content(self) -> Control:
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

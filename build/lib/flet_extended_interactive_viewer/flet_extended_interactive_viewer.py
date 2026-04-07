from dataclasses import dataclass
from typing import Optional, Annotated

from flet import Control
from flet.utils.validation import V

__all__ = [
    "FletExtendedInteractiveViewer",
    "FEIUpdateEvent",
]

import flet as ft

@dataclass
class FEIUpdateEvent(ft.Event["FletExtendedInteractiveViewer"]):
    """
    Event raised when the user interacts with the viewer.

    Example:
        ```python
        import flet as ft
        from flet_extended_interactive_viewer import FletExtendedInteractiveViewer, FEIUpdateEvent

        def main(page: ft.Page):
            def on_update(e: FEIUpdateEvent):
                print(e.offset_x, e.offset_y, e.scale)

            fei = FletExtendedInteractiveViewer(
                content=ft.Container(width=900, height=800, gradient=ft.LinearGradient(
                    colors=[ft.Colors.PINK, ft.Colors.ORANGE_700],
                )),
                width=400, height=250,
                on_interaction_update=on_update,
            )
            page.add(fei)

        ft.run(main)
        ```
    """
    offset_x: float
    """
    The X offset of the content in the Interactive Viewer.
    """
    offset_y: float
    """
    The Y offset of the content in the Interactive Viewer.
    """
    scale: float
    """
    The scale of the content in the Interactive Viewer.
    """

@ft.control("FletExtendedInteractiveViewer")
class FletExtendedInteractiveViewer(ft.LayoutControl):
    content: Annotated[Control,V.visible_control]
    x_scroll_enabled: bool = True
    y_scroll_enabled: bool = True
    over_zoom_enabled: bool = False
    interactive_scroll_enabled: bool = True
    pan_enabled: bool = True
    min_scale: ft.Number = 0.8
    max_scale: ft.Number = 2.5
    scale_enabled: bool = True
    scale_factor: ft.Number = 200.0
    constrained: bool = False
    on_interaction_update: Optional[ft.EventHandler[FEIUpdateEvent]] = None
    #scrollbarTheme
    thumb_color: Optional[ft.Colors] = None
    thumb_visible: bool = True

    async def get_transformation_data(self):
        data = await self._invoke_method("get_transformation_data", {})
        print(data["offset_x"], data["offset_y"], data["scale"])
        return data["offset_x"], data["offset_y"], data["scale"]

    async def set_transformation_data(self, offset_x: Optional[ft.Number] = None, offset_y: Optional[ft.Number] = None,
                                scale: Optional[ft.Number] = None, animation_duration: Optional[ft.DurationValue] = None):
        await self._invoke_method(
            "set_transformation_data",
            arguments={"offSetX": offset_x, "offSetY": offset_y,
                       "scale": scale,
                       "duration": animation_duration},
        )

    async def reset(self, animation_duration: Optional[ft.DurationValue] = None):
        await self._invoke_method(
            "reset", arguments={"duration": animation_duration}
        )

    async def zoom(self, factor: ft.Number):
        await self._invoke_method("zoom", arguments={"factor": factor})
# flet-extended-interactive-viewer
[![PyPI version](https://img.shields.io/pypi/v/flet-extended-interactive-viewer.svg)](https://pypi.org/project/flet-extended-interactive-viewer/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Flet](https://img.shields.io/badge/Flet-0.84.0+-green.svg)](https://flet.dev)
[![License](https://img.shields.io/github/license/PraiseTheDarkFlo/flet-extended-interactive-viewer.svg)](https://github.com/PraiseTheDarkFlo/flet-extended-interactive-viewer/blob/master/LICENSE)
> **Flet-Extended-Interactive-Viewer is a powerful 2D navigation control for [Flet](https://flet.dev/) that adds synchronized scrollbars and enhanced transformation control to the standard InteractiveViewer.**

> [!IMPORTANT]
> **Update:** Upgraded to **Flet v0.84.0** and introduced customizable scrollbar thumb colors via `thumbs_color`.

## 🌟 Key Features:
- **Synchronized XY Scrollbars:** Real-time visual feedback and manual scrolling for both axes, perfectly synced with panning and zoom.
- **Granular Navigation:** Toggle panning, scroll-axis visibility, and scrollbar interaction independently to suit your tool's needs.
- **Precision Zooming:** Smooth zoom control via mouse/touchpad or function calls, with optional constraints to keep content within the viewport.
- **Transformation API:** Direct programmatic access to current offsets (X, Y) and scale factors for real-time UI synchronization.
- **Flexible Layouts:** Supports both constrained and unconstrained content, making it ideal for everything from document viewers to infinite canvas editors.

## ℹ️ Overview

This extension was developed as part of a Bachelor Thesis, supervised by [Erik Kubaczka](https://github.com/ERIK-KE) at the [Self-Organizing Systems Lab](https://www.bcs.tu-darmstadt.de/welcome/index.en.jsp) of the Technical University Darmstadt. FletExtendedInteractiveViewer is a powerful control for [Flet](https://flet.dev/) which enables the user to customize an interactive content view experience.

## 📖 Documentation

Documentation to this package can be found [here](https://PraiseTheDarkFlo.github.io/flet-extended-interactive-viewer/).

## 🚀 Example
### Demo
![Example](https://github.com/PraiseTheDarkFlo/flet-extended-interactive-viewer/blob/master/docs/gifs/usage_extended_interactive_viewer.gif?raw=true)

### Code
```python
import flet as ft

from flet_extended_interactive_viewer import FletExtendedInteractiveViewer, FEIUpdateEvent



def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    text = ft.Text("MOVE ME",size=50)

    def on_click(ex:FletExtendedInteractiveViewer=None,text_move:ft.Text=None):
        if ex.pan_enabled:
            ex.pan_enabled = False
            text_move.value = "PAN DISABLED"
        else:
            ex.pan_enabled = True
            text_move.value = "MOVE ME"
        ex.update()
        text_move.update()

    def on_update(e: FEIUpdateEvent):
        print((e.offset_x,e.offset_y,e.scale))


    def toggle_scroll_x(ex:FletExtendedInteractiveViewer=None):
        ex.x_scroll_enabled = not ex.x_scroll_enabled
        ex.update()
    def toggle_scroll_y(ex: FletExtendedInteractiveViewer = None):
        ex.y_scroll_enabled = not ex.y_scroll_enabled
        ex.update()

    def toggle_interactive(ex: FletExtendedInteractiveViewer = None):
        ex.interactive_scroll_enabled = not ex.interactive_scroll_enabled
        ex.update()

    fei = FletExtendedInteractiveViewer(
        content=ft.Container(text,width=900,height=800,gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=[ft.Colors.PINK, ft.Colors.ORANGE_700],
        )),
        on_interaction_update=on_update,
        width=400, height=250
    )

    async def reset():
        await fei.reset(400)

    async def zoom_in():
        await fei.zoom(1.25)

    async def zoom_out():
        await fei.zoom(0.75)

    text_x_y_scale = ft.Text("offset_x=?, offset_y=?, scale=?")

    async def get_transformation_click():
        x, y, scale = await fei.get_transformation_data()
        text_x_y_scale.value = f"offset_x={round(x)}, offset_y={round(y)}, scale={scale}"
        text_x_y_scale.update()

    async def set_transformation_data():
        await fei.set_transformation_data(offset_x=-100, offset_y=-100, scale=1.0)

    page.add(ft.Row([
        ft.Column([text_x_y_scale,
                   fei,
                   ft.Row([ft.Button("toggle pan", on_click=lambda e, ex=fei, text_move=text:on_click(ex, text_move)), ft.Button("toggle interactive_scroll_bar", on_click=lambda e, ex=fei:toggle_interactive(ex))]), ft.Row([ft.Button("toggle scroll_bar_x", on_click=lambda e, ex=fei:toggle_scroll_x(ex)), ft.Button("toggle scroll_bar_y", on_click=lambda e, ex=fei:toggle_scroll_y(ex))]),
                   ft.Row([ft.Button("reset",on_click=reset),ft.Button("zoom in",on_click=zoom_in),ft.Button("zoom out",on_click=zoom_out)]),
                   ft.Row([ft.Button("get_transformation", on_click=get_transformation_click), ft.Button("set_transformation(-100,-100,1)", on_click=set_transformation_data)]),
                   ],alignment=ft.MainAxisAlignment.CENTER)],alignment=ft.MainAxisAlignment.CENTER),

    )


ft.run(main)
```

## ⬇️ Installation
> [!WARNING]
> **Custom Control:** This extension requires a one-time build. It will **NOT** work with the default `flet run` command unless you have previously built the app for your platform.

To install the `flet-extended-interactive-viewer` package:

- Using `uv`:
    ```bash
    uv add flet-extended-interactive-viewer
    ```
 
- Using `pip`:
    ```bash
    pip install flet-extended-interactive-viewer
    ```
    After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.


- Using `poetry`:
    ```bash
    poetry add flet-extended-interactive-viewer
    ```
  
Build your app:
- Using Linux:

    ```bash
    flet build linux -v
    ```
- Using Mac:

    ```bash
    flet build macos -v
    ```
- Using Windows:

    ```bash
    flet build windows -v
    ```

## 📝 License

This project is licensed under the **MIT license** – see the [LICENSE](LICENSE) file for details.


## 💭 Feedback & Contributions

Report bugs or suggest features via [GitHub Issues](https://github.com/PraiseTheDarkFlo/flet-extended-interactive-viewer/issues).
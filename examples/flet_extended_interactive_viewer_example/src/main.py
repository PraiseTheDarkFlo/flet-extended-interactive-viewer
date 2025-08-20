import flet as ft

from flet_extended_interactive_viewer import FletExtendedInteractiveViewer


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

    def get_transformation_click(ex:FletExtendedInteractiveViewer=None,text_update:ft.Text=None):
        x, y, scale = ex.get_transformation_data()
        text_update.value = f"offset_x={round(x)}, offset_y={round(y)}, scale={scale}"
        text_update.update()
    def toggle_scroll_x(ex:FletExtendedInteractiveViewer=None):
        ex.x_scroll_enabled = not ex.x_scroll_enabled
        ex.update()
    def toggle_scroll_y(ex: FletExtendedInteractiveViewer = None):
        ex.y_scroll_enabled = not ex.y_scroll_enabled
        ex.update()

    def toggle_interactive(ex: FletExtendedInteractiveViewer = None):
        ex.interactive_scroll_enabled = not ex.interactive_scroll_enabled
        ex.update()
    extended = FletExtendedInteractiveViewer(
                    content=ft.Container(text,width=900,height=800,gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=[ft.Colors.PINK, ft.Colors.ORANGE_700],
                    )),
                    width=400, height=250,constrained=False,pan_enabled=True,
                )
    text_x_y_scale = ft.Text("offset_x=?, offset_y=?, scale=?")
    page.add(ft.Row([
        ft.Column([text_x_y_scale,
                extended,
                   ft.Row([ft.Button("toggle pan",on_click=lambda e,ex=extended,text_move=text:on_click(ex,text_move)),ft.Button("toggle interactive_scroll_bar",on_click=lambda e,ex=extended:toggle_interactive(ex))]),ft.Row([ft.Button("toggle scroll_bar_x",on_click=lambda e,ex=extended:toggle_scroll_x(ex)),ft.Button("toggle scroll_bar_y",on_click=lambda e,ex=extended:toggle_scroll_y(ex))]),
                   ft.Row([ft.Button("reset",on_click=lambda e,ex=extended:ex.reset()),ft.Button("zoom in",on_click=lambda e,ex=extended:ex.zoom(1.25)),ft.Button("zoom out",on_click=lambda e,ex=extended:ex.zoom(0.75))]),
                   ft.Row([ft.Button("get_transformation",on_click=lambda e, ex=extended, x_y_scale=text_x_y_scale: get_transformation_click(ex,text_x_y_scale)),ft.Button("set_transformation(-100,-100,1)",on_click=lambda e,ex=extended:ex.set_transformation_data(offset_x=-100,offset_y=-100))])
                   ],alignment=ft.MainAxisAlignment.CENTER)],alignment=ft.MainAxisAlignment.CENTER),

    )


ft.app(main)

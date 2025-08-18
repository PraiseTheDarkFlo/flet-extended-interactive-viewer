import flet as ft

from flet_extended_interactive_viewer import FletExtendedInteractiveViewer,ExtendedInteractiveViewerUpdateEvent


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    text = ft.Text("TEST")
    def on_update(e:ExtendedInteractiveViewerUpdateEvent,text2:ft.Text):
        text2.value = e.offset_x
        text2.update()

    def on_click(ex:FletExtendedInteractiveViewer=None):
        x,y,scale = ex.get_transformation_data()
        print(x,y,scale)

    extended = FletExtendedInteractiveViewer(
                    content=ft.Container(text,width=3000,height=1000,bgcolor=ft.Colors.PINK),
                    width=300, height=150,constrained=False,
                    on_interaction_update=lambda e,txt=text: on_update(e,text),
                )
    page.add(
        ft.Column([ft.Container(ft.Text("TEST"),width=300,height=100),
                extended,
                   ft.Button("test",on_click=lambda e,ex=extended:on_click(ex))
                ])

    )


ft.app(main)

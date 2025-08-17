# Introduction

FletExtendedInteractiveViewer for Flet.

## Examples

```
import flet as ft

from flet_extended_interactive_viewer import FletExtendedInteractiveViewer


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(

                ft.Container(height=150, width=300, alignment = ft.alignment.center, bgcolor=ft.Colors.PURPLE_200, content=FletExtendedInteractiveViewer(
                    tooltip="My new FletExtendedInteractiveViewer Control tooltip",
                    value = "My new FletExtendedInteractiveViewer Flet Control", 
                ),),

    )


ft.app(main)
```

## Classes

[FletExtendedInteractiveViewer](FletExtendedInteractiveViewer.md)



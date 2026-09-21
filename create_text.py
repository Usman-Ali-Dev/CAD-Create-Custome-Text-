from OCC.Core.gp import gp_Pnt
from OCC.Display.SimpleGui import init_display


def create_text(
    display,
    text="Hello CAD",
    position=(0, 0, 0),
    size=20,
    color=(1.0, 1.0, 1.0)
):

    point = gp_Pnt(*position)

    display.DisplayMessage(
        point,
        text,
        update=True,
        height=size,
        message_color=color
    )


if __name__ == "__main__":

    display, start_display, _, _ = init_display()

    create_text(
        display,
        text="Usman",
        position=(170, 0, 89),
        size=30,
        color=(1.0, 0.0, 0.0)   # Red
    )


    start_display()
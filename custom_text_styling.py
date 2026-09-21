from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Ax2
from OCC.Core.Graphic3d import Graphic3d_TransformPers, Graphic3d_TMF_2d
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Display.SimpleGui import init_display
from OCC.Core.AIS import AIS_TextLabel
from OCC.Core.TCollection import TCollection_ExtendedString


def create_text(
    display,
    text="Hello CAD",
    position=(0, 0, 0),
    height=20,
    color=(1.0, 1.0, 1.0),
    angle=0.0,
    font="Arial",
    is_bold=False,
    is_italic=False,
    is_underlined=False,
    zoom_persistent=False
):
    pnt = gp_Pnt(*position)
    color_obj = Quantity_Color(color[0], color[1], color[2], Quantity_TOC_RGB)

    text_label = AIS_TextLabel()
    text_label.SetText(TCollection_ExtendedString(text))
    text_label.SetPosition(pnt)
    text_label.SetColor(color_obj)
    text_label.SetHeight(height)
    text_label.SetFont(font)

    if is_bold and is_italic:
        text_label.SetAspect("bolditalic")
    elif is_bold:
        text_label.SetAspect("bold")
    elif is_italic:
        text_label.SetAspect("italic")

    if is_underlined:
        text_label.SetUnderline(True)

    if angle != 0.0:
        ax = gp_Ax2(pnt, gp_Dir(0, 0, 1))
        text_label.SetOrientation(ax)

    if zoom_persistent:
        text_label.SetTransformPersistence(Graphic3d_TransformPers(Graphic3d_TMF_2d, pnt))

    display.Context.Display(text_label, True)
    return text_label


if __name__ == "__main__":

    display, start_display, _, _ = init_display()
    
    display.View.Redraw()

    create_text(display, "Usman",                (0, 0, 200), height=50, color=(1, 0, 0),   is_bold=True)
    # create_text(display, "Bold + Italic Text",   (0, 0, 130), height=40, color=(0, 1, 0),   is_bold=True, is_italic=True)
    # create_text(display, "Rotated Text 45°",     (100, 0, 80), height=35, color=(0, 0, 1),  angle=45)
    # create_text(display, "Underlined Text",     (-80, 80, 50), height=30, color=(1, 1, 0),  is_underlined=True)
    # create_text(display, "Zoom Persistent",     (-150, -50, 30), height=28, color=(1, 0.5, 0), zoom_persistent=True)

    start_display() 
     
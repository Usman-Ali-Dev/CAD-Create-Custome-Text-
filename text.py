from OCC.Core.gp import gp_Ax3, gp_Pnt, gp_Dir, gp_Trsf
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.Addons import text_to_brep, Font_FA_Regular, Font_FA_Bold, Font_FA_Italic, Font_FA_BoldItalic
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.XCAFDoc import XCAFDoc_ColorGen, XCAFDoc_ColorSurf, XCAFDoc_ColorCurv, XCAFDoc_DocumentTool
from OCC.Core.XCAFApp import XCAFApp_Application
from OCC.Core.TDocStd import TDocStd_Document
from OCC.Core.STEPCAFControl import STEPCAFControl_Writer
from OCC.Core.Interface import Interface_Static

FONT_ASPECT_MAP = {
    "regular": Font_FA_Regular,
    "bold": Font_FA_Bold,
    "italic": Font_FA_Italic,
    "bolditalic": Font_FA_BoldItalic,
}


COLOR_TYPE_MAP = {
    "general": XCAFDoc_ColorGen,
    "surface": XCAFDoc_ColorSurf,
    "curve": XCAFDoc_ColorCurv,
}


def create_text_step(
    text_str="Hello PythonOCC",
    font="Arial",
    font_aspect="regular",
    height=10.0,
    composite_curve=True,
    position=(0, 0, 0),
    direction=(0, 0, 1),
    x_dir=(1, 0, 0),
    color=(1.0, 1.0, 1.0),
    color_type="surface",
    output_file="text_export.stp",
    step_schema="AP214IS",
):
    aspect = FONT_ASPECT_MAP.get(font_aspect.lower(), Font_FA_Regular)

    text_shape = text_to_brep(text_str, font, aspect, height, composite_curve)

    if position != (0, 0, 0) or direction != (0, 0, 1) or x_dir != (1, 0, 0):
        ax3 = gp_Ax3(gp_Pnt(*position), gp_Dir(*direction), gp_Dir(*x_dir))
        trsf = gp_Trsf()
        trsf.SetTransformation(ax3)
        text_shape = BRepBuilderAPI_Transform(text_shape, trsf, True).Shape()

    app = XCAFApp_Application.GetApplication()
    doc = TDocStd_Document("MDTV-XCAF")
    app.NewDocument("MDTV-XCAF", doc)
    shape_tool = XCAFDoc_DocumentTool.ShapeTool(doc.Main())
    color_tool = XCAFDoc_DocumentTool.ColorTool(doc.Main())

    shape_label = shape_tool.AddShape(text_shape, True)

    color_obj = Quantity_Color(color[0], color[1], color[2], Quantity_TOC_RGB)
    color_type_enum = COLOR_TYPE_MAP.get(color_type.lower(), XCAFDoc_ColorSurf)
    color_tool.SetColor(shape_label, color_obj, color_type_enum)

    step_writer = STEPCAFControl_Writer()
    Interface_Static.SetCVal("write.step.schema", step_schema)
    step_writer.Transfer(doc)
    status = step_writer.Write(output_file)

    if status == 1:
        print(f"STEP file written successfully: {output_file}")
    else:
        print(f"STEP export failed with status: {status}")

    app.Close(doc)
    return output_file


if __name__ == "__main__":
    create_text_step(
        text_str="Usman",
        font="Arial",
        font_aspect="italic",
        composite_curve=False,
        height=3.0,
        position=(0, 90, 0),
        color=(1.0, 1.0, 0.0),
        color_type="surface",
        output_file="test.stp",
    )

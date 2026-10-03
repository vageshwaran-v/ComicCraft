import os
from datetime import datetime

from fpdf import FPDF


def save_pdf(layout):
    os.makedirs(
        "static/exports",
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = f"comic_{timestamp}.pdf"

    filepath = os.path.join(
        "static",
        "exports",
        filename
    )

    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4"
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    for panel in layout:

        pdf.add_page()

        # Panel title
        pdf.set_font(
            "Helvetica",
            "B",
            18
        )

        pdf.cell(
            0,
            12,
            f"Panel {panel['panel_number']}: {panel['title']}",
            ln=True
        )

        # Image
        image_path = panel["image_path"]

        if image_path.startswith("/"):
            image_path = image_path[1:]

        if os.path.exists(image_path):
            pdf.image(
                image_path,
                x=15,
                y=30,
                w=180
            )

        pdf.ln(105)

        # Scene
        pdf.set_font(
            "Helvetica",
            "B",
            12
        )

        pdf.cell(
            0,
            8,
            "Scene:",
            ln=True
        )

        pdf.set_font(
            "Helvetica",
            "",
            10
        )

        pdf.multi_cell(
            0,
            6,
            panel["scene_description"]
        )

        pdf.ln(3)

        # Caption
        pdf.set_font(
            "Helvetica",
            "B",
            12
        )

        pdf.cell(
            0,
            8,
            "Caption:",
            ln=True
        )

        pdf.set_font(
            "Helvetica",
            "",
            10
        )

        pdf.multi_cell(
            0,
            6,
            panel["caption"]
        )

        pdf.ln(3)

        # Narration
        pdf.set_font(
            "Helvetica",
            "B",
            12
        )

        pdf.cell(
            0,
            8,
            "Narration:",
            ln=True
        )

        pdf.set_font(
            "Helvetica",
            "",
            10
        )

        pdf.multi_cell(
            0,
            6,
            panel["narration"]
        )

        pdf.ln(3)

        # Dialogue
        pdf.set_font(
            "Helvetica",
            "B",
            12
        )

        pdf.cell(
            0,
            8,
            "Dialogue:",
            ln=True
        )

        pdf.set_font(
            "Helvetica",
            "",
            10
        )

        pdf.multi_cell(
            0,
            6,
            panel["dialogue"]
        )

    pdf.output(filepath)

    return f"/static/exports/{filename}"
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates

from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf


router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


# ==========================================
# HOME PAGE
# ==========================================

@router.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# ==========================================
# GENERATE COMIC
# ==========================================

@router.post("/generate")
async def generate_comic(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...)
):

    # --------------------------------------
    # STEP 1: Generate 5-panel outline
    # --------------------------------------

    outline = generate_outline(
        story_prompt,
        character_name,
        setting,
        tone,
        art_style
    )


    # --------------------------------------
    # STEP 2: Generate detailed story
    # --------------------------------------

    story = generate_story(
        story_prompt,
        character_name,
        setting,
        tone,
        outline
    )


    # --------------------------------------
    # STEP 3: Generate images
    # --------------------------------------

    image_paths = []

    for panel in outline:

        image_path = generate_image(
            panel["image_prompt"],
            panel["panel_number"]
        )

        image_paths.append(image_path)


    # --------------------------------------
    # STEP 4: Build comic layout
    # --------------------------------------

    layout = build_comic_layout(
        outline,
        story,
        image_paths
    )


    # --------------------------------------
    # STEP 5: Generate PDF
    # --------------------------------------

    pdf_path = save_pdf(layout)


    # --------------------------------------
    # STEP 6: Show comic preview
    # --------------------------------------

    return templates.TemplateResponse(
        request=request,
        name="comic_preview.html",
        context={
            "layout": layout,
            "pdf_path": pdf_path
        }
    )


# ==========================================
# EXPORT SUCCESS PAGE
# ==========================================

@router.get("/export-success")
async def export_success(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={}
    )


# ==========================================
# TEST IMAGE GENERATION
# ==========================================

@router.get("/test-image")
async def test_image():

    image_path = generate_image(
        "A brave fox exploring an enchanted forest, colorful comic book illustration",
        999
    )

    return {
        "message": "Image generated successfully",
        "image": image_path
    }
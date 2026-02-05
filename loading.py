from UI import Col, Row, Html, ui

def showLoading(page: str, child=False):
    with Col().classes(f"{'w-[95vw] h-[95vh]' if not child else ''} items-center justify-center") as c:
        with Row().classes("w-fit h-fit items-center"):
            ui.spinner("grid", size='lg')
            Html(f"Loading <span class='text-primary font-bold'>{page}</span>...").classes("text-lg")
    return c
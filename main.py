from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import Response
from pydantic import BaseModel
from playwright.async_api import async_playwright
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="HTML to PDF Service", description="Converts HTML content to PDF using Playwright")

class PdfRequest(BaseModel):
    html: str
    filename: str = "document.pdf"

@app.get("/")
async def root():
    return {"status": "ok", "service": "HtmlToPdfService"}

@app.post("/generate-pdf")
async def generate_pdf(request: PdfRequest):
    """
    Generates a PDF from the provided HTML string.
    """
    logger.info(f"Received PDF generation request for filename: {request.filename}")
    
    try:
        async with async_playwright() as p:
            # Launch the browser
            # We use 'chromium' which is generally fast and reliable for this
            browser = await p.chromium.launch(headless=True)
            
            # Create a context (like a fresh browser window)
            context = await browser.new_context()
            
            # Create a page
            page = await context.new_page()
            
            # Set the content
            # wait_until="networkidle" is crucial for loading external assets (Tailwind CDN, Plotly JS)
            await page.set_content(request.html, wait_until="networkidle")
            
            # Optional: Add a small delay if animations or delayed renders are suspected
            # await page.wait_for_timeout(1000) 
            
            # Generate PDF
            # print_background=True ensures CSS background colors/images are included
            pdf_data = await page.pdf(
                format="A4",
                print_background=True,
                margin={"top": "20px", "bottom": "20px", "left": "20px", "right": "20px"}
            )
            
            await browser.close()
            
            logger.info("PDF generated successfully")
            
            return Response(
                content=pdf_data, 
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename={request.filename}"}
            )
            
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

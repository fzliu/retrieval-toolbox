from io import BytesIO
import urllib.request

import pymupdf
from pymupdf import Document
from PIL import Image


def _pdf_to_screenshots(pdf: Document, zoom: float = 1.0) -> list[Image.Image]:

    images = []

    mat = pymupdf.Matrix(zoom, zoom)
    for n in range(pdf.page_count):
        pix = pdf[n].get_pixmap(matrix=mat)

        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    
    return images


def pdf_path_to_screenshots(path: str, zoom: float = 1.0) -> list[Image.Image]:
    """
    Extracts screenshots from a PDF file using PyMuPDF.
    
    Args:
        path: The path to the PDF file.
        zoom: The zoom factor for the screenshots (defaults to 1.0).
    
    Returns:
        A list of screenshots extracted from the PDF.
    """

    # Ensure that the path is valid
    if not path.endswith(".pdf"):
        raise ValueError("Invalid path")
    
    pdf = pymupdf.open(path, filetype="pdf")

    # Extract screenshots
    images = _pdf_to_screenshots(pdf, zoom = zoom)
    pdf.close()

    return images


def pdf_url_to_screenshots(url: str, zoom: float = 1.0) -> list[Image.Image]:
    """
    Extracts screenshots from a URL to a PDF using PyMuPDF.
    
    Args:
        path: The URL to the PDF file.
        zoom: The zoom factor for the screenshots (defaults to 1.0).
    
    Returns:
        A list of screenshots extracted from the PDF.
    """

    # Ensure that the URL is valid
    if not url.startswith("http") and url.endswith(".pdf"):
        raise ValueError("Invalid URL")

    # Read the PDF from the specified URL
    with urllib.request.urlopen(url) as response:
        pdf_data = response.read()
    pdf_stream = BytesIO(pdf_data)
    pdf = pymupdf.open(stream=pdf_stream, filetype="pdf")
    
    # Extract screenshots
    images = _pdf_to_screenshots(pdf, zoom = zoom)
    pdf.close()

    return images

from setuptools import setup, find_packages

setup(
    name="irish_law_analyzer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-multipart",
        "jinja2",
        "pdf2image",
        "pytesseract",
        "pdfplumber",
        "Pillow",
        "filetype",  # python-magic yerine filetype
        "pydantic-settings"
    ],
)
import streamlit as st
from PIL import Image
import os
import io
import tempfile
from pdf2image import convert_from_path
import cairosvg

def convert_png_to_jpg(png_file):
    temp_jpg_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    img = Image.open(png_file)
    img.save(temp_jpg_file, format="JPEG")
    temp_jpg_file.seek(0)
    return temp_jpg_file

def convert_jpg_to_png(jpg_file):
    temp_png_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    img = Image.open(jpg_file)
    img.save(temp_png_file, format="PNG")
    temp_png_file.seek(0)
    return temp_png_file

def convert_pdf_to_svg(pdf_file):
    svg_data = cairosvg.svg2svg(bytestring=pdf_file.read())
    return svg_data

def convert_svg_to_pdf(svg_data):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf_file:
        cairosvg.svg2pdf(bytestring=svg_data, write_to=temp_pdf_file)
        temp_pdf_file.seek(0)
        return temp_pdf_file

st.title("Image and Document Converter")

uploaded_file = st.file_uploader("Upload a file", type=["png", "jpg", "jpeg", "pdf", "svg"])

if uploaded_file:
    if uploaded_file.type in ["image/png", "image/jpeg"]:
        if st.button("Convert PNG to JPG"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_png_file:
                temp_png_file.write(uploaded_file.read())
                temp_png_file.seek(0)
                temp_jpg_file = convert_png_to_jpg(temp_png_file)
                st.image(temp_jpg_file)
                st.download_button(
                    label="Download JPG",
                    data=temp_jpg_file.read(),
                    file_name="output.jpg",
                    mime="image/jpeg"
                )

        if st.button("Convert JPG to PNG"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_jpg_file:
                temp_jpg_file.write(uploaded_file.read())
                temp_jpg_file.seek(0)
                temp_png_file = convert_jpg_to_png(temp_jpg_file)
                st.image(temp_png_file)
                st.download_button(
                    label="Download PNG",
                    data=temp_png_file.read(),
                    file_name="output.png",
                    mime="image/png"
                )

    elif uploaded_file.type in ["application/pdf"]:
        if st.button("Convert PDF to SVG"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf_file:
                temp_pdf_file.write(uploaded_file.read())
                temp_pdf_file.seek(0)
                svg_data = convert_pdf_to_svg(temp_pdf_file)
                st.markdown(svg_data, unsafe_allow_html=True)
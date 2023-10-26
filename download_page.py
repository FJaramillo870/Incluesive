import gradio as gr
from fpdf import *
import pyperclip

textInput = "There once was a farmer named..."


def download(output):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 10, str(output))
    pdf_file = "history_download.pdf"
    pdf.output(pdf_file)
    return pdf_file


def copyText(output):
    pyperclip.copy(output)
    text = pyperclip.paste()
    return text


with gr.Blocks() as demo:
    with gr.Accordion(label="Account"):
        preferences = gr.Button(value="Preferences")
        signout = gr.Button(value="Sign Out")
    with gr.Row():
        output = gr.Textbox(label="Output Textbox", value=textInput)
        file = gr.File()
    with gr.Row():
        download_btn = gr.Button(value="Download", scale=0)
        copy_btn = gr.Button(value="Copy", scale=0)
        done_btn = gr.Button(value="Done", scale=0)
        download_btn.click(fn=download, inputs=output, outputs=file, api_name="Download")
        copy_btn.click(fn=copyText, inputs=output, outputs=output, api_name="Copy")


demo.launch()
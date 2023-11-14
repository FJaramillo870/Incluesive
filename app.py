# Programmers: Anita Martin, Chris Heise, Dion Boyer, and Felix Jaramillo
# Course: BSSD 4350 - Agile Methodologies
# Instructor: Jonathan Lee
# Program: Inclusivity Editor App
# File: app.py

import gradio as gr
from difflib import Differ
from docx import *
from fpdf import *
import pyperclip

users_text = ""

canvas_html = """<iframe id='rich-text-root' style='width:100%' height='360px' src='file=RichTextEditor.html' frameborder='0' scrolling='no'></iframe>"""

# For testing, will be what the user inputs
EXAMPLE_TEXT = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris ultricies elementum nulla, id placerat nunc efficitur non. Nam tempus, nulla ac sodales laoreet, lacus tellus efficitur enim, eget sodales lorem ante ut neque. Mauris quis eros sed velit mollis porta. Aenean libero diam, sagittis sed arcu non, fermentum tincidunt leo. Nulla sed velit tempor, dapibus ex in, rhoncus orci. Praesent sit amet odio sagittis arcu venenatis consequat vitae vitae tortor. Sed et maximus nunc, nec placerat ligula.
Etiam libero nisi, fringilla a imperdiet in, luctus a tortor. Pellentesque quis venenatis velit, quis malesuada nisl. Praesent eu placerat ante. Vivamus quis mi porttitor, faucibus purus non, tempus lacus. Pellentesque et imperdiet dui. Vivamus ut lacus quis lacus maximus iaculis. Vivamus mollis odio orci, ut egestas nisl rhoncus nec. Quisque sit amet lorem viverra, lobortis erat quis, consectetur augue. Etiam blandit tempus purus nec maximus. Vestibulum tempus semper ipsum ac faucibus."""

# For testing, will be what the LLM returns
CORRECTED_TEXT = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris ultricies elementum nulla, id placerat nunc efficitur non. Nulla ac sodales laoreet, lacus tellus efficitur enim, eget sodales lorem ante ut neque. Mauris quis eros sed velit mollis porta. Aenean libero diam, sagittis sed arcu non, fermentum tincidunt leo. Nulla sed velit tempor, dapibus ex in, rhoncus orci. Praesent sit amet odio sagittis arcu venenatis consequat vitae vitae tortor. Sed et maximus nunc, nec placerat ligula.
Etiam libero nisi, fringilla a imperdiet in. Pellentesque quis venenatis velit, elit malesuada nisl. Praesent eu placerat ante. Vivamus quis mi porttitor, faucibus purus non, tempus lacus. Pellentesque et imperdiet dui. Vivamus ut lacus quis lacus maximus iaculis. Vivamus mollis odio orci, ut egestas nisl rhoncus nec. Quisque sit amet lorem viverra, lobortis erat quis, consectetur augue. Etiam blandit tempus purus nec maximus. Vestibulum tempus semper ipsum ac tortor."""

textInput = ""

DIFFERENCES = []


# Global Components (accessed by multiple tabs/pages)
original_text = gr.Textbox(
    label="Your Text",
    info="Your original text.",
    lines=10,
)

previewText = gr.Textbox(label="Output Textbox", value=textInput)

# Isn't currently working. Seems to need to be called with a button click like other componenets/functions
# Source: https://github.com/gradio-app/gradio/issues/2412


def update_preview(text):
    gr.Textbox(label="Output Textbox", value=textInput)
    return text


def change_page(page_number):
    """Changes the page to the page number passed in."""
    return gr.Tabs.update(selected=page_number)


def download(output, type):
    match type:
        case "PDF":
            """Download text as a PDF."""
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.multi_cell(0, 10, str(output))
            pdf_file = "history_download.pdf"
            pdf.output(pdf_file)
            return pdf_file
        case "DOCX":
            doc = Document()

            doc.add_heading('History Download', 0)
            doc.add_paragraph(output)
            doc_output = "history_download.docx"
            doc.save(doc_output)

            return doc_output
        case "TXT":
            text_file = 'history_download.txt'
            with open('history_download.txt', 'w') as txt_file:
                txt_file.write(output)
                txt_file.close()
            return text_file
        case _:
            """Download text as a PDF."""
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.multi_cell(0, 10, str(output))
            pdf_file = type + "history_download.pdf"
            pdf.output(pdf_file)
            return pdf_file


def copy_text(output):
    """Copy text to the clipboard."""
    pyperclip.copy(output)
    text = pyperclip.paste()


def load_text(temp_file):
    """Load text from a temporary file."""
    content = ""
    with open(temp_file.name, "r", encoding="utf-8") as f:
        content = f.read()
    return content


def submit_text(text):
    users_text = text
    text_input += users_text
    change_page(2)
    return users_text


def diff_texts(text1, text2):
    """Find the differences between two texts."""
    d = Differ()
    return [
        (token[2:], token[0] if token[0] != " " else None)
        for token in d.compare(text1, text2)
    ]


def dropdown_callback(value):
    return value


with gr.Blocks() as incluesive:
    gr.Markdown("# INCLUeSIVE")
    with gr.Tabs() as pages:


        """FIRST PAGE"""
        with gr.TabItem("Welcome", id=0) as first_page:
            with gr.Tabs():
                with gr.TabItem("Directions"):
                    gr.Markdown("Welcome to Incluesive an app that will help correcct your writings to be more incluesive of everyone. "
                    "To use Incluesive Pick a writing purpose then enter your text into the text box and submit. After you submit the changes to your text will be shown.")
                with gr.TabItem("Preferences"):
                    pref = gr.Button(value="Preferences", size='sm')
                    choice = gr.Radio(["Professional Correspondence", "Personal Correspondence", "Educational Paper", "Technical Instructions"],label="Writing purpose")
                    submit_button = gr.Button("Submit", link="")
                    submit_button.click(inputs=choice, outputs=None)
        """END FIRST PAGE"""


        """SECOND PAGE"""
        with gr.TabItem("Input", id=1) as second_page:
            with gr.Tab("Type/Paste"):
                text_input = gr.Textbox(
                    label="Your Text",
                    info="Your Original Text.",
                    lines=10,
                    value=EXAMPLE_TEXT,
                )
                submit_button = gr.Button("Submit")
                corrected_text = gr.Textbox(
                    label="Corrected Text",
                    info="Our suggested corrected text",
                    lines=10,
                    value=CORRECTED_TEXT,
                    visible=False,
                )
                submit_button.click(submit_text, inputs=[text_input], outputs=original_text)
                clear_button = gr.ClearButton()
                text_input.change(submit_text, text_input, original_text)
            with gr.Tab("Upload"):
                file_input = gr.File(
                    file_types=["text"],
                )
                with gr.Row():
                    upload_button = gr.Button("Upload")
                    clear_button = gr.ClearButton()
                loaded_text = gr.Textbox(
                    label="Your Text",
                    info="The text you uploaded.",
                    lines=10,
                )
                corrected_text = gr.Textbox(
                    label="Corrected Text",
                    info="Our suggested corrected text",
                    lines=10,
                    value=CORRECTED_TEXT,
                    visible=False,
                )
                submit_button = gr.Button("Submit")
                upload_button.click(load_text, inputs=[file_input], outputs=[loaded_text])
                submit_button.click(submit_text, inputs=[loaded_text], outputs=original_text)
            with gr.Tab("Rich Text Editor"):
                gr.HTML(canvas_html, elem_id="canvas_html")
                with gr.Row():
                    download_button = gr.Button("Download")
                    copy_button = gr.Button("Copy")
                    done_button = gr.Button("Done")
        """END SECOND PAGE"""


        """THIRD PAGE"""
        with gr.TabItem("Results", id=2) as third_page:
            original_text.render()
            original_text.change(update_preview, original_text, previewText)
            with gr.Row():
                submit_button = gr.Button("Submit")
                clear_button = gr.ClearButton()

            corrections = gr.HighlightedText(
                label="Corrections",
                combine_adjacent=True,
                show_legend=True,
                color_map={"+": "green", "-": "red"},
            )
            submit_button.click(diff_texts, inputs=[original_text, corrected_text], outputs=corrections)
            with gr.Row():
                submit_paragraph_button = gr.Button("Accept")
                accept_paragraph_button = gr.Button("Ignore")
                done_paragraph_button = gr.Button("Done")
        """END THIRD PAGE"""


        """FOURTH PAGE"""
        with gr.TabItem("Save", id=3) as fourth_page:
            with gr.Accordion(label="Account"):
                preferences = gr.Button(value="Preferences")
                signout = gr.Button(value="Sign Out")
            with gr.Row():
                previewText.render()
                file = gr.File()
            with gr.Row():
                dropdown_type = gr.Dropdown(
                    ["DOCX", "PDF", "TXT"], label="File Type", info="Select your file type."
                )
                download_btn = gr.Button(value="Download", scale=0)
                copy_btn = gr.Button(value="Copy", scale=0)
                done_btn = gr.Button(value="Done", scale=0)
                download_btn.click(fn=download, inputs=[previewText, dropdown_type], outputs=file, api_name="Download")
                copy_btn.click(fn=copy_text, inputs=previewText, api_name="Copy")
        """END FOURTH PAGE"""


incluesive.launch()
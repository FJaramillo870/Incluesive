# Programmers: Anita Martin, Chris Heise, Dion Boyer, and Felix Jaramillo
# Course: BSSD 4350 - Agile Methodologies
# Instructor: Jonathan Lee
# Program: Inclusivity Editor App
# File: app.py

import gradio as gr
from difflib import Differ
from fpdf import *
import pyperclip

canvas_html = """<iframe id='rich-text-root' style='width:100%' height='360px' src='file=RichTextEditor.html' frameborder='0' scrolling='no'></iframe>"""

EXAMPLE_TEXT = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris ultricies elementum nulla, id placerat nunc efficitur non. Nam tempus, nulla ac sodales laoreet, lacus tellus efficitur enim, eget sodales lorem ante ut neque. Mauris quis eros sed velit mollis porta. Aenean libero diam, sagittis sed arcu non, fermentum tincidunt leo. Nulla sed velit tempor, dapibus ex in, rhoncus orci. Praesent sit amet odio sagittis arcu venenatis consequat vitae vitae tortor. Sed et maximus nunc, nec placerat ligula.

Etiam libero nisi, fringilla a imperdiet in, luctus a tortor. Pellentesque quis venenatis velit, quis malesuada nisl. Praesent eu placerat ante. Vivamus quis mi porttitor, faucibus purus non, tempus lacus. Pellentesque et imperdiet dui. Vivamus ut lacus quis lacus maximus iaculis. Vivamus mollis odio orci, ut egestas nisl rhoncus nec. Quisque sit amet lorem viverra, lobortis erat quis, consectetur augue. Etiam blandit tempus purus nec maximus. Vestibulum tempus semper ipsum ac faucibus."""

CORRECTED_TEXT = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris ultricies elementum nulla, id placerat nunc efficitur non. Nulla ac sodales laoreet, lacus tellus efficitur enim, eget sodales lorem ante ut neque. Mauris quis eros sed velit mollis porta. Aenean libero diam, sagittis sed arcu non, fermentum tincidunt leo. Nulla sed velit tempor, dapibus ex in, rhoncus orci. Praesent sit amet odio sagittis arcu venenatis consequat vitae vitae tortor. Sed et maximus nunc, nec placerat ligula.

Etiam libero nisi, fringilla a imperdiet in. Pellentesque quis venenatis velit, elit malesuada nisl. Praesent eu placerat ante. Vivamus quis mi porttitor, faucibus purus non, tempus lacus. Pellentesque et imperdiet dui. Vivamus ut lacus quis lacus maximus iaculis. Vivamus mollis odio orci, ut egestas nisl rhoncus nec. Quisque sit amet lorem viverra, lobortis erat quis, consectetur augue. Etiam blandit tempus purus nec maximus. Vestibulum tempus semper ipsum ac tortor."""

textInput = "There once was a farmer named..."


def download(output):
    """Download text as a PDF."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 10, str(output))
    pdf_file = "history_download.pdf"
    pdf.output(pdf_file)
    return pdf_file


def copyText(output):
    """Copy text to the clipboard."""
    pyperclip.copy(output)
    text = pyperclip.paste()
    return text


def load_text(temp_file):
    """Load text from a temporary file."""
    content = ""
    with open(temp_file.name, "r", encoding="utf-8") as f:
        content = f.read()
    return content


def diff_texts(text1, text2):
    """Find the differences between two texts."""
    d = Differ()
    return [
        (token[2:], token[0] if token[0] != " " else None)
        for token in d.compare(text1, text2)
    ]


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
            with gr.Tabs():
                with gr.TabItem("Type/Paste"):
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
                    corrections = gr.HighlightedText(
                        label="Corrections",
                        combine_adjacent=True,
                        show_legend=True,
                        color_map={"+": "green", "-": "red"},
                    )
                    submit_button.click(diff_texts, inputs=[text_input, corrected_text], outputs=[corrections])
                    clear_button = gr.ClearButton()
                with gr.TabItem("Upload"):
                    file_input = gr.File(
                        file_types=["text"],
                    )
                    with gr.Row():
                        upload_button = gr.Button("Upload")
                        clear_button = gr.ClearButton()
                with gr.TabItem("Rich Text Editor"):
                    gr.HTML(canvas_html, elem_id="canvas_html")
                    with gr.Row():
                        download_button = gr.Button("Download")
                        copy_button = gr.Button("Copy")
                        done_button = gr.Button("Done")
        """END SECOND PAGE"""


        """THIRD PAGE"""
        with gr.TabItem("Results", id=2) as third_page:
            with gr.Tabs():
                with gr.TabItem("Format"):
                    gr.TabItem("Uploaded Text")

                    loaded_text = gr.Textbox(
                        label="Your Text",
                        info="The text you uploaded.",
                        lines=10,
                    )
                    with gr.Row():
                        submit_button = gr.Button("Submit")
                        clear_button = gr.ClearButton()

                    corrections = gr.HighlightedText(
                        label="Corrections",
                        combine_adjacent=True,
                        show_legend=True,
                        color_map={"+": "green", "-": "red"},
                    )

                    # file_input.upload(load_text, inputs=[], outputs=[loaded_text])
                    upload_button.click(load_text, inputs=[file_input], outputs=[loaded_text])
                    submit_button.click(diff_texts, inputs=[loaded_text, corrected_text], outputs=[corrections])

                    with gr.Row():
                        submit_paragraph_button = gr.Button("Accept")
                        accept_paragraph_button = gr.Button("Ignore")
                        done_paragraph_button = gr.Button("Done")
        """END THIRD PAGE"""


        """FOURTH PAGE"""
        with gr.TabItem("Save", id=3) as third_page:
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
        """END FOURTH PAGE"""


incluesive.launch()

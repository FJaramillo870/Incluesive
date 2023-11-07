# Programmers: Anita Martin, Chris Heise, Dion Boyer, and Felix Jaramillo
# Course: BSSD 4350 - Agile Methodologies
# Instructor: Jonathan Lee
# Program: Inclusivity Editor App
# File: app.py

import gradio as gr
from difflib import Differ
from fpdf import *
import pyperclip

from llm.incluesive_llm import IncluesiveLLM


users_text = ""
llms_text = ""
llms_reasoning = ""

canvas_html = """<iframe id='rich-text-root' style='width:100%' height='360px' src='file=RichTextEditor.html' frameborder='0' scrolling='no'></iframe>"""

textInput = ""


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
    users_text = content
    return content


def submit_text(text):
    users_text = text
    llm = IncluesiveLLM(users_text)
    llms_text = llm.get_corrections()
    llms_reasoning = llm.get_reasoning()
    #text_input += users_text   #-wasn't working as of 11/7
    return users_text


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
            with gr.Tab("Type/Paste"):
                text_input = gr.Textbox(
                    label="Your Text",
                    info="Your Original Text.",
                    lines=10,
                )
                submit_button = gr.Button("Submit")
                submit_button.click(submit_text, inputs=[text_input], outputs=[])
                clear_button = gr.ClearButton()
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
                submit_button = gr.Button("Submit")
                upload_button.click(load_text, inputs=[file_input], outputs=[loaded_text])
                submit_button.click(submit_text, inputs=[loaded_text], outputs=[])
            with gr.Tab("Rich Text Editor"):
                gr.HTML(canvas_html, elem_id="canvas_html")
                with gr.Row():
                    download_button = gr.Button("Download")
                    copy_button = gr.Button("Copy")
                    done_button = gr.Button("Done")
        """END SECOND PAGE"""


        """THIRD PAGE"""
        with gr.TabItem("Results", id=2) as third_page:
            original_textbox = gr.Textbox(
                label="Your Text",
                info="Your original text.",
                lines=10,
                value=users_text,
            )
            corrections = gr.HighlightedText(
                label="Corrections",
                combine_adjacent=True,
                show_legend=True,
                color_map={"+": "green", "-": "red"},
                value=diff_texts(users_text, llms_text),
            )
            corrected_textbox = gr.Textbox(
                label="Corrected Text",
                info="Our suggested corrected text",
                lines=10,
                value=llms_text,
            )
            reasoning_textbox = gr.Textbox(
                label="Reasoning",
                info="Our reasoning for the corrections",
                lines=10,
                value=llms_reasoning,
            )
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

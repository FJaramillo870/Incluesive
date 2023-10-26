# Programmers: Anita Martin, Chris Heise, Dion Boyer, and Felix Jaramillo
# Course: BSSD 4350 - Agile Methodologies
# Instructor: Jonathan Lee
# Program: Inclusivity Editor App
# File: second_page.py

import gradio as gr
from difflib import Differ
import gradio as gr

canvas_html = """<iframe id='rich-text-root' style='width:100%' height='360px' src='file=RichTextEditor.html' frameborder='0' scrolling='no'></iframe>"""

EXAMPLE_TEXT = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris ultricies elementum nulla, id placerat nunc efficitur non. Nam tempus, nulla ac sodales laoreet, lacus tellus efficitur enim, eget sodales lorem ante ut neque. Mauris quis eros sed velit mollis porta. Aenean libero diam, sagittis sed arcu non, fermentum tincidunt leo. Nulla sed velit tempor, dapibus ex in, rhoncus orci. Praesent sit amet odio sagittis arcu venenatis consequat vitae vitae tortor. Sed et maximus nunc, nec placerat ligula.

Etiam libero nisi, fringilla a imperdiet in, luctus a tortor. Pellentesque quis venenatis velit, quis malesuada nisl. Praesent eu placerat ante. Vivamus quis mi porttitor, faucibus purus non, tempus lacus. Pellentesque et imperdiet dui. Vivamus ut lacus quis lacus maximus iaculis. Vivamus mollis odio orci, ut egestas nisl rhoncus nec. Quisque sit amet lorem viverra, lobortis erat quis, consectetur augue. Etiam blandit tempus purus nec maximus. Vestibulum tempus semper ipsum ac faucibus."""

CORRECTED_TEXT = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris ultricies elementum nulla, id placerat nunc efficitur non. Nulla ac sodales laoreet, lacus tellus efficitur enim, eget sodales lorem ante ut neque. Mauris quis eros sed velit mollis porta. Aenean libero diam, sagittis sed arcu non, fermentum tincidunt leo. Nulla sed velit tempor, dapibus ex in, rhoncus orci. Praesent sit amet odio sagittis arcu venenatis consequat vitae vitae tortor. Sed et maximus nunc, nec placerat ligula.

Etiam libero nisi, fringilla a imperdiet in. Pellentesque quis venenatis velit, elit malesuada nisl. Praesent eu placerat ante. Vivamus quis mi porttitor, faucibus purus non, tempus lacus. Pellentesque et imperdiet dui. Vivamus ut lacus quis lacus maximus iaculis. Vivamus mollis odio orci, ut egestas nisl rhoncus nec. Quisque sit amet lorem viverra, lobortis erat quis, consectetur augue. Etiam blandit tempus purus nec maximus. Vestibulum tempus semper ipsum ac tortor."""

def load_text(temp_file):
    content = ""
    with open(temp_file.name, "r", encoding="utf-8") as f:
        content = f.read()
    return content

def diff_texts(text1, text2):
    d = Differ()
    return [
        (token[2:], token[0] if token[0] != " " else None)
        for token in d.compare(text1, text2)
    ]

with gr.Blocks(theme=gr.themes.Soft()) as second_page:

    with gr.Tab("Type/Paste"):
        text_input = gr.Textbox(
            label="Your Text",
            info="Your original text.",
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
    with gr.Tab("Upload"):
        file_input = gr.File(
            file_types=["text"],
        )
        upload_button = gr.Button("Upload")
        loaded_text = gr.Textbox(
            label="Your Text",
            info="The text you uploaded.",
            lines=10,
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
        #file_input.upload(load_text, inputs=[], outputs=[loaded_text])
        upload_button.click(load_text, inputs=[file_input], outputs=[loaded_text])
        submit_button.click(diff_texts, inputs=[loaded_text, corrected_text], outputs=[corrections])
    with gr.TabItem("Rich Text Editor"):
        gr.HTML(canvas_html, elem_id="canvas_html")
        with gr.Row():
            accept_paragraph_button = gr.Button("Ignore")
            submit_paragraph_button = gr.Button("Swap")  # gr.Button("Accept")

#second_page.launch()

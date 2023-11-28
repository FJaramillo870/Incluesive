import gradio as gr

with gr.Blocks(theme=gr.themes.Soft()) as first_page:

    with gr.Tab("Directions"):
        gr.Markdown("Welcome to Incluesive an app that will help correcct your writings to be more incluesive of everyone. "
                    "To use Incluesive Pick a writing purpose then enter your text into the text box and submit. After you submit the changes to your text will be shown.")

    with gr.Tab("Writing Preferences"):
        pref = gr.Button(value="Preferences", size='sm')
        choice = gr.Radio(["Professional Correspondence", "Personal Correspondence", "Educational Paper", "Technical Instructions"],label="Writing purpose")
        choice.change(fn=None, inputs=choice, outputs=None)
        #submit_button = gr.Button("Submit")
        #submit_button.click(inputs=radio, outputs=text)

first_page.launch()
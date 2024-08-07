import gradio as gr

app = gr.Interface(lambda x: x, "image", "image")
app.launch(share=True, share_server_address="my-gpt-wrapper.com:7000")
import json
import gradio as gr

from providers.auto_embed1 import AutoEmbed1
from providers.auto_embed2 import AutoEmbed2
from providers.two_embed import TwoEmbed

providers = [
    AutoEmbed1(),
    AutoEmbed2(),
    TwoEmbed(),
]

def get_streams(imdbID, mediaType, title, year, season=None, episode=None):
    video_data_list = []
    for provider in providers:
        video_data = provider.scrape(imdbID, mediaType, title, year, season, episode)
        if video_data:
            video_data_list.extend(video_data)
    return json.dumps(video_data_list, indent=4)

with gr.Blocks() as app:
    gr.Markdown("# Streamora Backend")

    def update_media_type(media_type):
        if media_type == "movie":
            return gr.update(visible=False), gr.update(visible=False)
        else:
            return gr.update(visible=True), gr.update(visible=True)

    
    with gr.Row():
        with gr.Column():
            # imdbID, mediaType, title, year, season, episode
            imdbID = gr.Textbox(label="IMDB ID", placeholder="tt14513804")
            mediaType = gr.Dropdown(label="Media Type", choices=["movie", "tv"], value="movie")
            title = gr.Textbox(label="Title", placeholder="Captain America: Brave New World")
            year = gr.Textbox(label="Year", placeholder="2025")
            with gr.Row():
                season = gr.Textbox(label="Season", placeholder="1", visible=False)
                episode = gr.Textbox(label="Episode", placeholder="1", visible=False)
            mediaType.change(update_media_type, inputs=mediaType, outputs=[season, episode])
        output = gr.TextArea(label="Output", placeholder="Output will be shown here", interactive=False, show_copy_button=True)
    submit = gr.Button(value="Submit")
    submit.click(fn=get_streams, inputs=[imdbID, mediaType, title, year, season, episode], outputs=[output])
    
app.queue(default_concurrency_limit=500).launch(show_api=False, show_error=True)
import gradio as gr

from sentiment_analysis import analyze_sentiment

interface = gr.Interface(
    fn=analyze_sentiment,
    inputs=gr.Textbox(lines=3, placeholder="Enter a sentence for sentiment analysis."),
    outputs=gr.Textbox(label="Sentiment Result"),
    title="AI-Powered Sentiment Analysis",
    description="Enter a sentence, DeepSeek AI will classify its sentiment as Positive, Negative, or Neutral."
)


# Launch the web app
if __name__ == "__main__":
    interface.launch()
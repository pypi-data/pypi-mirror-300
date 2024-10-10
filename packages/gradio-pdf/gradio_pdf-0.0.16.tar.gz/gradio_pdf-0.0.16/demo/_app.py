
import gradio as gr
from gradio_pdf import PDF
# from pdf2image import convert_from_path
# from transformers import pipeline
from pathlib import Path

dir_ = Path(__file__).parent

# p = pipeline(
#     "document-question-answering",
#     model="impira/layoutlm-document-qa",
# )

def qa(question: str, doc: str) -> str:
   return doc


demo = gr.Interface(
    qa,
    [gr.Textbox(label="Question"), PDF(label="Document")],
    PDF(),
    examples=[["What is the total gross worth?", "invoice_2.pdf"],
              ["Whos is being invoiced?", "sample_invoice.pdf"]]
)

if __name__ == "__main__":
    demo.launch()

import pathlib
import textwrap

import google.generativeai as genai

from IPythpipon.display import display
from IPython.display import Markdown

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

model = genai.GenerativeModel('gemini-1.5-flash')
messages = [
  genai.Message(
    role=genai.Message.Role.USER,
    content="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."
  ),
]

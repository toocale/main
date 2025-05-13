#from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain.chains import LLMChain
from langchain_core.messages import HumanMessage
from langchain.schema import HumanMessage
from os import getenv
import base64
from dotenv import load_dotenv
load_dotenv()
import base64
from prompt import prompt

html_string = "html_string"
question = "What is in this image?"
with open("screenshot.png", "rb") as image_file:
    image_bytes = image_file.read()
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")
message_list = prompt(image_bytes,html_string)

model = ChatOpenAI(
  openai_api_key=getenv("OPENROUTER_API_KEY"),
  openai_api_base=getenv("OPENROUTER_BASE_URL"),
  model_name="mistralai/mistral-small-3.1-24b-instruct:free"
)

response = model.invoke([HumanMessage(content=message_list[0]["content"])])
print(response.content)
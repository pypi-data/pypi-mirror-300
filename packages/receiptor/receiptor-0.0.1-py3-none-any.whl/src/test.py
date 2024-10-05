from receiptor import Receiptor
import os
from dotenv import load_dotenv
from llm_parser.gpt_4o_mini_parser.gpt_4o_mini import DocumentStructureExtractor
from models.message import Message
from typing import Optional , List
load_dotenv()


obj = Receiptor()

access_token = "your gmail readonly access token you get from google oauth2 flow"
for data in obj.fetch_receipt_data(access_token=access_token) :    
    if data.attachments:
        print(data.attachments[0].attachment_raw_text)


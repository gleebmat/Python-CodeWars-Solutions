from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter
from dotenv import load_dotenv
from openai import OpenAI
import os

from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
load_dotenv()


client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

MAX_TOKENS = 300

converter = DocumentConverter()
result = converter.convert("https://arxiv.org/pdf/2408.09869")

chunker = HybridChunker(
    tokenizer=tokenizer,
    max_tokens=MAX_TOKENS,
    merge_peers=True,
)
chunk_iter = chunker.chunk(dl_doc=result.document)
chunks = list(chunk_iter)
print(chunks[0].text)

from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter
from dotenv import load_dotenv
from openai import OpenAI
import os
import lancedb
from typing import List

from transformers import AutoTokenizer
from lancedb.embeddings import get_registry

from lancedb.pydantic import LanceModel, Vector

tokenizer = AutoTokenizer.from_pretrained("gpt2")
load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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


# ----------------------


db = lancedb.connect("data/lancedb")

func = get_registry().get("openai").create(name="text-embedding-3-large")


class ChunkMetadata(LanceModel):
    filename: str | None
    page_numbers: List[int] | None
    title: str | None


class Chunks(LanceModel):
    text: str = func.SourceField()
    vector: Vector(func.ndims()) = func.VectorField()

    metadata: ChunkMetadata


table = db.create_table("docling", schema=Chunks, mode="overwrite")


processed_chunks = [
    {
        "text": chunk.text,
        "metadata": {
            "filename": chunk.meta.origin.filename,
            "page_numbers": [
                page_no
                for page_no in sorted(
                    set(
                        prov.page_no
                        for item in chunk.meta.doc_items
                        for prov in item.prov
                    )
                )
            ]
            or None,
            "title": chunk.meta.headings[0] if chunk.meta.headings else None,
        },
    }
    for chunk in chunks
]

# --------------------------------------------------------------
# Add the chunks to the table (automatically embeds the text)
# --------------------------------------------------------------

table.add(processed_chunks)

# --------------------------------------------------------------
# Load the table
# --------------------------------------------------------------

table.to_pandas()
table.count_rows()

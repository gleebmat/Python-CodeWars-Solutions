import lancedb


uri = "data/lancedb"
db = lancedb.connect(uri)


table = db.open_table("docling")


result = table.search(query="pdf", query_type="vector").limit(5)
result.to_pandas()

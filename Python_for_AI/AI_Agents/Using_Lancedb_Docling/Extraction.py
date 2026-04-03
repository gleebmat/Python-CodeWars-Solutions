from docling.document_converter import DocumentConverter
from utils.sitemap import get_sitemap_urls


converter = DocumentConverter()


result = converter.convert("https://genius.com/Sarah-connor-bedingungslos-lyrics")

document = result.document


markdown_output = document.export_to_markdown()
dict_output = document.export_to_dict()

print(markdown_output)


result = converter.convert("https://www.alestorm.net/")

document = result.document
markdown_output = document.export_to_markdown()
print(markdown_output)


sitemap_urls = get_sitemap_urls("https://www.youtube.com/")
conv_result_iter = converter.convert_all(sitemap_urls)

docs = []
for result in conv_result_iter:
    if result.document:
        document = result.document
        docs.append(document)

print(docs[0].export_to_markdown())

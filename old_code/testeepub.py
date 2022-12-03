from ebooklib import epub

book = epub.EpubBook()

c1 = epub.EpubHtml(title="teste", file_name="ahsuiha.xhtml")
c1.content = "<h1>Intro</h1>" "<p>Meu texto aqui dentro</p>"


book.add_item(c1)
epub.write_epub("test.epub", book, {})

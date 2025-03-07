import io
from src.data_processing import (
    process_documents,
    remove_stopwords,
    normalize_text,
    remove_special_characters,
    tokenize_text,
    cached_process_documents
)

#* Stop workds test
def test_remove_stopwords():
    text = "This is a sample sentence with stopwords."
    filtered = remove_stopwords(text)
    for word in ["is", "a", "with"]:
        assert word not in filtered.lower()

#* Normalization test
def test_normalize_text():
    text = "   This    is   A Test.   "
    normalized = normalize_text(text)
    assert normalized == "this is a test."

#* Special characters test
def test_remove_special_characters():
    text = "Hello, world! How are you?"
    cleaned = remove_special_characters(text)
    assert "," not in cleaned and "!" not in cleaned and "?" not in cleaned

#* Tokenization test
def test_tokenize_text():
    text = "Hello world"
    tokens = tokenize_text(text)
    assert tokens == ["Hello", "world"]

#* Process pdf test 
def test_cached_process_documents_pdf():
    # Dummy pdf for test
    from PyPDF2 import PdfWriter
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    pdf_bytes = io.BytesIO()
    writer.write(pdf_bytes)
    pdf_bytes.seek(0)
    
    file_data = [("dummy.pdf", pdf_bytes.read())]
    result = cached_process_documents(file_data)

    assert result.strip() == ""

#* Process csv test
def test_process_documents_csv():
    # Dummy csv file
    csv_content = "col1,col2\nvalue1,value2\n"
    file_obj = io.BytesIO(csv_content.encode("utf-8"))
    class DummyFile:
        def __init__(self, name, data):
            self.name = name
            self.data = data
        def getvalue(self):
            return self.data
    dummy_file = DummyFile("test.csv", file_obj.getvalue())
    result = process_documents([dummy_file])
    assert "value1" in result

#* Process txt test
def test_process_documents_txt():
    # Dummy txt file
    txt_content = "Hello, this is a test."
    file_obj = io.BytesIO(txt_content.encode("utf-8"))
    class DummyFile:
        def __init__(self, name, data):
            self.name = name
            self.data = data
        def getvalue(self):
            return self.data
    dummy_file = DummyFile("test.txt", file_obj.getvalue())
    result = process_documents([dummy_file])
    assert "Hello" in result

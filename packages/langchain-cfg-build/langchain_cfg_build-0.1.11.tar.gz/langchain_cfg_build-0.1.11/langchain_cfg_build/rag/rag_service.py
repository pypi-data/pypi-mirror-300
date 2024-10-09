import os
from typing import Iterator, List

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from langchain_cfg_build.infra import config
from langchain_cfg_build.utils import file_utils


def save_embed_db(db_path: str, doc_iterator: Iterator[List[Document]]) -> str:
    exist_db_folder = os.path.exists(db_path)
    if exist_db_folder:
        file_utils.delete_folder_and_contents(db_path)
    embeddings = OpenAIEmbeddings()
    db = Chroma(persist_directory=db_path, embedding_function=embeddings)
    for doc_list in doc_iterator:
        db.add_documents(doc_list)
    return db_path


def _test_document_generator() -> Iterator[List[Document]]:
    # Imagine this function pulls documents from a database or some other source
    for i in range(20):  # Example of generating 1000 batches
        print(f"Generating {i}")
        yield [Document(
            page_content=f"1This is document {i + 1}. It contains some sample text.",
            metadata={"source_url": f"https://1example.com/document/{i + 1}"}
        ), Document(
            page_content=f"1This is another document {i + 1}. It contains more sample text.",
            metadata={"source_url": f"https://2example.com/document/{i + 1}"}
        )]


def trim_metadata_dict(input_dict: dict) -> dict:
    """
    Recursively trims a dictionary to ensure all values are of type str, int, float, or bool.
    It removes any entries that do not conform to these types.
    """
    return {key: value for key, value in input_dict.items()
            if isinstance(value, (str, int, float, bool))}


if __name__ == '__main__':
    config.load_env()
    _test_it = _test_document_generator()
    print(_test_it)
    wd_path = os.path.dirname(__file__)
    db_path = wd_path + '/_db'
    db_path = save_embed_db(db_path, _test_it)

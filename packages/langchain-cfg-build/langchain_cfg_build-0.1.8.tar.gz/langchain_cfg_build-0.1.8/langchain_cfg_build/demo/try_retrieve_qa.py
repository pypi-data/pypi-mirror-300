from pathlib import Path
from typing import List

from langchain_core.documents import Document

from langchain_cfg_build import app
from langchain_cfg_build.embed_db import embed_db_query_service
from langchain_cfg_build.embed_db.embed_db_loader import EmbedDbLoader
from langchain_cfg_build.llm.enum_llm import EnumLLM
from langchain_cfg_build.rag import rag_service


def generate_document_list() -> List[Document]:
    documents = [
        Document(page_content="Tom is a sunflower", metadata={"booktitle": "Magical summer rainy day"}),
        Document(page_content="BigCoCo is a water monster", metadata={"booktitle": "Magical summer rainy day"})
    ]
    # Add your document generation logic here
    return documents


if __name__ == '__main__':
    env_path = Path(__file__).parent.parent.parent
    app.initialize(str(env_path))
    d_list = generate_document_list()
    db_path = '/tmp/dsa/embed_db/test'
    rag_service.save_embed_db(db_path, iter([d_list]))
    db_loader = EmbedDbLoader(local_path=db_path)
    resp = embed_db_query_service.retrieve_qa(db_loader=db_loader, llm=EnumLLM.gpt_4o,
                                              query='BigCoCo 是什麼?')
    print(resp)

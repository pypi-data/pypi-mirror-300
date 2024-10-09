from langchain.chains.retrieval_qa.base import RetrievalQA

from langchain_cfg_build.embed_db.embed_db_loader import EmbedDbLoader
from langchain_cfg_build.llm.enum_llm import EnumLLM


def retrieve_qa(db_loader: EmbedDbLoader, llm: EnumLLM, query: str):
    db = db_loader.load()
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    chain = RetrievalQA.from_chain_type(llm=llm.value.get_instance(),
                                        chain_type='stuff',
                                        retriever=retriever,
                                        return_source_documents=True,
                                        verbose=True,
                                        input_key="question",
                                        )
    ans = chain.invoke(query)
    return ans

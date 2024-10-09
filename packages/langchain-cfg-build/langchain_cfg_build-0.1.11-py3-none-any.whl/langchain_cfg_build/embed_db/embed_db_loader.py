from dataclasses import dataclass

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


@dataclass
class EmbedDbLoader:
    local_path: str = None
    _db: Chroma = None

    def load(self) -> Chroma:
        if not self._db:
            self._db = self._load()
        return self._db

    def _load(self) -> Chroma:
        embeddings = OpenAIEmbeddings()
        if self.local_path:
            db = Chroma(persist_directory=self.local_path, embedding_function=embeddings)
            return db
        raise NotImplementedError(f"{self.__dict__} EmbedDbLoader load is not implemented!")

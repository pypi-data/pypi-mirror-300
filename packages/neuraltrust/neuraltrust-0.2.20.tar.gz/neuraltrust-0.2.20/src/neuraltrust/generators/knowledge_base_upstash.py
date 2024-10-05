import os
from typing import Dict, Optional, Sequence, List, Union

import logging
import uuid

import numpy as np
import pandas as pd
from sklearn.cluster import HDBSCAN
from upstash_vector import Index
from upstash_vector.types import RangeResult, QueryResult

from .base_knowledge_base import BaseKnowledgeBase
from ..llm.client import ChatMessage, LLMClient, get_judge_client
from ..llm.embeddings import get_default_embedding
from ..llm.embeddings.base import BaseEmbedding
from ..errors.exceptions import ImportError
from ..utils.language_detection import detect_lang
import upstash_vector
import re

try:
    import umap
except ImportError as err:
    raise ImportError(missing_package="umap") from err

logger = logging.getLogger("neuraltrust.generators")

LANGDETECT_MAX_TEXT_LENGTH = 300
LANGDETECT_DOCUMENTS = 10

TOPIC_SUMMARIZATION_PROMPT = """Your task is to define the topic which best represents a set of documents.

Your are given below a list of documents and you must extract the topic best representing ALL contents.
- The topic name should be between 1 to 5 words
- Provide the topic in this language: {language}

Make sure to only return the topic name between quotes, and nothing else.

For example, given these documents:

<documents>
Camembert is a moist, soft, creamy, surface-ripened cow's milk cheese.
----------
Bleu d'Auvergne is a French blue cheese, named for its place of origin in the Auvergne region.
----------
Roquefort is a sheep milk cheese from the south of France.
</documents>

The topic is:
"French Cheese"

Now it's your turn. Here is the list of documents:

<documents>
{topics_elements}
</documents>

The topic is:
"""


class Document:
    """A class to wrap the elements of the knowledge base into a unified format."""

    def __init__(
            self,
            id_vector: str,
            metadata: Dict[str, str],
            vector: List[float]
    ):
        self.content = metadata.get('text', '')
        self.filename = metadata.get('url', '')
        self.id = id_vector
        self.embeddings = vector
        self.reduced_embeddings = None
        self.topic_id = None


class KnowledgeBaseUpstash(BaseKnowledgeBase):
    def __init__(
            self,
            url_upstash: str = None,
            token: str = None,
            seed: int = None,
            llm_client: Optional[LLMClient] = None,
            seed_topic: str = None,
            seed_topic_samples: int = 100
    ) -> None:

        if not url_upstash:
            url_upstash = os.getenv("UPSTASH_URL")

        if not token:
            token = os.getenv("UPSTASH_TOKEN")

        self.index = Index(url=url_upstash, token=token)

        self._embedding_model = get_default_embedding()
        self._documents = self.load_data(seed_topic=seed_topic, seed_topic_samples=seed_topic_samples)
        self._documents = [doc for doc in self._documents if doc.content.strip() != ""]

        self._rng = np.random.default_rng(seed=seed)
        self._llm_client = llm_client or get_judge_client()

        if len(self._documents) > 0:
            self._embeddings_inst = np.array([doc.embeddings for doc in self._documents])
            self._min_topic_size = round(2 + np.log(len(self._documents)))
            self._reduced_embeddings_inst = self.reduce_embeddings()

            # Detect language of the documents
            document_languages = [
                detect_lang(doc.content[:LANGDETECT_MAX_TEXT_LENGTH])
                for doc in self._rng.choice(self._documents, size=min(LANGDETECT_DOCUMENTS, len(self._documents)))
            ]
            languages, occurences = np.unique(
                ["en" if (pd.isna(lang) or lang == "unknown") else lang for lang in document_languages], return_counts=True
            )
            self._language = languages[np.argmax(occurences)]
        else:
            self._embeddings_inst = np.array([])
            self._min_topic_size = 2
            self._reduced_embeddings_inst = np.array([])
            self._language = "en"  # Default to English if no documents

        self._topics_inst = None
        self._index_inst = None
        self._documents_index = {doc.id: doc for doc in self._documents}

    def _get_documents(self, res: Union[RangeResult, QueryResult]) -> List[Document]:
        data = []
        vectors = res.vectors if isinstance(res, RangeResult) else res
        for vector_info in vectors:
            doc = Document(id_vector=vector_info.id,
                           metadata=vector_info.metadata,
                           vector=vector_info.vector)
            data.append(doc)
        return data

    def reduce_embeddings(self):
        if len(self._embeddings_inst) <= 2:
            # If we have 2 or fewer samples, return the original embeddings
            return self._embeddings_inst

        # Adjust n_neighbors to be at most the number of samples minus 1
        n_neighbors = min(15, max(2, len(self._embeddings_inst) - 1))
        
        # Adjust n_components to be at most the number of samples minus 1
        n_components = min(2, len(self._embeddings_inst) - 1)
        
        try:
            reducer = umap.UMAP(
                n_neighbors=n_neighbors,
                min_dist=0.1,
                n_components=n_components,
                random_state=1234,
                n_jobs=1,
                low_memory=True,
                metric='cosine'  # Change to cosine similarity which can handle high-dimensional data better
            )
            reduced_vectors = reducer.fit_transform(self._embeddings_inst)
        except ValueError as e:
            print(f"UMAP reduction failed: {e}")
            print("Falling back to original embeddings")
            reduced_vectors = self._embeddings_inst

        for doc, reduced_vector in zip(self._documents, reduced_vectors):
            doc.reduced_embeddings = reduced_vector

        return reduced_vectors

    def load_data(self, seed_topic: str = None, seed_topic_samples: int = 10) -> List[Document]:
        if seed_topic is None:
            return self._load_all_data()
        else:
            return self._load_data_with_seed_topic(seed_topic, seed_topic_samples)

    def _load_all_data(self) -> List[Document]:
        res = self.index.range(cursor="", limit=5, include_vectors=True, include_metadata=True)
        data = self._get_documents(res)

        while res.next_cursor != "":
            res = self.index.range(cursor=res.next_cursor, limit=10, include_vectors=True, include_metadata=True)
            docs = self._get_documents(res)
            data.extend(docs)

        return data

    def _load_data_with_seed_topic(self, seed_topic: str, seed_topic_samples: int) -> List[Document]:
        seed_embedding = self._embedding_model.embed(seed_topic)
        # Ensure the embedding is a flat list of floats
        seed_embedding_list = seed_embedding.flatten().tolist() if isinstance(seed_embedding, np.ndarray) else seed_embedding
        try:
            res = self.index.query(
                vector=seed_embedding_list,
                top_k=seed_topic_samples,
                include_metadata=True,
                include_vectors=True,
            )
        except upstash_vector.errors.UpstashError as e:
            print(f"Error querying Upstash: {e}")
            print(f"Full embedding: {seed_embedding_list}")
            raise
        
        return self._get_documents(res)

    @property
    def language(self):
        return self._language

    @property
    def _embeddings(self):
        return self._embeddings_inst

    @property
    def _reduced_embeddings(self):
        return self._reduced_embeddings_inst

    @property
    def _dimension(self):
        return self._embeddings[0].shape[0]

    def get_savable_data(self):
        return {
            "columns": self._columns,
            "min_topic_size": self._min_topic_size,
            "topics": {int(k): topic for k, topic in self.topics.items()},
            "documents_topics": [int(doc.topic_id) for doc in self._documents],
        }

    @property
    def _index(self):
        if self._index_inst is None:
            try:
                from faiss import IndexFlatL2
            except ImportError as err:
                raise ImportError(missing_package="faiss") from err

            self._index_inst = IndexFlatL2(self._dimension)
            self._index_inst.add(self._embeddings)
        return self._index_inst

    @property
    def topics(self):
        if self._topics_inst is None:
            self._topics_inst = self._find_topics()
        return self._topics_inst

    def _find_topics(self):
        logger.info("Finding topics in the knowledge base.")
        hdbscan = HDBSCAN(
            min_cluster_size=self._min_topic_size,
            min_samples=3,
            metric="euclidean",
            cluster_selection_epsilon=0.0,
        )
        clustering = hdbscan.fit(self._reduced_embeddings)
        for i, doc in enumerate(self._documents):
            doc.topic_id = clustering.labels_[i]

        topics_ids = set(clustering.labels_)
        topics = {
            idx: self._get_topic_name([self._documents[doc_id] for doc_id in np.nonzero(clustering.labels_ == idx)[0]])
            for idx in topics_ids
            if idx != -1
        }
        topics[-1] = "Others"

        logger.info(f"Found {len(topics)} topics in the knowledge base.")
        return topics

    def _get_topic_name(self, topic_documents):
        logger.debug("Create topic name from topic documents")
        self._rng.shuffle(topic_documents)
        topics_str = "\n\n".join(["----------" + doc.content[:500] for doc in topic_documents[:10]])

        # prevent context window overflow
        topics_str = topics_str[: 3 * 8192]
        prompt = TOPIC_SUMMARIZATION_PROMPT.format(language=self._language, topics_elements=topics_str)

        raw_output = self._llm_client.complete([ChatMessage(role="user", content=prompt)], temperature=0.0).content

        return raw_output.strip().strip('"')

    def get_random_document(self):
        return self._rng.choice(self._documents)

    def get_neighbors(self, seed_document: Document, n_neighbors: int = 4, similarity_threshold: float = 0.2):
        seed_embedding = seed_document.embeddings

        relevant_documents = [
            doc
            for (doc, score) in self.vector_similarity_search_with_score(seed_embedding, k=n_neighbors)
            if score < similarity_threshold
        ]

        return relevant_documents

    def similarity_search_with_score(self, query: str, k: int) -> Sequence:
        query_emb = np.array(self._embedding_model.embed(query), dtype="float32")
        return self.vector_similarity_search_with_score(query_emb, k)

    def vector_similarity_search_with_score(self, query_emb: np.ndarray, k: int) -> Sequence:
        query_emb = np.atleast_2d(query_emb)
        distances, indices = self._index.search(query_emb, k)
        return [(self._documents[i], d) for d, i in zip(distances[0], indices[0])]

    def __len__(self):
        return len(self._documents)

    def __getitem__(self, doc_id: str):
        return self._documents_index[doc_id]

    def reset_index():
        """
        Reset the index.
        """
        url_upstash = os.getenv("UPSTASH_URL")
        token = os.getenv("UPSTASH_TOKEN")

        index = Index(url=url_upstash, token=token)
        index.reset() 

    @classmethod
    def from_pdf(cls, path: str, **kwargs):
        """
        Create a KnowledgeVectorBase from a PDF file or a directory containing PDF files.

        Parameters
        ----------
        path : str
            Path to the PDF file or directory containing PDF files.
        search_service_name : str
            The name of your Azure AI Search service.
        index_name : str
            The name of the index in your Azure AI Search service.
        api_key : str
            The API key for authenticating with Azure AI Search.
        **kwargs :
            Additional keyword arguments to pass to the KnowledgeVectorBase constructor.

        Returns
        -------
        KnowledgeBaseAzure
            An instance of KnowledgeVectorBase with the PDF content embedded and stored in Azure AI Search.
        """
        kb = cls(**kwargs)

        pdf_files = []
        if os.path.isdir(path):
            # If path is a directory, get all PDF files
            for root, _, files in os.walk(path):
                for file in files:
                    if file.lower().endswith('.pdf'):
                        pdf_files.append(os.path.join(root, file))
        elif os.path.isfile(path) and path.lower().endswith('.pdf'):
            # If path is a single PDF file
            pdf_files.append(path)
        else:
            raise ValueError("The provided path is neither a PDF file nor a directory containing PDF files.")

        for pdf_path in pdf_files:
            # Extract text from PDF
            text_chunks = kb._extract_text_from_pdf(pdf_path)

            # Compute embeddings using Azure OpenAI
            embeddings = kb._compute_embeddings(text_chunks)

            # Write to vector store
            ids = [str(uuid.uuid4())[:8] for doc in text_chunks]
            kb._write_to_vector_store(ids, text_chunks, embeddings, pdf_path)

        # Reload documents after writing to the vector store
        kb._documents = kb.load_data()
        
        if not kb._documents:
            print("No documents were loaded. The PDF might be empty or unreadable.")
            return kb

        # Reinitialize embeddings and other properties
        kb._embeddings_inst = np.array([doc.embeddings for doc in kb._documents])
        kb._min_topic_size = max(2, round(2 + np.log(len(kb._documents))))
        
        # Only reduce embeddings if we have more than one document
        if len(kb._documents) > 1:
            kb._reduced_embeddings_inst = kb.reduce_embeddings()
        else:
            kb._reduced_embeddings_inst = kb._embeddings_inst  # Use original embeddings if only one document
        
        # Recalculate language
        document_languages = [
            detect_lang(doc.content[:LANGDETECT_MAX_TEXT_LENGTH])
            for doc in kb._rng.choice(kb._documents, size=min(LANGDETECT_DOCUMENTS, len(kb._documents)))
        ]
        languages, occurences = np.unique(
            ["en" if (pd.isna(lang) or lang == "unknown") else lang for lang in document_languages], return_counts=True
        )
        kb._language = languages[np.argmax(occurences)]

        kb._documents_index = {doc.id: doc for doc in kb._documents}

        return kb

    def _write_to_vector_store(self, ids: List[str], text_chunks: List[str], embeddings: List[List[float]], pdf_path: str):
        """
        Write text chunks and their embeddings to the Azure AI Search index.

        Parameters
        ----------
        text_chunks : List[str]
            List of text chunks to be stored.
        embeddings : List[List[float]]
            List of embeddings corresponding to the text chunks.
        pdf_path : str
            Path to the original PDF file.
        """
        self.index.upsert(
                vectors=[
                (
                    id,
                    embedding,
                    {
                        "text": document,
                        "url": pdf_path
                    }
                )
                for id, embedding, document
                in zip(ids, embeddings, text_chunks)
            ]
        )
        
        print(f"Uploaded {len(text_chunks)} documents to Upstash index.")

    def _extract_text_from_pdf(self, pdf_path: str) -> List[str]:
        try:
            import PyPDF2
        except ImportError:
            raise ImportError("PyPDF2 is required to extract text from PDF files. Install it using 'pip install PyPDF2'.")

        def split_into_sentences(text):
            # Normalize line breaks and spaces
            text = re.sub(r'\s+', ' ', text)
            
            # Split text into lines first
            lines = text.split('\n')
            
            sentences = []
            current_sentence = ""
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Check if the line is a list item or table-like content
                if re.match(r'^[o•]\s|^\w+\s*\.{3,}', line):
                    if current_sentence:
                        sentences.append(current_sentence.strip())
                        current_sentence = ""
                    sentences.append(line)
                else:
                    # Split regular text into sentences
                    line_sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s', line)
                    for s in line_sentences:
                        if s:
                            if current_sentence:
                                current_sentence += " " + s
                            else:
                                current_sentence = s
                            if s[-1] in '.!?':
                                sentences.append(current_sentence.strip())
                                current_sentence = ""
            
            if current_sentence:
                sentences.append(current_sentence.strip())
            
            return [s for s in sentences if s.strip()]

        def create_chunks(sentences, max_chunk_size=1000):
            chunks = []
            current_chunk = []
            current_length = 0

            for sentence in sentences:
                sentence_length = len(sentence)
                if current_length + sentence_length > max_chunk_size and current_chunk:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = []
                    current_length = 0
                
                current_chunk.append(sentence)
                current_length += sentence_length

            if current_chunk:
                chunks.append(" ".join(current_chunk))

            return chunks

        text_chunks = []
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                sentences = split_into_sentences(text)
                chunks = create_chunks(sentences)
                text_chunks.extend(chunks)

        return text_chunks

    def _compute_embeddings(self, text_chunks: List[str]) -> List[List[float]]:
        """
        Compute embeddings for text chunks using Azure OpenAI.

        Parameters
        ----------
        text_chunks : List[str]
            List of text chunks to compute embeddings for.

        Returns
        -------
        List[List[float]]
            A list of embeddings for each text chunk.
        """
        
        embeddings = []
        for chunk in text_chunks:
            seed_embedding = np.array(self._embedding_model.embed(texts=[chunk]))
            seed_embedding_list = seed_embedding.flatten().tolist() if isinstance(seed_embedding, np.ndarray) else seed_embedding
            embeddings.append(seed_embedding_list)

        return embeddings
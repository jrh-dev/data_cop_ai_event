import os

import chromadb
from chromadb.utils import embedding_functions
from google import genai
from tenacity import retry, stop_after_attempt, wait_exponential 


class Interface:
    def __init__(self, name: str):
        self.name = name
        try:
            self.api_key = os.environ["GEMINI_API_KEY"]
        except KeyError:
            raise RuntimeError("GEMINI_API_KEY environment variable not set")
        self.client = genai.Client(api_key=self.api_key)
        self.chroma = chromadb.Client()
        self.embedding = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
            api_key=self.api_key,
            model_name="models/text-embedding-004",
        )
        self.collection = self._create_collection(name)

    def __repr__(self):
        return f"Interface(name={self.name})"

    def _create_collection(self, name: str):
        return self.chroma.create_collection(
            name=name, embedding_function=self.embedding
        )

    def _chunk_text(self, text: str, chunk_size=100, overlap=20):
        # split based on paragraph, double new lines
        return text.split("\n\n")

    def add_policy(self, policy_name: str, policy_text: str):
        chunks = self._chunk_text(policy_text)
        ids = [f"policy_{policy_name}_{i}" for i in range(len(chunks))]
        self.collection.add(documents=chunks, ids=ids)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
    def ask(self, question: str, n_results=20):
        results = self.collection.query(query_texts=[question], n_results=n_results)
        documents = results.get("documents", [[]])[0]
        distances = results.get("distances", [[]])[0]

        documents = [
            document
            for document, distance in zip(documents, distances)
            if distance < 0.3
        ]

        if not documents:
            return "No relevant policy information found."

        context = "\n".join(documents)

        prompt = (
            "You are an HR assistant. Answer using the context below.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}"
        )

        response = self.client.models.generate_content(
            model="models/gemini-2.5-flash", contents=prompt
        )

        return response.text

    def add_policy_from_file(self, path: str):
        with open(path, "r") as f:
            text = f.read()
        name = os.path.splitext(os.path.basename(path))[0]
        self.add_policy(name, text)

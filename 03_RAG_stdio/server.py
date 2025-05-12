from pathlib import Path 

from mcp.server.fastmcp import FastMCP
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI

VECTORDB_PATH = Path(__file__).parents[0] / "my-vectordb"
#-------------------------------------------------------------------
# 0. VectorDB 인스턴스 만들기
#-------------------------------------------------------------------
# 임베딩 모델 불러오기
embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3",  # 또는 multilingual: "BAAI/bge-m3"
    model_kwargs={"device": "mps"},  # or "cuda" / "mps" / "cpu"
    encode_kwargs={"normalize_embeddings": True}
)

# FAISS 로드 및 Retriever 생성
vectordb = FAISS.load_local(VECTORDB_PATH, embedding_model, allow_dangerous_deserialization=True)
retriever = vectordb.as_retriever()

#-------------------------------------------------------------------
# 1. MCP 서버 인스턴스 생성
#-------------------------------------------------------------------
mcp = FastMCP("rag-mcp-server")

#-------------------------------------------------------------------
# 2. 도구 등록
#-------------------------------------------------------------------
@mcp.tool()
def rag_qa(question: str) -> str:
    """벡터 검색 기반 RAG QA. 질문을 입력하면 관련 문서를 검색합니다."""
    results = retriever.invoke(question)

    if not results:
        return "죄송합니다. 관련된 문서를 찾을 수 없습니다."

    return "\n".join([doc.page_content for doc in results])

#-------------------------------------------------------------------
# 3. MCP 서버 실행
#-------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run(transport="stdio")
FROM python:3.11-slim 

# Linux 환경에서 패키지 목록 최신 상태로 업데이트 & curl 설치
# -y: 사용자 입력없이 자동 설치
# curl: uv 패키지 설치를 하기 위함
RUN apt-get update && apt-get install -y curl

# uv 패키지 설치(https://docs.astral.sh/uv/getting-started/installation/)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# uv가 설치된 경로를 PATH에 추가
ENV PATH="/root/.local/bin:${PATH}"

# 작업 디렉토리 생성
WORKDIR /src

# 파일 복사(from A to B)
COPY requirements.txt ./

# 의존성 패키지 설치
RUN uv pip install -r requirements.txt --system

# 파일 복사
COPY 05_MCP_docker ./05_MCP_docker

# 디렉토리 이동
WORKDIR /src/05_MCP_docker

# server.py 실행
CMD ["python", "server.py"]




import asyncio 
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent 
from langchain_openai import ChatOpenAI 

# 환경변수 불러오기
load_dotenv()

#-------------------------------------------------------------------
# 1. LLM 모델 설정
#-------------------------------------------------------------------
model = ChatOpenAI(model="gpt-4o-mini")

#-------------------------------------------------------------------
# 2. MCP 서버 실행을 위한 파라미터 설정
#-------------------------------------------------------------------
server_params = StdioServerParameters(
    command="python",                                                   # 실행 명령어
    args=[                                                              # 내가 만든 서버 파일 위치
        "/Users/narae/wanted/mcp_exercise/03_RAG_stdio/server.py"
    ]
)

#-------------------------------------------------------------------
# 3. 비동기 실행
#-------------------------------------------------------------------
async def main():
    # MCP를 subprocess로 실행(=stdio)
    async with stdio_client(server_params) as (read, write):
        # MCP 세션 시작
        async with ClientSession(read, write) as session:
            # MCP 세션 초기화
            await session.initialize()

            #-------------------------------------------------------
            # 4. MCP 도구 불러오기
            #-------------------------------------------------------
            tools = await load_mcp_tools(session)
            
            #-------------------------------------------------------
            # 5. AI Agent 생성
            #-------------------------------------------------------
            agent = create_react_agent(model, tools)
            
            #-------------------------------------------------------
            # 6. 사용자 질문에 따른 응답 생성
            #-------------------------------------------------------
            while True:
                question = input("\n❓ 질문: ")
                if question.lower() in ["exit", "quit"]:
                    print("👋 종료합니다.")
                    break

                # MCP Tool 호출 (tool name은 서버에서 등록한 'rag_qa')
                agent_response = agent.astream({"messages": question}, stream_mode="values")
                async for s in agent_response:
                    message = s["messages"][-1]
                    if message: 
                        message.pretty_print()
            

#-------------------------------------------------------------------
# 7. Client 실행
#-------------------------------------------------------------------
if __name__ == "__main__":
    result = asyncio.run(main())




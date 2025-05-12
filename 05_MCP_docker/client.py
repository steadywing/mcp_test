import asyncio 
from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.sse import sse_client

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
url = "http://0.0.0.0:8005/sse"

#-------------------------------------------------------------------
# 3. 비동기 실행
#-------------------------------------------------------------------
async def main():
    # MCP를 sse로 실행
    async with sse_client(url) as (read, write):
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
            # 출력방법 1. 한번에 출력하기
            # agent_response = await agent.ainvoke({"messages": "'2 * 5 + 8'을 계산해줘"})
            # print(agent_response)

            # 출력방법 2. 단계별로 출력하기
            agent_response = agent.astream({"messages": "딥씨크 배경이 뭐야"}, stream_mode="values")
            async for s in agent_response:
                message = s["messages"][-1]
                if message: 
                    message.pretty_print()

#-------------------------------------------------------------------
# 7. Client 실행
#-------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())
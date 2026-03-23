import streamlit as st
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

st.title('🚀 AI 자소서 전문 컨설턴트')

# 1. 실제 로직을 수행할 함수 (도구)
def get_resume_template(job, question, experience):
    """자소서의 뼈대를 만드는 함수"""
    return f"직무: {job}\n문항: {question}\n경험 소재: {experience}\n위 내용을 바탕으로 STAR 기법에 맞춰 가독성 있게 작성된 초안입니다."

# 2. 도구(Tools) 정의
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_resume_template",
            "description": "사용자의 직무와 경험을 바탕으로 자소서 초안 텍스트를 생성합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "job": {"type": "string"},
                    "question": {"type": "string"},
                    "experience": {"type": "string"},
                },
                "required": ["job", "question", "experience"],
            },
        },
    }
]

if 'messages' not in st.session_state:
    st.session_state.messages = []

# 사이드바 입력
with st.sidebar:
    st.header("📝 초안 만들기")
    job_i = st.text_input("직무")
    ques_i = st.text_area("문항")
    exp_i = st.text_area("경험")
    if st.button("초안 생성"):
        user_msg = f"{job_i} 직무, '{ques_i}' 문항에 대해 '{exp_i}' 경험으로 자소서 써줘."
        st.session_state.messages.append({"role": "user", "content": user_msg})
        st.rerun()

# 기존 대화 출력
for msg in st.session_state.messages:
    # [수정] tool 호출 메시지는 화면에 표시하지 않도록 필터링
    if msg.get("content"):
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])

# --- AI 응답 처리 로직 ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message('assistant'):
        # 1차 호출: AI가 함수를 쓸지 판단
        response = client.chat.completions.create(
            model="gpt-4o", # gpt-5.2 대신 안정적인 4o 사용 권장
            messages=[{"role": "system", "content": "너는 전문 자소서 컨설턴트야."}] + st.session_state.messages,
            tools=tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # [수정] AI가 함수 호출을 요청한 경우
        if tool_calls:
            # AI의 함수 호출 요청 메시지를 히스토리에 추가 (필수 단계)
            st.session_state.messages.append(response_message)
            
            for tool_call in tool_calls:
                function_args = json.loads(tool_call.function.arguments)
                # 실제 함수 실행 결과 얻기
                function_response = get_resume_template(
                    job=function_args.get("job"),
                    question=function_args.get("question"),
                    experience=function_args.get("experience")
                )
                
                # [중요] 함수의 실행 결과를 AI에게 다시 전달하는 메시지 추가
                st.session_state.messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": "get_resume_template",
                    "content": function_response,
                })
            
            # 2차 호출: 함수 실행 결과를 포함하여 AI에게 최종 답변 요청
            second_response = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.messages
            )
            final_content = second_response.choices[0].message.content
            st.markdown(final_content)
            st.session_state.messages.append({"role": "assistant", "content": final_content})
        
        else:
            # 함수 호출이 필요 없는 일반 대화인 경우
            final_content = response_message.content
            st.markdown(final_content)
            st.session_state.messages.append({"role": "assistant", "content": final_content})

if prompt := st.chat_input('수정사항을 입력하세요.'):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()
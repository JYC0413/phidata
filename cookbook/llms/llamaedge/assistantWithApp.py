import streamlit as st

from phi.assistant import Assistant
from phi.llm.openai.like import OpenAILike
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from phi.tools.youtube_tools import YouTubeTools

st.set_page_config(
    page_title="PhiData for GaiaNet",
    page_icon=":robot:",
)
st.title("PhiData for GaiaNet")


def restart_assistant():
    st.session_state["assistant"] = None
    st.session_state["messages"] = []
    st.rerun()


if "assistant" not in st.session_state:
    st.session_state["assistant"] = None

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi！How are you today？"}]

# 获取输入
base_url = st.sidebar.text_input("Base URL")
model = st.sidebar.text_input("Model")
api_key = st.sidebar.text_input("API Key", type="password")
# 工具选项
tool_options = {
    "None": None,
    "DuckDuckGo": DuckDuckGo(),
    "YFinanceTools": YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True),
    "YouTubeTools": YouTubeTools()
}
selected_tool = st.sidebar.selectbox("Select Tool", list(tool_options.keys()))

# 检查输入变化并重置assistant
if "prev_base_url" not in st.session_state:
    st.session_state["prev_base_url"] = base_url
if "prev_model" not in st.session_state:
    st.session_state["prev_model"] = model
if "prev_api_key" not in st.session_state:
    st.session_state["prev_api_key"] = api_key
if "prev_tool" not in st.session_state:
    st.session_state["prev_tool"] = selected_tool

if (base_url != st.session_state["prev_base_url"] or
    model != st.session_state["prev_model"] or
    api_key != st.session_state["prev_api_key"]):
    if selected_tool == "None":
        st.session_state["assistant"] = Assistant(
            llm=OpenAILike(
                model=model,
                api_key=api_key,
                base_url=base_url
            )
        )
    else:
        st.session_state["assistant"] = Assistant(
            llm=OpenAILike(
                model=model,
                api_key=api_key,
                base_url=base_url
            ),
            tools=[tool_options[selected_tool]],
            show_tool_calls=True
        )
    assistant_chat_history = st.session_state["assistant"].memory.get_chat_history()
    if len(assistant_chat_history) > 0:
        st.session_state["messages"] = assistant_chat_history
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi！How are you today？"}]

    st.session_state["prev_base_url"] = base_url
    st.session_state["prev_model"] = model
    st.session_state["prev_api_key"] = api_key

assistant = st.session_state["assistant"]

# 配合获取memory显示历史记录
for message in st.session_state["messages"]:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 聊天框
if prompt := st.chat_input("enter your question"):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.experimental_rerun()

# 处理用户输入
if len(st.session_state["messages"]) > 0:
    last_message = st.session_state["messages"][-1]
    if last_message.get("role") == "user":
        question = last_message["content"]
        with st.chat_message("assistant"):
            response = ""
            resp_container = st.empty()
            for delta in assistant.run(question):
                response += delta  # type: ignore
                resp_container.markdown(response)
            st.session_state["messages"].append({"role": "assistant", "content": response})

# 重启助手按钮
if st.sidebar.button("rebot assistant"):
    restart_assistant()

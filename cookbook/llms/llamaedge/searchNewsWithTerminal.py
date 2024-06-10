from phi.assistant import Assistant
from phi.llm.openai.like import OpenAILike
from phi.tools.duckduckgo import DuckDuckGo

assistant = Assistant(
    llm=OpenAILike(
        model="XXX",
        api_key="",
        base_url="https://XXX/v1"
    ),
    tools=[DuckDuckGo()],
    show_tool_calls=True
)
assistant.print_response('what is the weather today in Paris?', markdown=True)

from phi.assistant import Assistant
from phi.llm.openai.like import OpenAILike
from phi.tools.youtube_tools import YouTubeTools

assistant = Assistant(
    llm=OpenAILike(
        model="XXX",
        api_key="",
        base_url="https://XXX/v1"
    ),
    tools=[YouTubeTools()],
    description="You are a YouTube assistant. Obtain the captions of a YouTube video and answer questions.",
    show_tool_calls=True
)
assistant.print_response('Summarize this video https://www.youtube.com/watch?v=XkZOiD3napU', markdown=True)

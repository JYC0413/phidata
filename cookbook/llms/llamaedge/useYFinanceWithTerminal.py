from phi.assistant import Assistant
from phi.llm.openai.like import OpenAILike
from phi.tools.yfinance import YFinanceTools

assistant = Assistant(
    llm=OpenAILike(
        model="XXX",
        api_key="",
        base_url="https://XXX/v1"
    ),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
    show_tool_calls=True
)
assistant.print_response('What is the most advanced LLM currently? Save the answer to a file.', markdown=True)

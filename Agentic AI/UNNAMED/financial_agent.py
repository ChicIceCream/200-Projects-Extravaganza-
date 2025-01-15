from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo

from dotenv import load_dotenv
import os
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

model = "llama-3.1-8b-instant"

# Create a web search agent
web_search_agent = Agent(
    name = "Web Search Agent",
    role = "Search the web for any information I want",
    model = Groq(id=model),
    # llm=Groq(id="llama-3.1-70b-versatile", api_key=GROQ_API_KEY),
    tools = [DuckDuckGo()],
    # instructions = ["Always include your sources"],
    markdown = True,
)

# Create a financial agent
financial_agent = Agent(
    name = "Financial Agent",
    model = Groq(id = model),
    # llm=Groq(id="llama-3.1-70b-versatile", api_key=GROQ_API_KEY),
    tools = [
        YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, company_news=True)
        ],
    instructions = ["Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)

# multi_agent = Agent(
#     team = [web_search_agent, financial_agent],
#     # model = Groq(id="llama-3.1-70b-versatile"),
#     llm=Groq(id="llama-3.1-70b-versatile", api_key=GROQ_API_KEY),
#     instructions=["Always include sources", "Display your data in tables"],
#     show_tool_calls=True,
#     markdown=True,
# )

multi_ai_agent=Agent(
    team=[web_search_agent, financial_agent],
    model=Groq(id=model),
    instructions=["Always include sources", "Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)
multi_ai_agent.print_response("Summarize analyst recommendations + share latest news for NVDA", stream=True)

# multi_agent.print_response("Summarize analyst recommendations and share the latest news for NVIDIA", stream=True, )
# print(GROQ_API_KEY)  # Should display your API key


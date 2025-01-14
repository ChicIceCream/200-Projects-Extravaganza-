from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo

# Create a web search agent
web_search_agent = Agent(
    name = "Web Search Agent",
    role = "Search the web for any information I want",
    model = Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools = [DuckDuckGo()],
    instructions = ["Always include your sources"],
    markdown = True,
)

# Create a financial agent
financial_agent = Agent(
    name = "Financial Agent",
    model = Groq(id = "llama3-groq-70b-8192-tool-use-preview"),
    tools = [
        YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, company_news=True)
        ],
    instructions = ["Use tables to display your data"],
    show_tool_calls=True,
    markdown=True,
)

multi_agent = Agent(
    team = [web_search_agent, financial_agent],
    instructions=["Always include sources", "Display your data in tables"],
    show_tool_calls=True,
    markdown=True,
)

multi_agent.print_response("Summarize analyst recommendations and share the latest news for NVIDIA", stream=True)

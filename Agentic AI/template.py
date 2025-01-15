from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo

from dotenv import load_dotenv
import os
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

model = "llama-3.1-8b-instant"

web_search_agent = Agent(
    name = "Web Search Agent",
    role = "Search the web for any information I want",
    model = Groq(id=model),
    # llm=Groq(id="llama-3.1-70b-versatile", api_key=GROQ_API_KEY),
    tools = [DuckDuckGo()],
    # instructions = ["Always include your sources"],
    markdown = True,
)
# Get the response in a variable
# run: RunResponse = agent.run("Share a 2 sentence horror story.")
# print(run.content)

# Print the response in the terminal
web_search_agent.print_response("What paper is the most influential paper in the AI space till today?")


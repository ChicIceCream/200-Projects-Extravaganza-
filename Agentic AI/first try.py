from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel

agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=HfApiModel("meta-llama/Llama-3.2-3B-Instruct"))

agent.run("How many seconds would it take for a leopard at full speed to run through Taj Mahal")

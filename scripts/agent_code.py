# scripts/agent_code.py
# This file defines the agent logic. MLflow will execute this code to load the model.

import mlflow
from databricks_langchain import ChatDatabricks, UCFunctionToolkit
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor

# 1. Setup Tools
tool_names = [
    "demo.tools.get_weather",
    "demo.tools.get_post",
    "demo.tools.get_current_datetime"
]
toolkit = UCFunctionToolkit(function_names=tool_names)
tools = toolkit.tools

# 2. Setup LLM
llm = ChatDatabricks(model="databricks-meta-llama-3-3-70b-instruct")

# 3. Setup Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant with access to real-time tools. Use them when needed."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 4. Create Agent
agent = create_tool_calling_agent(llm, tools, prompt)

# 5. Create AgentExecutor
model = AgentExecutor(agent=agent, tools=tools, verbose=False)

# 6. CRITICAL: Tell MLflow this is the model
mlflow.models.set_model(model)
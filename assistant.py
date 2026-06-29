from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
import os
from google.generativeai import configure, GenerativeModel

# 1. SETUP
os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY_HERE"
configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# 2. TOOLS
from stock_tool import check_stock_price
from reading_tool import search_my_papers

def get_google_search_results(query):
    """Uses Google Search grounding to fetch real-time info."""
    model = GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        query,
        tools=[{"google_search_retrieval": {}}]
    )
    return response.text

tools = [
    Tool(
        name="Stock_Sensor",
        func=lambda ticker: check_stock_price("^NSEI") if "nifty" in ticker.lower() else check_stock_price(ticker),
        description="Check stock price. Use '^NSEI' if the user asks for Nifty."
    ),
    Tool(
        name="Research_Cabinet",
        func=search_my_papers,
        description="Search local research papers."
    ),
    Tool(
        name="Web_Explorer",
        func=get_google_search_results,
        description="Search Google for real-time information."
    )
]

# 3. AGENT
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are Boss AI. Use Stock_Sensor for stocks (use ^NSEI for Nifty), Research_Cabinet for papers, and Web_Explorer for anything else."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)

def boss_ai(user_prompt):
    try:
        result = agent_executor.invoke({"input": user_prompt})
        return result["output"]
    except Exception as e:
        return f"I hit a snag: {e}"
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents.output_parsers import ReActSingleInputOutputParser 
 
from tools.discovery_layer import discovery_tools
from tools.intelligence_layer import intelligence_tools
from tools.generation_layer import get_email_tools
from llm.ollama_llm import get_llm

class SmartOutreachAgent:
    def __init__(self, model_name="llama3.1:8b"):
        self.llm = get_llm(model_name)
        email_tools = get_email_tools(self.llm)

        self.tools = discovery_tools + intelligence_tools + email_tools
        self.memory = ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True)
        self.agent_executor = self._create_agent()

    def _create_agent(self):
        tool_names = ", ".join([tool.name for tool in self.tools])
        tool_desc = "\n".join([f"- {tool.name}: {tool.description}" for tool in self.tools])

        prompt = PromptTemplate(
            template='''
            You are SmartOutreach, an expert assistant for B2B cold outreach.
            Your job is to help users:
            1. Find relevant companies
            2. Gather intelligence (news, funding, tech stack, jobs, etc.)
            3. Generate a personalized email using that information

            You can use the following tools:
            {tools}

            Available tool names: {tool_names}

            You must ALWAYS follow this format when responding:

            Thought: <your reasoning>
            Action: <tool_name>
            Action Input: <string or JSON input>

            When you're done, just respond with:
            Final Answer: <your conclusion>

            Previous chat:
            {chat_history}

            User task:
            {input}

            Begin!
            {agent_scratchpad}
            ''',
            input_variables=["input", "chat_history", "agent_scratchpad", "tools", "tool_names"]
                )

        return AgentExecutor.from_agent_and_tools(
            agent=create_react_agent(
                llm=self.llm,
                tools=self.tools,
                prompt=prompt,
                output_parser=ReActSingleInputOutputParser()
            ),
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=8,
            early_stopping_method="generate"
        )

    def invoke(self, query: str) -> str:
        return self.agent_executor.invoke({"input": query})

    def run_tool(self, tool_name: str, input_str: str) -> str:
        for tool in self.tools:
            if tool.name == tool_name:
                return tool.run(input_str)
        return f"Tool '{tool_name}' not found."

    def list_tools(self):
        return [(t.name, t.description) for t in self.tools]

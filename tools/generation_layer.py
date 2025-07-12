from langchain.tools import Tool
from langchain.llms import Ollama

def get_email_tools(llm: Ollama):
    def research_summary(inputs: str) -> str:
        prompt = f"""
        Given the following structured data from Discovery + Intelligence:
        {inputs}

        Create a concise 1-page research summary on this company with:
        - Overview
        - Tech Stack
        - Recent News Highlights

        Return in markdown with headers for each.
        """
        return llm(prompt)

    def generate_email(context: str) -> str:
        prompt = f"""
        You are an expert in personalized cold outreach.
        Write a cold email based on:
        {context}

        Structure:
        - Subject: compelling, short (max 8 words)
        - Greeting
        - Personalization: based on the company and refer to the specific business context 
        - Value Proposition (tied to service)
        - CTA (meeting / reply / resource link)
        - Length: Max 150 words
        - SignOff with Warm Regards

        Return JSON with keys: subject, body, personalization_notes
        """
        return llm(prompt)

    tools = [
        Tool(
            name="company_research_summary",
            func=research_summary,
            description="Summarize company research from structured data into a 1-page markdown brief.",
        ),
        Tool(
            name="email_generator",
            func=generate_email,
            description="Generate a cold outreach email from research summary and business context.",
        )
    ]
    return tools

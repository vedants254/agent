# gmail_toolkit.py

from langchain.agents import Tool
from langchain_google_community import GmailToolkit
from langchain_google_community.gmail.create_draft import GmailCreateDraft

'''
from langchain_google_community.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)

# Can review scopes here https://developers.google.com/gmail/api/auth/scopes
# For instance, readonly scope is 'https://www.googleapis.com/auth/gmail.readonly'
credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="credentials.json",
)
api_resource = build_resource_service(credentials=credentials)
toolkit = GmailToolkit(api_resource=api_resource)
'''
toolkit = GmailToolkit()#this automatically generates a token file for OAuth and reads the credentail.json. 

tools = toolkit.get_tools()

gmail_create_draft_tool = GmailCreateDraft(api_resource=toolkit.api_resource)
gmail_tools = [
    Tool(
        name="save_gmail_draft",
        func=gmail_create_draft_tool.run,
        description="Save an email draft to Gmail. Input should be a JSON string with 'to', 'subject', and 'body'."
    )
]


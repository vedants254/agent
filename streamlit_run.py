# streamlit_app.py
import streamlit as st
import os
from agent_main import SmartOutreachAgent
#from tools.gmail_toolkit import gmail_tools

# Set LangSmith tracing (if used)
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = os.getenv('LANGSMITH_API_KEY')

st.set_page_config(page_title="Smart Outreach Assistant", layout="wide")
st.title("Smart Outreach Assistant")
st.markdown("Generate research-driven cold emails by discovering and enriching companies based on your product or service.")

# Initialize agent
@st.cache_resource
def load_agent():
    return SmartOutreachAgent(model_name="llama3.1:8b")

agent = load_agent()

# Load the Gmail draft tool
#save_gmail_tool = [tool for tool in gmail_tools if tool.name == "save_gmail_draft"][0]

# Input form
with st.form("outreach_form"):
    user_query = st.text_input("Who do you want to target?", placeholder="e.g. logistics startups in Dubai")
    user_service = st.text_area("What are you offering them?", placeholder="e.g. AI-powered optimization tool to reduce costs by 30%")
    submitted = st.form_submit_button("🚀 Run Outreach")

result = ""
if submitted and user_query and user_service:
    with st.spinner("Thinking, researching and writing..."):
        query = f"Find companies like: {user_query}. Then write an outreach email for this service: {user_service}"
        result = agent.invoke(query)

    st.subheader("Agent Response")
    st.text_area("Generated Email & Insights", result, height=400)
    st.download_button("Download Result", result, file_name="smart_outreach.txt", mime="text/plain")
'''if result:
    with st.expander("Save Email to Gmail Draft"):
        to = st.text_input("Recipient Email", value="", key="to_email")
        subject = st.text_input("Email Subject", value="Following up", key="email_subject")

        if st.button("Save to Gmail"):
            if to and subject and result:
                # Prepare input JSON
                draft_input = {
                    "to": to,
                    "subject": subject,
                    "body": result
                }
                try:
                    draft_url = save_gmail_tool.run(draft_input)
                    st.success("Draft saved!")
                    if draft_url:
                        st.markdown(f"[📬 Open Gmail Draft]({draft_url})", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Failed to save draft: {e}")
            else:
                st.warning("Please fill in recipient, subject, and generate email first.")
'''
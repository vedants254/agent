
# Smart Outreach Assistant

**Smart Outreach Assistant** is a research-driven tool designed to help you craft highly personalized cold outreach emails. It automates the discovery of relevant companies, enriches company profiles using real-time intelligence, and generates effective email drafts — all within a clean Streamlit interface.

## What It Does

- Discovers companies matching your product/service offering  
- Enriches companies with insights like recent news and tech stacks  
- Writes personalized outreach emails based on real-time intelligence  
- (Optional) Saves emails directly as Gmail drafts  

This agent leverages LangChain, LLaMA 3.1 via Ollama, and multiple specialized tools under the hood to streamline your B2B outreach workflow.

## How It Works

1. Discovery Layer  
   - Uses Apollo API to search companies by location and keywords  
   - Falls back to DuckDuckGo if Apollo data is unavailable  

2. Intelligence Layer  
   - Scrapes the latest news from the web  
   - Enriches company profiles with domain-level insights  

3. Generation Layer  
   - Creates a structured research brief  
   - Generates an email with subject, body, and personalization highlights  

4. Gmail Integration (optional)  
   - Saves the generated email as a draft in your Gmail inbox  
   - OAuth handled via langchain_google_community toolkit  

## Important Note on Data Quality

While the current company discovery uses Apollo API and DuckDuckGo, Google Places API would offer significantly higher precision and data relevance, especially for local or niche business discovery.

However, since Google Places API is a paid service, I wasn't able to completely explore its working. Google Places API would give much better results from small to large businesses. 

Also, Instead of local run using Ollama, to make inference faster, Groq API coudl be used with a better,faster model.

## Run It Locally

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/smart-outreach-assistant.git
cd smart-outreach-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Set up .env file

Create a `.env` file with the following (Apollo and LangSmith keys):

```env
APOLLO_API_KEY=your_apollo_api_key
LANGSMITH_API_KEY=your_langsmith_key  # optional for LangChain tracing
```

### 4. Run the app

```bash
streamlit run streamlit_run.py
```

## Features at a Glance

| Layer         | Functionality                                      |
|---------------|----------------------------------------------------|
| Discovery     | Apollo API and DuckDuckGo for company search       |
| Intelligence  | News scraping and company profile enrichment       |
| Generation    | Research summary and cold email generation         |
| Gmail Toolkit | Optional Gmail draft saving (OAuth2 required)      |
| LLM           | LLaMA 3.1 (via Ollama) for email and summary writing |

## Future Enhancements

- Integrate Google Places API for better discovery  
- Add support for multiple target personas  
- Expand to multilingual outreach capability  

## Contributing

Pull requests are welcome.  
 
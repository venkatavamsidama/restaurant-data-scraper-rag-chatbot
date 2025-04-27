# 🍽️ Restaurant Data Scraper & RAG Chatbot

A full pipeline to **scrape restaurant websites**, **organize** the data using **LLMs or rule-based parsing**, **index** it into a **FAISS vector database**, and finally **chat** with the structured information using a **Retrieval-Augmented Generation (RAG) Chatbot**.

---

## ✨ Features
- **IP Masking**: Scraper rotates between public proxies to mask IPs automatically.
- **Multithreading**: Scraper uses concurrent threads to fetch multiple pages faster.
- **Caching**: Disk-based caching avoids redundant page fetches and re-parsing.
- **LLM Integration**: Organizes raw HTML into structured data using Gemini or fallback extraction.
- **Vector Search**: FAISS-based similarity search for retrieving relevant menu items.
- **Chatbot Interface**: Ask questions and get intelligent answers based on indexed menu data.

---

## 📂 Project Structure

```bash
restaurant-data-scraper-rag-chatbot/
├── config/              # Environment configs
├── data/                # Raw and structured scraped data
├── scraper/             # Scraper scripts
├── pipeline/            # Organizer, extractor, preprocessor, indexer
├── rag_chatbot/         # Retriever, Generator, Chatbot Interface
├── ui/                  # Streamlit frontend
├── requirements.txt
├── README.md
├── .gitignore
└── .env.example
```

---

## ⚙️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/restaurant-data-scraper-rag-chatbot.git
   cd restaurant-data-scraper-rag-chatbot
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Fill your Gemini API Key in the .env file
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 How to Run

The project runs in **4 simple stages**:

### 1. Scrape raw restaurant web pages
```bash
python -m scraper.raw_scraper
```
- Scrapes all URLs listed in `config/urls.txt`
- Saves raw HTML into `data/raw/`

---

### 2. Organize & Extract structured data
```bash
python -m pipeline.organizer
```
- Calls Gemini LLM (or fallback HTML parser) to extract fields like **restaurant name, menu, contact, hours**.
- Stores JSONs in `data/structured/`

---

### 3. Build the FAISS knowledge index
```bash
python -m pipeline.indexer
```
- Preprocesses menu items.
- Encodes using Sentence Transformers.
- Builds a FAISS index in `knowledge_base/`

---

### 4. Launch the Chatbot UI
```bash
streamlit run ui/app.py
```
- Visit the Streamlit app at `http://localhost:8501`
- Start chatting about restaurant menus, prices, features, etc!

---

## 🧪 Example Usage

- **Query:** "Show me pasta dishes under $20."
- **Query:** "Which restaurants are open after 10PM?"
- **Query:** "Find me vegan options."

The chatbot retrieves the most relevant menu items and answers naturally!

---

## 📄 Environment Variables (`.env`)

| Variable        | Description                                 |
|-----------------|---------------------------------------------|
| `PROXY_LIST`    | Comma-separated proxy servers (optional)    |
| `LLM_PROVIDER`  | LLM provider (currently expects `gemini`)   |
| `GEMINI_API_KEY`| Your Gemini API Key                         |
| `LLM_MODEL`     | Model name (default: `gemini-pro`)          |

---

## 🛠️ Tech Stack

- **Selenium** – Web scraping
- **BeautifulSoup** – Fallback extraction
- **DiskCache** – Scraper caching
- **Sentence-Transformers** – Embedding generation
- **FAISS** – Vector similarity search
- **Transformers** – RAG Token model
- **Streamlit** – Chat UI

---

## 📋 Notes

- This project supports **Gemini LLM integration** for extraction, but has a **rule-based fallback** if API fails.
- You can **customize extraction fields** or **extend chatbot abilities** by modifying `pipeline/extractor.py` and `rag_chatbot/`.

---

## 📈 Future Improvements (Optional)

- Add multi-turn conversational memory
- Implement better UI (chat history, markdown rendering)
- Use OpenAI / Claude / Mixtral as alternative LLMs
- Add automatic website crawling (site maps)

---

## 🧹 Clean Commands (Optional)

- Clear all data:
  ```bash
  rm -rf data/raw/* data/structured/* knowledge_base/*
  ```

---

# 🙌 Happy Building!

If you find this project useful, feel free to ⭐ star it or fork to customize for your use case!


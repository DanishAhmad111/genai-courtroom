# 🧑‍⚖️ GenAI Courtroom – Legal Trial Simulator

An AI-powered courtroom simulation system that generates realistic legal proceedings using advanced RAG (Retrieval Augmented Generation), fine-tuned LLMs, and legal document analysis.

## ✨ Features

- **🎭 Automated Trial Simulation**: Generate prosecution arguments, defense responses, and judge verdicts
- **📚 RAG-Powered Legal Research**: FAISS-based vector search through legal documents (Indian Constitution)
- **🤖 Fine-Tuned Judge Model**: Custom LoRA-adapted LLM trained on Indian legal cases
- **📄 PDF Document Processing**: Upload and analyze legal documents in real-time
- **⚡ Hybrid AI System**: Combines fine-tuned models with Groq API for optimal results
- **🎨 Interactive UI**: Clean Streamlit interface for easy case submission

## 🏗️ Architecture

```
┌─────────────────┐
│  Streamlit UI   │
└────────┬────────┘
         │
    ┌────▼─────────────────────────────┐
    │   Courtroom Orchestration        │
    │  (backend/courtroom_logic.py)    │
    └────┬─────────────────────────┬───┘
         │                         │
    ┌────▼────────┐          ┌─────▼──────────┐
    │  RAG System │          │   LLM Calls    │
    │   (FAISS)   │          │  (Groq API +   │
    │             │          │  Fine-tuned)   │
    └─────────────┘          └────────────────┘
```

### Components

1. **Frontend** ([frontend/App.py](frontend/App.py))
   - Streamlit-based user interface
   - PDF upload and processing
   - Case submission and results display

2. **Backend** ([backend/courtroom_logic.py](backend/courtroom_logic.py))
   - Orchestrates the trial simulation
   - Manages LLM calls (Groq API)
   - Handles fine-tuned model inference
   - Implements hybrid judge logic

3. **RAG System** ([rag/rag_utils.py](rag/rag_utils.py))
   - PDF text extraction (PyMuPDF)
   - Text chunking and embedding (BGE-small)
   - FAISS vector indexing and search

4. **Fine-Tuning** ([fine_tune_judge.py](fine_tune_judge.py))
   - LoRA-based fine-tuning script
   - Trained on Indian legal dataset
   - PEFT (Parameter-Efficient Fine-Tuning)

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Groq API Key ([Get one here](https://console.groq.com))
- (Optional) Hugging Face account for model hosting

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd genai-courtroom
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Groq API key:
   ```
   CHATGROQ_API_KEY=your_groq_api_key_here
   USE_LOCAL_JUDGE=false  # Set to true if using fine-tuned model locally
   ```

5. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

6. **Access the app**
   - Open [http://localhost:8501](http://localhost:8501)

## 🎯 Usage

### Basic Trial Simulation

1. **Enter a case description**
   ```
   A shopkeeper is accused of selling expired food products that 
   caused food poisoning to 10 customers. The defense claims the 
   products were within the expiry date and properly stored.
   ```

2. **Upload legal documents** (optional)
   - Upload relevant PDFs (laws, precedents, constitution)
   - System will automatically index and use for RAG

3. **Click "Simulate Trial"**
   - Wait for AI to generate:
     - 👨‍💼 Prosecution argument
     - 👨‍⚖️ Defense response
     - 📜 Judge verdict

### Using the Fine-Tuned Model

To use the fine-tuned judge model locally:

1. Ensure you have the `judge-lora` directory
2. Set in `.env`:
   ```
   USE_LOCAL_JUDGE=true
   JUDGE_LORA_PATH=judge-lora
   ```

## 📦 Deployment

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for comprehensive deployment instructions covering:

- 🌐 **Streamlit Cloud** (Recommended)
- 🐳 **Render** (Docker)
- 🚂 **Railway**
- 🤗 **Hugging Face Spaces**
- 💻 **Local Docker**

### Quick Deploy to Streamlit Cloud

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Set secrets (API keys)
5. Deploy!

## 🧪 Fine-Tuning Your Own Model

### Prepare Dataset

```bash
python prepare_dataset.py
```

This creates `judge_dataset.jsonl` from legal cases.

### Train the Model

```bash
python fine_tune_judge.py \
  --data judge_dataset.jsonl \
  --base distilgpt2 \
  --output judge-lora \
  --epochs 3
```

### Upload to Hugging Face

```bash
python scripts/upload_model_to_hf.py \
  --repo_name YOUR_USERNAME/genai-courtroom-judge
```

## 🔧 Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `CHATGROQ_API_KEY` | ✅ Yes | - | Groq API key for LLM calls |
| `USE_LOCAL_JUDGE` | ❌ No | `false` | Use fine-tuned model |
| `JUDGE_LORA_PATH` | ❌ No | `judge-lora` | Path or HF model ID |
| `GROQ_MODEL` | ❌ No | `llama-3.3-70b-versatile` | Groq model name |
| `HF_TOKEN` | ❌ No | - | HuggingFace token (for private models) |

## 📊 Project Structure

```
genai-courtroom/
├── backend/
│   ├── app.py                    # Backend API (empty, for future use)
│   └── courtroom_logic.py        # Core trial orchestration
├── frontend/
│   └── App.py                    # Streamlit UI
├── rag/
│   ├── constitution.pdf          # Indian Constitution
│   ├── rag_utils.py              # RAG utilities
│   └── embeddings/               # FAISS index storage
├── prompts/
│   ├── prosecution.txt           # Prosecution prompt template
│   ├── defense.txt               # Defense prompt template
│   └── judge.txt                 # Judge prompt template
├── scripts/
│   └── upload_model_to_hf.py     # Model upload utility
├── judge-lora/                   # Fine-tuned LoRA adapter
├── .streamlit/
│   └── config.toml               # Streamlit configuration
├── Dockerfile                    # Docker configuration
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
├── streamlit_app.py              # Main entry point
├── fine_tune_judge.py            # Fine-tuning script
├── prepare_dataset.py            # Dataset preparation
├── build_constitution_index.py  # Pre-build FAISS index
└── DEPLOYMENT.md                 # Deployment guide
```

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM API**: Groq (Llama 3.3 70B)
- **Fine-Tuning**: PEFT (LoRA), Hugging Face Transformers
- **RAG**: FAISS, Sentence Transformers (BGE-small)
- **PDF Processing**: PyMuPDF
- **Deployment**: Docker, Streamlit Cloud, Render, Railway

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Add more legal document sources
- [ ] Support multiple languages
- [ ] Improve fine-tuning dataset
- [ ] Add case history tracking
- [ ] Implement user authentication
- [ ] Add export to PDF functionality

## 📝 License

[Add your license here]

## 🙏 Acknowledgments

- Indian Constitution text from [india.gov.in](https://www.india.gov.in)
- Groq for fast LLM inference
- Hugging Face for model hosting and transformers
- Streamlit for the amazing framework

## 📧 Contact

[Add your contact information]

---

**Built with ❤️ for legal tech innovation**

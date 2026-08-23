# 🔬 AI Research Scientist

A Streamlit-based multi-agent scientific research platform built with the **OpenAI Agents SDK**.  
The system automates major stages of a research workflow—from literature discovery and research-gap analysis to experiment planning, data interpretation, citation management, and final scientific report generation.

## ✨ Key Features

- 🤖 **6 specialized AI agents**
- 🔁 **Agent coordination and SDK handoffs**
- 📚 Academic literature search using arXiv, PubMed, OpenAlex, and Crossref
- 🌐 Supplementary public web search
- 📄 Optional research-paper PDF upload and text extraction
- 🧠 Short-term session memory for research context
- 👤 Human approval gate before final report generation
- 📦 Structured final output using Pydantic
- 📝 Runtime error logging
- 📥 Downloadable Markdown and PDF research reports
- 🛡️ Research-integrity instructions to avoid fabricated papers, citations, data, or experimental results

---

## 🎯 Problem Statement

Researchers spend significant time searching scientific literature, identifying research gaps, designing experiments, planning data analysis, organizing citations, and writing reports.

This project combines multiple specialized AI agents into one controlled workflow that takes a **research topic** and an optional **research PDF** and produces a structured, publication-style research report.

The system is designed to keep proposed methodology and expected outcomes separate from actual empirical findings.

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │   Streamlit Web UI   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Research Coordinator│
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Literature Review    │
                    │ Agent                │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
       Research Gap      Experiment Plan   Data Interpretation
          Agent               Agent              Agent
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Citation Manager     │
                    │ Agent                │
                    └──────────┬───────────┘
                               │
                         Human Approval
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Scientific Writer    │
                    │ Agent                │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Structured Final     │
                    │ Research Report      │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴───────────┐
                    ▼                      ▼
              Markdown Report          PDF Report
```

---

## 🤖 AI Agents

| Agent | Responsibility |
|---|---|
| 📚 **Literature Review Agent** | Finds and synthesizes source-backed academic literature |
| 🔎 **Research Gap Agent** | Identifies limitations, open problems, and future research directions |
| 🧪 **Experiment Planning Agent** | Designs hypotheses, variables, methodology, procedure, and evaluation metrics |
| 📊 **Data Interpretation Agent** | Defines data requirements and responsible analysis/interpretation methods |
| 📚 **Citation Manager Agent** | Organizes source-backed citations and APA-style references |
| ✍️ **Scientific Writer Agent** | Converts the validated research context into a structured publication-style report |

The **Research Coordinator** uses OpenAI Agents SDK handoffs to route research requests to the appropriate specialist.

---

## 🔧 Tools and APIs

The Literature Review Agent has access to six research tools:

1. **arXiv** — AI, computer science, and other preprint literature
2. **PubMed / NCBI E-utilities** — biomedical and life-science literature
3. **OpenAlex** — broad scholarly discovery
4. **Crossref** — publication and DOI metadata
5. **Web Search** — supplementary public web information
6. **PDF Reader** — extracts text from user-uploaded research papers

---

## 🔄 Research Workflow

```text
Research Topic
      │
      ▼
Literature Review
      │
      ▼
Research Gap Analysis
      │
      ▼
Experiment Planning
      │
      ▼
Data Interpretation Plan
      │
      ▼
Citation Management
      │
      ▼
Human Approval Gate
      │
      ▼
Scientific Writer
      │
      ▼
Final Structured Report
      │
      ├── Markdown
      └── PDF
```

### Workflow Steps

1. Enter a research topic.
2. Optionally upload a research PDF.
3. Start the research workflow.
4. The Literature Review Agent searches scholarly sources.
5. The Research Gap Agent analyzes limitations and open problems.
6. The Experiment Planning Agent creates a reproducible research plan.
7. The Data Interpretation Agent defines data and analysis requirements.
8. The Citation Manager organizes supported references.
9. Review the intermediate outputs.
10. Approve final report generation through the human-in-the-loop gate.
11. The Scientific Writer generates the structured `FinalReport`.
12. Download the final report as Markdown or PDF.

---

## 📦 Project Structure

```text
AI-Research-Scientist-Capstone/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── research_agents/
│   ├── __init__.py
│   ├── citation_agent.py
│   ├── coordinator.py
│   ├── data_agent.py
│   ├── experiment_agent.py
│   ├── literature_agent.py
│   ├── research_gap_agent.py
│   └── scientific_writer_agent.py
│
├── tools/
│   ├── __init__.py
│   ├── arxiv_tool.py
│   ├── crossref_tool.py
│   ├── openalex_tool.py
│   ├── pdf_reader.py
│   ├── pubmed_tool.py
│   └── web_search_tool.py
│
├── memory/
│   └── session_memory.py
│
├── schemas/
│   └── final_report_schema.py
│
├── utils/
│   ├── __init__.py
│   └── logger.py
│
├── data/
│   ├── uploads/
│   └── processed/
│
├── reports/
│   ├── json/
│   ├── markdown/
│   └── pdf/
│
└── logs/
```

Runtime-generated files inside `data/`, `reports/`, and `logs/` are ignored by Git.

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **OpenAI Agents SDK**
- **Pydantic**
- **Requests**
- **arXiv API/library**
- **PubMed / NCBI E-utilities**
- **OpenAlex API**
- **Crossref API**
- **DuckDuckGo HTML search**
- **pypdf**
- **ReportLab**

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Research-Scientist-Capstone.git
cd AI-Research-Scientist-Capstone
```

### 2. Create a virtual environment

#### Windows

```cmd
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a file named `.env` in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

**Never commit `.env` or any API key to GitHub.**

For a public repository, you can add a `.env.example` file containing only:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser at the local Streamlit address.

---

## 🧪 Example Research Topic

Try a topic such as:

```text
Reliability of retrieval-augmented generation systems for question answering
```

You can also upload a relevant research paper in PDF format to provide additional source material.

---

## 📊 Final Report Structure

The Scientific Writer Agent returns a structured `FinalReport` containing:

- Title
- Abstract
- Introduction
- Literature Review
- Research Gap
- Research Objectives
- Methodology
- Experimental Plan
- Data Analysis
- Discussion
- Limitations
- Conclusion
- Future Work
- References

The report can then be exported as:

- `.md`
- `.pdf`

---

## 🧠 Memory and Context

The application uses a lightweight `SessionMemory` dataclass to maintain short-term research context during a Streamlit session.

The workflow stores:

- Research topic
- Uploaded PDF information
- Literature review
- Research gaps
- Experiment plan
- Data analysis
- Citation information
- Final report

This is **session-based memory**, not persistent vector/RAG memory.

---

## 👤 Human-in-the-Loop

The application includes an optional human approval gate.

Before the final Scientific Writer Agent runs, the user can review:

- Literature Review
- Research Gap
- Experiment Plan
- Data Interpretation
- Citations

The final report is generated only after approval when the approval option is enabled.

---

## 🛡️ Research Integrity

The agents are explicitly instructed to:

- Never fabricate papers or authors
- Never invent citations, URLs, DOIs, or publication details
- Never fabricate experimental data
- Never claim an experiment was performed when it was not
- Clearly distinguish expected results from observed results
- State when empirical data is unavailable
- Preserve source fidelity

This makes the system suitable for **research assistance and planning**, rather than pretending to replace scientific validation.

---

## ⚠️ Limitations

- Search quality depends on the availability and quality of external APIs/services.
- Web search results are supplementary and should be independently verified.
- PDF extraction depends on the PDF containing extractable text.
- The current memory implementation is session-based.
- The system does not perform actual scientific experiments by itself.
- AI-generated research content should be reviewed by a human before academic or professional use.

---

## 🚀 Future Improvements

Possible future enhancements include:

- Persistent vector/RAG memory
- More scholarly databases
- Better source verification and deduplication
- Persistent research projects
- User authentication
- Experiment execution integrations
- Advanced data visualization
- Citation export formats such as BibTeX
- Cloud deployment
- Automated research-progress tracking

---

## 📚 Capstone Project

**Project:** AI Research Scientist  
**Program:** Summer School '26 — OpenAI Agents SDK Capstone  
**Domain:** Artificial Intelligence / Generative AI / Multi-Agent Systems

---

## 📄 License

This project is intended for educational and capstone-project purposes.

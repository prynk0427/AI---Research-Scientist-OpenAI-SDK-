import asyncio
import io
import os
import re
from datetime import datetime
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from agents import Runner

from memory.session_memory import SessionMemory
from research_agents.citation_agent import citation_agent
from research_agents.coordinator import coordinator_agent
from research_agents.data_agent import data_agent
from research_agents.experiment_agent import experiment_agent
from research_agents.literature_agent import literature_agent
from research_agents.research_gap_agent import research_gap_agent
from research_agents.scientific_writer_agent import scientific_writer_agent
from schemas.final_report_schema import FinalReport
from utils.logger import get_logger

load_dotenv()
logger = get_logger()

APP_TITLE = "AI Research Scientist"
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main-title { font-size: 42px; font-weight: 800; margin-bottom: 5px; }
    .subtitle { font-size: 18px; opacity: .75; margin-bottom: 25px; }
    .metric-card { text-align: center; padding: 15px; border-radius: 12px; border: 1px solid rgba(128,128,128,.25); }
    </style>
    """,
    unsafe_allow_html=True,
)


def init_state() -> None:
    defaults = {
        "research_topic": "",
        "uploaded_file_name": None,
        "uploaded_pdf_path": None,
        "results": {},
        "memory": SessionMemory(),
        "pipeline_stage": "idle",
        "pending_finalization": False,
        "final_report": None,
        "approved": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()


def run_agent(agent, prompt):
    """Run an OpenAI Agents SDK agent from Streamlit."""
    return asyncio.run(Runner.run(agent, prompt))


def save_uploaded_pdf(uploaded_file) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    safe_name = re.sub(r"[^A-Za-z0-9_.-]", "_", uploaded_file.name)
    path = UPLOAD_DIR / f"{timestamp}_{safe_name}"
    path.write_bytes(uploaded_file.getbuffer())
    return str(path)


def create_pdf(report_text: str) -> bytes | None:
    try:
        from reportlab.lib.enums import TA_CENTER
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

        buffer = io.BytesIO()
        document = SimpleDocTemplate(
            buffer, pagesize=A4, rightMargin=45, leftMargin=45, topMargin=45, bottomMargin=45
        )
        styles = getSampleStyleSheet()
        styles["Title"].alignment = TA_CENTER
        story = [
            Paragraph("AI Research Scientist", styles["Title"]),
            Spacer(1, 18),
        ]

        for raw in report_text.splitlines():
            line = raw.strip()
            if not line:
                story.append(Spacer(1, 7))
                continue
            safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            if line.startswith("### "):
                story.append(Paragraph(safe[4:], styles["Heading3"]))
            elif line.startswith("## "):
                story.append(Paragraph(safe[3:], styles["Heading2"]))
            elif line.startswith("# "):
                story.append(Paragraph(safe[2:], styles["Heading1"]))
            elif line.startswith("- "):
                story.append(Paragraph("• " + safe[2:], styles["BodyText"]))
            else:
                story.append(Paragraph(safe, styles["BodyText"]))

        document.build(story)
        return buffer.getvalue()
    except Exception:
        logger.exception("PDF generation failed")
        return None


def reset_project_state() -> None:
    old_path = st.session_state.get("uploaded_pdf_path")
    if old_path:
        try:
            Path(old_path).unlink(missing_ok=True)
        except Exception:
            logger.warning("Could not remove old uploaded PDF: %s", old_path)
    st.session_state.results = {}
    st.session_state.memory = SessionMemory()
    st.session_state.pipeline_stage = "idle"
    st.session_state.pending_finalization = False
    st.session_state.final_report = None
    st.session_state.approved = False
    st.session_state.uploaded_pdf_path = None
    st.session_state.uploaded_file_name = None


async def run_literature_with_coordinator(prompt: str):
    """Use the SDK handoff graph first, with a safe direct-agent fallback."""
    try:
        result = await Runner.run(coordinator_agent, prompt)
        output = result.final_output
        # If the coordinator itself answered instead of handing off, fall back to the specialist.
        text = str(output)
        if "## Research Area" in text or "## Relevant Papers" in text:
            return output
    except Exception:
        logger.exception("Coordinator handoff failed; using direct literature agent")

    return (await Runner.run(literature_agent, prompt)).final_output


with st.sidebar:
    st.title("🔬 AI Research Scientist")
    st.caption("Multi-Agent Scientific Research Platform")
    st.markdown("---")

    st.markdown("### 🤖 AI Agents")
    for name in [
        "📚 Literature Review",
        "🔎 Research Gap",
        "🧪 Experiment Planning",
        "📊 Data Interpretation",
        "📚 Citation Manager",
        "✍️ Scientific Writer",
    ]:
        st.write(name)

    st.markdown("---")
    st.markdown("### 🔧 Integrated Tools")
    for name in [
        "🔎 arXiv Search",
        "🧬 PubMed Search",
        "📚 OpenAlex Search",
        "📑 Crossref Search",
        "🌐 Web Search",
        "📄 PDF Reader",
    ]:
        st.write(name)

    st.markdown("---")
    st.markdown("### 🧠 Capstone Features")
    st.write("🔁 Agent handoffs")
    st.write("🧠 Session memory / context")
    st.write("📦 Structured final output")
    st.write("👤 Human approval gate")
    st.write("📝 Runtime logging")
    st.caption("OpenAI Agents SDK • Python • Streamlit")

st.markdown('<div class="main-title">🔬 AI Research Scientist</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Multi-Agent Research Platform powered by OpenAI Agents SDK</div>',
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("🤖 Agents", "6")
with c2:
    st.metric("🔧 Tools", "6")
with c3:
    st.metric("🧠 Memory", "Session")
with c4:
    st.metric("📦 Output", "Structured")

st.markdown("---")

st.subheader("🔬 Enter Your Research Topic")
topic = st.text_input(
    "Research Topic",
    placeholder="Example: ChatGPT reliability in retrieval-grounded question answering",
    value=st.session_state.research_topic,
)
st.session_state.research_topic = topic

st.subheader("📄 Upload Research Paper")
uploaded_file = st.file_uploader(
    "Upload a PDF (Optional)",
    type=["pdf"],
    help="The Literature Review Agent can use the PDF Reader tool to inspect the uploaded paper.",
)

require_approval = st.checkbox(
    "👤 Require human approval before generating the final report",
    value=True,
    help="The workflow pauses after citations so you can review the intermediate research context.",
)

st.markdown("---")
st.subheader("🤖 Agent Workflow")
agent_labels = ["📚 Literature", "🔎 Gap", "🧪 Experiment", "📊 Data", "📚 Citation", "✍️ Writer"]
status_cols = st.columns(6)
status_placeholders = []
for i, label in enumerate(agent_labels):
    with status_cols[i]:
        ph = st.empty()
        ph.info(f"⏳\n\n{label}")
        status_placeholders.append(ph)

start = st.button("🚀 Start Research", type="primary", use_container_width=True)

if start:
    if not topic.strip():
        st.error("Please enter a research topic first.")
        st.stop()
    if not os.getenv("OPENAI_API_KEY"):
        st.error("OPENAI_API_KEY is missing. Check your .env file.")
        st.stop()

    reset_project_state()
    st.session_state.research_topic = topic.strip()
    pdf_path = None
    if uploaded_file:
        pdf_path = save_uploaded_pdf(uploaded_file)
        st.session_state.uploaded_pdf_path = pdf_path
        st.session_state.uploaded_file_name = uploaded_file.name

    pdf_context = ""
    if pdf_path:
        pdf_context = f"""
A user-uploaded research PDF is available.
File name: {uploaded_file.name}
Local path: {pdf_path}
Use the PDF Reader tool when it is relevant.
"""

    memory = st.session_state.memory
    memory.save("topic", topic.strip())
    memory.save("uploaded_pdf", uploaded_file.name if uploaded_file else None)

    # 1. Literature + coordinator handoff
    status_placeholders[0].warning("🔄\n\n📚 Literature")
    literature_prompt = f"""
Research topic: {topic.strip()}
{pdf_context}

Begin the research workflow by handing this request to the Literature Review Agent.
Perform a source-grounded literature review. Use academic tools as appropriate.
Return research area, key concepts, relevant papers, literature findings,
important research questions, and potential research gaps.
Do not invent sources or results.
"""
    try:
        literature_output = asyncio.run(run_literature_with_coordinator(literature_prompt))
        memory.save("literature", literature_output)
        st.session_state.results["literature"] = str(literature_output)
        status_placeholders[0].success("✅\n\n📚 Literature")
    except Exception as exc:
        logger.exception("Literature stage failed")
        status_placeholders[0].error("❌\n\nLiterature")
        st.error(f"Literature Agent Error: {exc}")
        st.stop()

    # 2. Research gap
    status_placeholders[1].warning("🔄\n\n🔎 Gap")
    try:
        gap = run_agent(
            research_gap_agent,
            f"""Research Topic:\n{topic}\n\nLiterature Review:\n{literature_output}\n\nIdentify established knowledge, current limitations, potential research gaps, why they matter, and future directions. Do not invent evidence.""",
        ).final_output
        memory.save("research_gap", gap)
        st.session_state.results["research_gap"] = str(gap)
        status_placeholders[1].success("✅\n\n🔎 Gap")
    except Exception as exc:
        logger.exception("Research gap stage failed")
        status_placeholders[1].error("❌\n\nGap")
        st.error(f"Research Gap Agent Error: {exc}")
        st.stop()

    # 3. Experiment planning
    status_placeholders[2].warning("🔄\n\n🧪 Experiment")
    try:
        experiment = run_agent(
            experiment_agent,
            f"""Research Topic:\n{topic}\n\nLiterature Review:\n{literature_output}\n\nResearch Gap:\n{gap}\n\nDesign a reproducible experiment with objective, hypothesis, variables, dataset, methodology, steps, evaluation metrics, expected outcomes, risks, and limitations. Do not claim experiments were performed.""",
        ).final_output
        memory.save("experiment", experiment)
        st.session_state.results["experiment"] = str(experiment)
        status_placeholders[2].success("✅\n\n🧪 Experiment")
    except Exception as exc:
        logger.exception("Experiment stage failed")
        status_placeholders[2].error("❌\n\nExperiment")
        st.error(f"Experiment Agent Error: {exc}")
        st.stop()

    # 4. Data interpretation
    status_placeholders[3].warning("🔄\n\n📊 Data")
    try:
        data = run_agent(
            data_agent,
            f"""Research Topic:\n{topic}\n\nLiterature Review:\n{literature_output}\n\nResearch Gap:\n{gap}\n\nExperiment Plan:\n{experiment}\n\nExplain the data requirements, variables, analysis approach, evaluation metrics, interpretation rules, limitations, and sources of error. If no actual dataset/results are supplied, explicitly keep this as a proposed analysis plan.""",
        ).final_output
        memory.save("data", data)
        st.session_state.results["data"] = str(data)
        status_placeholders[3].success("✅\n\n📊 Data")
    except Exception as exc:
        logger.exception("Data stage failed")
        status_placeholders[3].error("❌\n\nData")
        st.error(f"Data Agent Error: {exc}")
        st.stop()

    # 5. Citation manager
    status_placeholders[4].warning("🔄\n\n📚 Citation")
    try:
        citations = run_agent(
            citation_agent,
            f"""Research Topic:\n{topic}\n\nLiterature Review:\n{literature_output}\n\nResearch Gap:\n{gap}\n\nExperiment Plan:\n{experiment}\n\nData Interpretation:\n{data}\n\nCreate a structured citation/reference section using only sources actually present in the literature review. Include title, authors, year, source, URL when available, relevance, in-text citations, and an APA reference list. Never invent bibliographic details.""",
        ).final_output
        memory.save("citations", citations)
        st.session_state.results["citations"] = str(citations)
        status_placeholders[4].success("✅\n\n📚 Citation")
    except Exception as exc:
        logger.exception("Citation stage failed")
        status_placeholders[4].error("❌\n\nCitation")
        st.error(f"Citation Agent Error: {exc}")
        st.stop()

    st.session_state.pipeline_stage = "awaiting_approval" if require_approval else "ready_to_write"
    st.session_state.pending_finalization = require_approval
    st.session_state.approved = not require_approval
    logger.info("Research context prepared for topic=%s", topic.strip())

    if require_approval:
        st.rerun()

# Human approval gate after the five preparation stages.
if st.session_state.pending_finalization:
    st.markdown("---")
    st.subheader("👤 Human Approval Gate")
    st.info(
        "The research context is ready. Review the Literature, Research Gap, Experiment, Data, and Citations tabs below before approving the final scientific writer."
    )
    reviewed = st.checkbox("I have reviewed the intermediate research outputs and approve final report generation.")
    approve = st.button("✅ Approve & Generate Final Report", type="primary", disabled=not reviewed, use_container_width=True)
    if approve:
        st.session_state.pending_finalization = False
        st.session_state.approved = True
        st.session_state.pipeline_stage = "writing"
        st.rerun()

# Final writer runs only after approval, or immediately when approval is disabled.
if st.session_state.approved and st.session_state.pipeline_stage in {"ready_to_write", "writing"} and not st.session_state.final_report:
    status_placeholders[5].warning("🔄\n\n✍️ Writer")
    memory = st.session_state.memory
    try:
        writer_prompt = f"""
Create the final publication-style research report for:
{memory.get('topic')}

LITERATURE REVIEW:
{memory.get('literature')}

RESEARCH GAP:
{memory.get('research_gap')}

EXPERIMENT PLAN:
{memory.get('experiment')}

DATA ANALYSIS:
{memory.get('data')}

CITATION INFORMATION:
{memory.get('citations')}

Return the report using the structured FinalReport schema.
Do not invent empirical results. If no actual experiment/data was supplied,
state that the report contains a proposed methodology and no claimed empirical results.
Preserve citation fidelity and use only the supplied source information.
"""
        result = run_agent(scientific_writer_agent, writer_prompt)
        structured = result.final_output
        if isinstance(structured, FinalReport):
            final_report = structured
        elif isinstance(structured, dict):
            final_report = FinalReport.model_validate(structured)
        else:
            raise TypeError(f"Unexpected structured output type: {type(structured).__name__}")

        st.session_state.final_report = final_report.model_dump()
        memory.save("final_report", st.session_state.final_report)
        st.session_state.results["final_report"] = final_report.to_markdown()
        st.session_state.pipeline_stage = "completed"
        status_placeholders[5].success("✅\n\n✍️ Writer")
        logger.info("Final report generated for topic=%s", memory.get("topic"))
        st.success("🎉 AI Research Scientist Pipeline Completed Successfully!")
    except Exception as exc:
        logger.exception("Scientific writer stage failed")
        status_placeholders[5].error("❌\n\nWriter")
        st.error(f"Scientific Writer Error: {exc}")

# Results
if st.session_state.results:
    st.markdown("---")
    st.header("📊 Research Results")
    results = st.session_state.results
    tabs = st.tabs(["📚 Literature", "🔎 Research Gap", "🧪 Experiment", "📊 Data", "📚 Citations", "📄 Final Report"])
    keys = ["literature", "research_gap", "experiment", "data", "citations", "final_report"]
    titles = ["📚 Literature Review", "🔎 Research Gap Analysis", "🧪 Experiment Plan", "📊 Data Interpretation", "📚 Citation Manager", "📄 Final Research Report"]
    for tab, key, title in zip(tabs, keys, titles):
        with tab:
            st.subheader(title)
            st.markdown(results.get(key, "No result yet."))

    st.markdown("---")
    st.subheader("🧠 Session Context")
    st.caption(f"Stored research artifacts: {len(st.session_state.memory.keys())}")
    st.write(", ".join(st.session_state.memory.keys()))

    if results.get("final_report"):
        final_report_text = results["final_report"]
        d1, d2 = st.columns(2)
        with d1:
            st.download_button(
                "⬇️ Download Markdown Report",
                data=final_report_text,
                file_name="AI_Research_Scientist_Report.md",
                mime="text/markdown",
                use_container_width=True,
            )
        with d2:
            pdf_data = create_pdf(final_report_text)
            if pdf_data:
                st.download_button(
                    "📄 Download PDF Report",
                    data=pdf_data,
                    file_name="AI_Research_Scientist_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

st.markdown("---")
st.markdown(
    "<div style='text-align:center;opacity:.7'>🔬 <b>AI Research Scientist</b><br>Literature • Research Gaps • Experiments • Data • Citations • Scientific Writing</div>",
    unsafe_allow_html=True,
)

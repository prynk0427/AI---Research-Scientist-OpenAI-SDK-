from agents import Agent

from research_agents.citation_agent import citation_agent
from research_agents.data_agent import data_agent
from research_agents.experiment_agent import experiment_agent
from research_agents.literature_agent import literature_agent
from research_agents.research_gap_agent import research_gap_agent
from research_agents.scientific_writer_agent import scientific_writer_agent


coordinator_agent = Agent(
    name="Research Coordinator",
    instructions="""
You are the coordinator of the AI Research Scientist system.

Route research requests to the correct specialist using SDK handoffs.
For a full research request, begin with the Literature Review Agent. The
specialists are:
- Literature Review Agent
- Research Gap Agent
- Experiment Planning Agent
- Data Interpretation Agent
- Citation Manager Agent
- Scientific Writer Agent

Do not fabricate research evidence. Your main responsibility is delegation.
""",
    handoffs=[
        literature_agent,
        research_gap_agent,
        experiment_agent,
        data_agent,
        citation_agent,
        scientific_writer_agent,
    ],
)

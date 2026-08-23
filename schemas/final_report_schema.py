from pydantic import BaseModel, Field


class FinalReport(BaseModel):
    """Structured final research report returned by the Scientific Writer Agent."""

    title: str = Field(description="Publication-style title")
    abstract: str = Field(description="Concise research abstract")
    introduction: str = Field(description="Background and problem context")
    literature_review: str = Field(description="Literature review")
    research_gap: str = Field(description="Established knowledge, limitations, and research gaps")
    research_objectives: str = Field(description="Research objectives and questions")
    methodology: str = Field(description="Proposed methodology")
    experimental_plan: str = Field(description="Experimental design and evaluation plan")
    data_analysis: str = Field(description="Data collection, analysis, and interpretation approach")
    discussion: str = Field(description="Discussion of expected implications")
    limitations: str = Field(description="Study limitations and uncertainty")
    conclusion: str = Field(description="Conclusion")
    future_work: str = Field(description="Future research directions")
    references: str = Field(description="References supported by supplied sources")

    def to_markdown(self) -> str:
        sections = [
            ("# " + self.title, ""),
            ("## Abstract", self.abstract),
            ("## Introduction", self.introduction),
            ("## Literature Review", self.literature_review),
            ("## Research Gap", self.research_gap),
            ("## Research Objectives", self.research_objectives),
            ("## Methodology", self.methodology),
            ("## Experimental Plan", self.experimental_plan),
            ("## Data Analysis", self.data_analysis),
            ("## Discussion", self.discussion),
            ("## Limitations", self.limitations),
            ("## Conclusion", self.conclusion),
            ("## Future Work", self.future_work),
            ("## References", self.references),
        ]
        return "\n\n".join(
            heading if not body else f"{heading}\n\n{body}"
            for heading, body in sections
        )

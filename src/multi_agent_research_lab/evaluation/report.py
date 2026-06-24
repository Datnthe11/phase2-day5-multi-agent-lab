"""Benchmark report rendering."""

from multi_agent_research_lab.core.schemas import BenchmarkMetrics


from multi_agent_research_lab.core.state import ResearchState

def render_markdown_report(metrics: list[BenchmarkMetrics], states: list[ResearchState] = None) -> str:
    """Render benchmark metrics to markdown.

    This report lists the latency, cost, and quality scores for comparison.
    """

    lines = ["# Benchmark Report", "", "| Run | Latency (s) | Cost (USD) | Quality | Citation Cov | Fail Rate | Notes |", "|---|---:|---:|---:|---:|---:|---|"]
    for item in metrics:
        cost = "" if item.estimated_cost_usd is None else f"{item.estimated_cost_usd:.4f}"
        quality = "" if item.quality_score is None else f"{item.quality_score:.1f}"
        cit_cov = "" if item.citation_coverage is None else f"{item.citation_coverage:.0%}"
        fail_rate = "" if item.failure_rate is None else f"{item.failure_rate:.0%}"
        lines.append(f"| {item.run_name} | {item.latency_seconds:.2f} | {cost} | {quality} | {cit_cov} | {fail_rate} | {item.notes} |")
        
    if states:
        lines.append("\n## Final Answers Comparison\n")
        for metric, state in zip(metrics, states):
            lines.append(f"### {metric.run_name}")
            answer = state.final_answer if state and state.final_answer else "*No answer generated or failed.*"
            lines.append(f"{answer}\n")
            lines.append("---\n")
            
    return "\n".join(lines) + "\n"

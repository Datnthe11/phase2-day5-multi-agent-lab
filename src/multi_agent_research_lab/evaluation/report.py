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
            
    lines.append("\n## Prompts Used\n")
    lines.append("### Single-Agent Baseline Prompt")
    lines.append("```text\nYou are a helpful assistant. Write a summary answering the user query.\n```\n")
    
    lines.append("### Multi-Agent Workflow Prompts")
    lines.append("**Supervisor**: `You are a supervisor managing a research team. Route the query to the correct worker.`")
    lines.append("**Researcher**: `You are a meticulous researcher. Search the web to find factual information based on the query.`")
    lines.append("**Analyst**: `You are a critical analyst. Read the research notes, extract key claims, identify conflicting information, and structure the data.`")
    lines.append("**Writer**: `You are an expert technical writer. Write a comprehensive, well-structured report. You MUST include in-text citations.`\n")
    
    lines.append("### Evaluator (LLM-as-a-judge) Prompts")
    lines.append("**Quality Score Prompt**:")
    lines.append("```text\nYou are an expert evaluator. Rate the quality of the following answer to the query '{query}' on a scale from 0 to 10. Only return the number.\n```\n")
    lines.append("**Citation Coverage Prompt**:")
    lines.append("```text\nYou are a strict evaluator. Analyze the text. Count the total number of factual claims. Then count how many of those claims are explicitly backed by an in-text citation (e.g. '[1]' or '(Author, Year)'). Return EXACTLY two integers separated by a comma (e.g. '5, 0' if 5 claims and 0 citations).\n```\n")
            
    return "\n".join(lines) + "\n"

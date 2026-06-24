"""Benchmark skeleton for single-agent vs multi-agent."""

from time import perf_counter
from typing import Callable

from multi_agent_research_lab.core.schemas import BenchmarkMetrics
from multi_agent_research_lab.core.state import ResearchState


Runner = Callable[[str], ResearchState]


def run_benchmark(run_name: str, query: str, runner: Runner) -> tuple[ResearchState, BenchmarkMetrics]:
    """Measure latency and return a placeholder metric object.

    TODO(student): Add quality scoring, estimated token cost, citation coverage, and error rate.
    """

    from multi_agent_research_lab.services.llm_client import LLMClient

    started = perf_counter()
    failure_rate = 0.0
    state = None
    try:
        state = runner(query)
    except Exception as e:
        failure_rate = 1.0
        
    latency = perf_counter() - started
    
    quality_score = None
    citation_coverage = None
    estimated_cost_usd = None

    if state and state.final_answer:
        llm = LLMClient()
        prompt = f"Rate the quality of the following answer to the query '{query}' on a scale from 0 to 10. Only return the number.\nAnswer: {state.final_answer}"
        resp = llm.complete("You are an expert evaluator. Rate the answer quality.", prompt)
        try:
            quality_score = float(resp.content.strip())
        except ValueError:
            quality_score = 0.0
            
        cit_prompt = f"Count the total number of main claims and the number of main claims that have citations in the following text. Return exactly two numbers separated by a comma (e.g. '5, 3').\nText: {state.final_answer}"
        cit_resp = llm.complete("You are an evaluator. Return only 'total_claims, cited_claims'.", cit_prompt)
        try:
            parts = cit_resp.content.split(",")
            total_claims = max(1, int(parts[0].strip()))
            cited_claims = int(parts[1].strip())
            citation_coverage = cited_claims / total_claims
        except Exception:
            citation_coverage = 0.0

        input_tokens = sum(r.metadata.get("input_tokens", 0) or 0 for r in state.agent_results)
        output_tokens = sum(r.metadata.get("output_tokens", 0) or 0 for r in state.agent_results)
        estimated_cost_usd = (input_tokens / 1_000_000) * 0.150 + (output_tokens / 1_000_000) * 0.600

    metrics = BenchmarkMetrics(
        run_name=run_name, 
        latency_seconds=latency, 
        quality_score=quality_score, 
        estimated_cost_usd=estimated_cost_usd,
        citation_coverage=citation_coverage,
        failure_rate=failure_rate
    )
    return state, metrics

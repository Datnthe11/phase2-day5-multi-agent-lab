import os
import sys

from dotenv import load_dotenv
from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.graph.workflow import MultiAgentWorkflow
from multi_agent_research_lab.evaluation.benchmark import run_benchmark
from multi_agent_research_lab.evaluation.report import render_markdown_report

load_dotenv()

def baseline_runner(query: str) -> ResearchState:
    from multi_agent_research_lab.services.llm_client import LLMClient
    from multi_agent_research_lab.core.schemas import AgentResult

    request = ResearchQuery(query=query)
    state = ResearchState(request=request)
    
    llm = LLMClient()
    sys_prompt = "You are a helpful assistant. Write a summary answering the user query."
    resp = llm.complete(sys_prompt, query)
    
    state.final_answer = resp.content
    state.agent_results.append(
        AgentResult(
            agent="baseline", 
            content=resp.content, 
            metadata={"input_tokens": resp.input_tokens, "output_tokens": resp.output_tokens}
        )
    )
    return state

def multi_agent_runner(query: str) -> ResearchState:
    state = ResearchState(request=ResearchQuery(query=query))
    workflow = MultiAgentWorkflow()
    result = workflow.run(state)
    return result

def main():
    query = "Who won the Best Picture award at the 96th Academy Awards in 2024, and who won Best Director? Cite your sources."
    print(f"Running baseline for query: {query}")
    baseline_state, baseline_metrics = run_benchmark("Single-Agent Baseline", query, baseline_runner)
    
    print(f"Running multi-agent for query: {query}")
    multi_state, multi_metrics = run_benchmark("Multi-Agent Workflow", query, multi_agent_runner)
    
    report_content = render_markdown_report([baseline_metrics, multi_metrics], [baseline_state, multi_state])
    
    os.makedirs("reports", exist_ok=True)
    with open("reports/benchmark_report.md", "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print("Benchmark report saved to reports/benchmark_report.md")

if __name__ == "__main__":
    main()

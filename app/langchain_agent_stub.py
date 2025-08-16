"""Reference LangChain Agent (requires OPENAI_API_KEY).

pip install langchain openai pandas networkx
export OPENAI_API_KEY=sk-...

This file shows how you'd wire tools in LangChain. It is a stub to keep
this repo runnable without external keys.
"""

from typing import Any, Dict
import os
import pandas as pd
import networkx as nx

from utils import load_data, build_lineage_graph, find_lineage_paths, compliance_checks

# Pseudocode / illustrative wiring only
def tool_search_policies(query: str) -> str:
    # Here you would do a vector DB similarity search.
    return "Policy search result for: " + query

def tool_check_compliance() -> str:
    base = os.path.dirname(os.path.dirname(__file__))
    ds, cols, lin, audits = load_data(base)
    comp = compliance_checks(ds, cols, audits)
    return comp.to_csv(index=False)

def tool_trace_lineage(dataset: str) -> str:
    base = os.path.dirname(os.path.dirname(__file__))
    ds, cols, lin, audits = load_data(base)
    g = build_lineage_graph(lin)
    if dataset not in g.nodes: return "No lineage."
    paths = find_lineage_paths(g, dataset)
    return "\n".join(" -> ".join(p) for p in paths) or "No upstream paths."

def build_agent():
    from langchain_openai import ChatOpenAI
    from langchain.tools import Tool
    from langchain.agents import initialize_agent, AgentType

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [
        Tool(name="search_policies", func=tool_search_policies, description="Search compliance docs and policies."),
        Tool(name="check_compliance", func=lambda _: tool_check_compliance(), description="Generate compliance CSV."),
        Tool(name="trace_lineage", func=tool_trace_lineage, description="Trace upstream lineage paths for a dataset."),
    ]
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    return agent

def demo():
    agent = build_agent()
    print(agent.run("List datasets with PII that are not encrypted."))
    print(agent.run("Trace the lineage of customer_profiles"))
    print(agent.run("Summarize retention requirements under GDPR."))

if __name__ == "__main__":
    print("This is a stub. Set OPENAI_API_KEY and install langchain/openai to run the demo.")
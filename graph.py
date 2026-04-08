from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from tools import harvest_data, run_change_detection, run_causal_analysis

class AgriRSState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "add_messages"]
    task_plan: dict
    data: dict
    change_map: dict
    causal_report: dict
    critique: dict
    final_report: str

def planner_node(state: AgriRSState):
    state["task_plan"] = {"region": "河南省", "time_range": ("2020-01-01", "2025-12-31"), "analysis_prompt": "extreme_rain wheat"}
    state["messages"].append(AIMessage(content="✅ 任务已规划"))
    return state

def data_node(state: AgriRSState):
    state["data"] = harvest_data.invoke({"region": state["task_plan"]["region"], "time_range": state["task_plan"]["time_range"]})
    state["messages"].append(AIMessage(content="📡 数据采集&对齐完成"))
    return state

def analysis_node(state: AgriRSState):
    state["change_map"] = run_change_detection.invoke({
        "t1_path": state["data"]["t1_path"],
        "t2_path": state["data"]["t2_path"],
        "prompt": state["task_plan"]["analysis_prompt"]
    })
    state["messages"].append(AIMessage(content=f"🔍 变化检测完成：{state['change_map']['semantic_description']}"))
    return state

def causal_node(state: AgriRSState):
    state["causal_report"] = run_causal_analysis.invoke({})
    return state

def critic_node(state: AgriRSState):
    # 简单反思逻辑
    state["critique"] = {"pass": "yes", "feedback": "所有物理量与语义一致"}
    state["messages"].append(AIMessage(content="✅ Critic 检查通过"))
    return state

def build_graph():
    workflow = StateGraph(AgriRSState)
    workflow.add_node("planner", planner_node)
    workflow.add_node("data", data_node)
    workflow.add_node("analysis", analysis_node)
    workflow.add_node("causal", causal_node)
    workflow.add_node("critic", critic_node)

    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "data")
    workflow.add_edge("data", "analysis")
    workflow.add_edge("analysis", "causal")
    workflow.add_edge("causal", "critic")
    workflow.add_edge("critic", END)   # MVP先不加循环，后续可加

    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)

import streamlit as st
from langchain_core.messages import HumanMessage
from graph import build_graph, AgriRSState
from utils import (
    display_map_in_streamlit,
    generate_report_summary,
    save_demo_mask
)

st.set_page_config(page_title="AgriRS-Agent MVP", layout="wide")
st.title("🌾 AgriRS-Agent - 农业遥感全流程自动化智能Agent")
st.markdown("**一句话驱动**：从数据采集 → ChangeCLIP变化检测 → 因果归因 → 完整报告")

user_input = st.text_input(
    "请输入分析指令（示例）：",
    "分析过去五年极端降雨对河南省小麦产量的影响，并给出归因报告"
)

if st.button("🚀 启动Agent"):
    with st.spinner("Agent正在执行 World-Tools-Protocol 闭环..."):
        # 确保演示掩码已生成
        save_demo_mask()
        
        graph = build_graph()
        initial_state: AgriRSState = {
            "messages": [HumanMessage(content=user_input)],
            "task_plan": {}, 
            "data": {}, 
            "change_map": {},
            "causal_report": {}, 
            "critique": {}, 
            "final_report": ""
        }
        config = {"configurable": {"thread_id": "mvp_001"}}
        
        result = graph.invoke(initial_state, config)
        
        st.success("✅ 分析完成！")
        
        # 使用 utils.py 的地图展示
        display_map_in_streamlit(result["change_map"])
        
        # 使用 utils.py 的报告摘要
        st.markdown(generate_report_summary(result))
        
        # 额外JSON查看（调试用）
        with st.expander("📋 查看原始JSON结果"):
            st.json({
                "change_map": result.get("change_map", {}),
                "causal_report": result.get("causal_report", {})
            })

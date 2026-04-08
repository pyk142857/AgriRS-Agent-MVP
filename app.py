import streamlit as st
import folium
from streamlit_folium import st_folium
from graph import build_graph, AgriRSState
from langchain_core.messages import HumanMessage

st.set_page_config(page_title="AgriRS-Agent MVP", layout="wide")
st.title("🌾 AgriRS-Agent - 农业遥感全流程自动化智能Agent")
st.markdown("**一句话驱动**：从数据采集 → ChangeCLIP变化检测 → 因果归因 → 完整报告")

user_input = st.text_input("请输入分析指令（示例）：", 
                           "分析过去五年极端降雨对河南省小麦产量的影响，并给出归因报告")

if st.button("🚀 启动Agent"):
    with st.spinner("Agent正在执行 World-Tools-Protocol 闭环..."):
        graph = build_graph()
        initial_state: AgriRSState = {
            "messages": [HumanMessage(content=user_input)],
            "task_plan": {}, "data": {}, "change_map": {},
            "causal_report": {}, "critique": {}, "final_report": ""
        }
        config = {"configurable": {"thread_id": "mvp_001"}}
        
        result = graph.invoke(initial_state, config)
        
        # 显示报告
        st.success("✅ 分析完成！")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("🔍 变化检测结果（Mock ChangeCLIP）")
            st.json(result["change_map"])
        
        with col2:
            st.subheader("📊 因果归因报告")
            st.json(result["causal_report"])
        
        # 模拟地图
        st.subheader("🗺️ 河南省小麦变化热力图（交互式）")
        m = folium.Map(location=[34.5, 113.5], zoom_start=7)
        folium.Marker([34.5, 113.5], popup="变化区域示例").add_to(m)
        st_folium(m, width=700, height=400)
        
        st.subheader("📝 最终分析报告")
        st.write(f"**指令**：{user_input}")
        st.write(f"**变化描述**：{result['change_map'].get('semantic_description', 'N/A')}")
        st.write(f"**反事实结论**：{result['causal_report'].get('counterfactual', 'N/A')}")

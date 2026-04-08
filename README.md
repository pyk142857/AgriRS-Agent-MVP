# AgriRS-Agent-MVP
农业遥感全流程自动化智能Agent最小可用产品（基于 World-Tools-Protocol + LangGraph + Mock ChangeCLIP
# 🌾 AgriRS-Agent-MVP

**农业遥感全流程自动化智能Agent**（Minimum Viable Product）

一句话驱动：从数据采集 → ChangeCLIP变化检测 → 因果归因 → 完整报告

### ✨ 核心特性
- 基于 **World-Tools-Protocol**（AgriWorld 架构）
- LangGraph 多Agent协同（Planner + Data + Analysis + Causal + Critic）
- 集成 **Mock ChangeCLIP**（零样本遥感变化检测）
- Streamlit 交互式 Web 界面 + Folium 地图
- 完全离线运行（所有模块均为 Mock，后续可一键替换为真实 GEE / ChangeCLIP / PROSAIL）

### 🚀 快速启动
```bash
git clone https://github.com/你的用户名/AgriRS-Agent-MVP.git
cd AgriRS-Agent-MVP
pip install -r requirements.txt
streamlit run app.py

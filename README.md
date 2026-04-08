# 🌾 AgriRS-Agent-MVP

**农业遥感全流程自动化智能Agent**（Minimum Viable Product）

基于 **World-Tools-Protocol** + **LangGraph** + **Mock ChangeCLIP** 实现一句话驱动的遥感分析闭环。

### ✨ 核心特性
- ✅ 多Agent协同（Planner → Data Harvester → Analysis Expert → Causal Analyst → Critic）
- ✅ 集成 **Mock ChangeCLIP**（零样本遥感变化检测 + 语义描述）
- ✅ **AgriWorld** 执行环境 + 坐标对齐协议
- ✅ Streamlit 交互式界面 + Folium 动态地图（变化热力图）
- ✅ `utils.py` 模块化地图与报告生成
- ✅ 支持 Docker 一键部署
- ✅ 完全离线运行（后续可无缝替换为真实 GEE / ChangeCLIP / PROSAIL）

### 🚀 快速启动

#### 方法一：本地运行（推荐开发）
```bash
git clone https://github.com/你的用户名/AgriRS-Agent-MVP.git
cd AgriRS-Agent-MVP
pip install -r requirements.txt
streamlit run app.py

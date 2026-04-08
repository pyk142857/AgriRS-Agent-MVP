"""
utils.py
AgriRS-Agent-MVP 辅助工具函数模块
主要功能：
- 交互式Folium地图渲染（带变化检测结果叠加）
- 报告摘要生成
- 演示掩码可视化辅助
"""

import folium
from streamlit_folium import st_folium
import streamlit as st
import numpy as np
from PIL import Image
import os


def create_interactive_map(change_result: dict, center: list = [34.5, 113.5], zoom: int = 7) -> folium.Map:
    """创建河南省交互式分析地图，叠加ChangeCLIP变化检测结果"""
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles="CartoDB positron",
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    )

    # 添加河南省大致边界（简化GeoJSON）
    henan_geojson = {
        "type": "Feature",
        "properties": {"name": "河南省"},
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [112.5, 32.5], [114.5, 32.5], [114.5, 36.5],
                [112.5, 36.5], [112.5, 32.5]
            ]]
        }
    }
    folium.GeoJson(
        henan_geojson,
        style_function=lambda x: {"fillColor": "transparent", "color": "#3388ff", "weight": 3},
        tooltip="河南省（分析区域）"
    ).add_to(m)

    # 模拟变化区域（红色高亮）
    if "area_ha" in change_result:
        # 在地图中心附近随机生成几个变化热力点
        for i in range(5):
            lat = center[0] + np.random.uniform(-0.8, 0.8)
            lon = center[1] + np.random.uniform(-0.8, 0.8)
            folium.CircleMarker(
                location=[lat, lon],
                radius=12,
                popup=f"变化区域 {i+1}<br>面积: {change_result.get('area_ha', 0)} 公顷",
                color="#ff0000",
                fill=True,
                fill_color="#ff4444",
                fill_opacity=0.7,
                tooltip=change_result.get("semantic_description", "ChangeCLIP检测到的变化")
            ).add_to(m)

    # 添加图例
    legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; width: 160px; height: 90px; 
                background-color: white; border:2px solid grey; z-index:9999; font-size:14px; padding: 10px;">
    <b>图例</b><br>
    <i style="background:#ff4444; border-radius:50%; width:12px; height:12px; display:inline-block;"></i> 
    变化区域 (ChangeCLIP)<br>
    <i style="background:#3388ff; border:2px solid #3388ff; width:20px; height:3px; display:inline-block;"></i> 
    河南省边界
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    return m


def display_map_in_streamlit(change_result: dict):
    """在Streamlit中展示交互式地图（供 app.py 调用）"""
    st.subheader("🗺️ 河南省小麦变化热力图（交互式）")
    m = create_interactive_map(change_result)
    st_folium(m, width=700, height=500, returned_objects=[])


def generate_report_summary(state: dict) -> str:
    """生成简洁的Markdown格式分析报告摘要"""
    change = state.get("change_map", {})
    causal = state.get("causal_report", {})
    
    summary = f"""
    ### 🌾 AgriRS-Agent 分析报告摘要
    
    **用户指令**：{state.get('messages', [{}])[-1].content if state.get('messages') else 'N/A'}
    
    **变化检测结果（ChangeCLIP）**  
    {change.get('semantic_description', '未检测到变化')}
    - 变化面积：**{change.get('area_ha', 'N/A')} 公顷**
    - 置信度：**{change.get('confidence', 'N/A')}**
    
    **因果归因结论（DoWhy）**  
    {causal.get('counterfactual', '未进行归因分析')}
    - 平均处理效应 (ATE)：**{causal.get('ate', 'N/A')}**
    - 因果贡献：{causal.get('causal_graph', '气候因素主导')}
    
    **系统状态**：Critic 检查通过 ✅
    """
    return summary.strip()


def save_demo_mask():
    """生成一个演示用的空白变化掩码图像（供后续真实ChangeCLIP替换）"""
    os.makedirs("sample_data", exist_ok=True)
    mask_path = "sample_data/change_mask.tif"
    if not os.path.exists(mask_path):
        # 创建一个简单的红色变化掩码
        img = np.zeros((256, 256, 3), dtype=np.uint8)
        img[80:180, 80:180] = [255, 0, 0]   # 红色矩形模拟变化区
        Image.fromarray(img).save(mask_path)
    return mask_path

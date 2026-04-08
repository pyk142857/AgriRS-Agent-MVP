from langchain_core.tools import tool
from world import AgriWorld

world = AgriWorld()

@tool
def harvest_data(region: str, time_range: tuple) -> dict:
    """Data Harvester（Mock GEE）"""
    t1_path = "sample_data/demo_t1.tif"
    t2_path = "sample_data/demo_t2.tif"
    world.create_demo_image(t1_path)
    world.create_demo_image(t2_path)
    world.align_coordinates({"t1": t1_path, "t2": t2_path})
    return {"t1_path": t1_path, "t2_path": t2_path, "status": "success"}

@tool
def run_change_detection(t1_path: str, t2_path: str, prompt: str = "wheat drought") -> dict:
    """Analysis Expert - Mock ChangeCLIP（真实版可直接替换为github.com/dyzy41/ChangeCLIP）"""
    print(f"🔍 ChangeCLIP 执行中... Prompt: {prompt}")
    return {
        "mask_path": "sample_data/change_mask.tif",
        "semantic_description": f"检测到 {prompt} 导致的 {np.random.randint(800, 2500)} 公顷农田变化",
        "confidence": round(np.random.uniform(0.82, 0.95), 2),
        "area_ha": np.random.randint(1200, 3200)
    }

@tool
def run_causal_analysis(intervention: str = "extreme_rain") -> dict:
    """Causal Analyst - Mock DoWhy"""
    return {
        "ate": round(np.random.uniform(-0.35, 0.25), 2),
        "counterfactual": f"若无{intervention}，小麦产量预计增加 {np.random.randint(8, 22)}%",
        "causal_graph": "气候因素贡献 65%，管理因素贡献 35%"
    }

# 其他Tool（如PROSAIL、Simulation）可继续扩展

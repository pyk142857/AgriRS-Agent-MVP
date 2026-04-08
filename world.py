import os
import numpy as np
from PIL import Image

class AgriWorld:
    def __init__(self):
        os.makedirs("sample_data", exist_ok=True)

    def execute_code(self, code: str) -> dict:
        print("🚀 AgriWorld 执行代码...")
        return {"status": "success", "result": "执行成功", "meta": {"crs": "EPSG:4326"}}

    def align_coordinates(self, data: dict) -> dict:
        print("📍 协议层：坐标系已自动对齐")
        return data

    def create_demo_image(self, path: str):
        img = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
        Image.fromarray(img).save(path)

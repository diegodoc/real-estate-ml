# real_estate_ml/scraping/pipelines.py
import json
from pathlib import Path

class RealEstatePipeline:
    def process_item(self, item, spider):
        # Exemplo: Limpar e transformar dados
        if "price" in item:
            item["price"] = float(item["price"].replace("R$", "").replace(".", "").strip())
        return item
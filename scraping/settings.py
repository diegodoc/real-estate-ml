# real_estate_ml/scraping/settings.py
import os
from pathlib import Path

# Caminho para a pasta data/raw/
PROJECT_DIR = Path(__file__).resolve().parents[2]  # Ajuste o número de parents conforme necessário
DATA_DIR = PROJECT_DIR / "data" / "raw"

# Configuração para salvar os dados coletados
FEEDS = {
    os.path.join(DATA_DIR, "olx_data.json"): {
        "format": "json",
        "encoding": "utf8",
    }
}

# Pipelines
ITEM_PIPELINES = {
    'real_estate_ml.scraping.pipelines.RealEstatePipeline': 300,
}

# Configurações adicionais (opcional)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
DOWNLOAD_DELAY = 2  # 2 segundos entre requisições
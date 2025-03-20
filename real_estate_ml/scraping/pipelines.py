# real_estate_ml/scraping/pipelines.py
import json
import re
from pathlib import Path

class RealEstatePipeline:
    def process_item(self, item, spider):
        # Clean price
        if item.get("price"):
            # Remove currency symbol and non-numeric characters
            price_str = item["price"].replace("R$", "").replace(".", "").replace(",", ".").strip()
            try:
                item["price"] = float(re.sub(r'[^\d.]', '', price_str))
            except ValueError:
                item["price"] = None
        
        # Clean area values
        for area_field in ["area_total", "area_util"]:
            if item.get(area_field):
                # Extract numeric value and convert to float
                area_str = item[area_field]
                match = re.search(r'(\d+(?:[\.,]\d+)?)', area_str)
                if match:
                    try:
                        item[area_field] = float(match.group(1).replace(',', '.'))
                    except ValueError:
                        item[area_field] = None
        
        # Clean numeric fields
        for field in ["bedrooms", "bathrooms", "parking_spots"]:
            if item.get(field):
                try:
                    item[field] = int(re.sub(r'[^\d]', '', item[field]))
                except ValueError:
                    item[field] = None
        
        # Clean condo fee and IPTU
        for fee_field in ["condo_fee", "iptu"]:
            if item.get(fee_field):
                fee_str = item[fee_field].replace("R$", "").replace(".", "").replace(",", ".").strip()
                try:
                    item[fee_field] = float(re.sub(r'[^\d.]', '', fee_str))
                except ValueError:
                    item[fee_field] = None
        
        # Convert boolean fields
        for bool_field in ["accept_pets", "furnished"]:
            if item.get(bool_field):
                item[bool_field] = "sim" in item[bool_field].lower()
        
        return item
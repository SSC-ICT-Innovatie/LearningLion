from typing import Dict, List, Tuple
import pandas as pd
import numpy as np

class WooParser:
    """
    A class with functionality to parse woo documents
    """
    
    def convert_nat_to_nan(self, obj: Dict[str, any]) -> None:
        for key, value in obj.items():
            if pd.isna(value):
                obj[key] = np.nan
                
    def convert_timestamp_to_str(self, obj: Dict[str, any]) -> None:
        for key, value in obj.items():
            if isinstance(value, pd.Timestamp):
                # Convert to string using a specific format (e.g., ISO format)
                obj[key] = value.strftime('%Y-%m-%d %H:%M:%S')

    def parse_woo(self, woo: pd.core.series.Series) -> Tuple[List[Tuple[int, str]], Dict[str, any]]:
        woo_json = woo.to_dict()
        
        # Check if 'bodytext_foi_bodyText' exists and is not NaN
        if 'bodytext_foi_bodyText' in woo_json and not pd.isna(woo_json['bodytext_foi_bodyText']):
            raw_text = woo_json['bodytext_foi_bodyText']
        # If the above condition is not met, check 'bodytext_foi_bodyTextOCR'
        elif 'bodytext_foi_bodyTextOCR' in woo_json and not pd.isna(woo_json['bodytext_foi_bodyTextOCR']):
            raw_text = woo_json['bodytext_foi_bodyTextOCR']
        else:
            return None, None
        
        # Delete keys if they exist in woo_json
        woo_json.pop('bodytext_foi_bodyText', None)
        woo_json.pop('bodytext_foi_bodyTextOCR', None)
                
        # Convert 'NaT' to 'NaN' in the dictionary, and timestamps to string
        self.convert_nat_to_nan(woo_json)
        self.convert_timestamp_to_str(woo_json)
        
        # Return 0 tuple, because the way we are currently preprocessing, we only have 1 page.        
        return [(0, raw_text)], woo_json
    
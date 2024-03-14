from typing import Dict, List, Tuple
import pandas as pd
import numpy as np

class WooParser:
    """
    A class with functionality to parse woo documents
    """
    
    def convert_nat_to_nan(self, obj: Dict[str, any]) -> None:
        for key, value in obj.items():
            # Skip the value if it is a list
            if isinstance(value, list):
                continue
            if pd.isna(value):
                obj[key] = np.nan
                
    def convert_timestamp_to_str(self, obj: Dict[str, any]) -> None:
        for key, value in obj.items():
            if isinstance(value, pd.Timestamp):
                # Convert to string using a specific format (e.g., ISO format)
                obj[key] = value.strftime('%Y-%m-%d %H:%M:%S')

    def parse_woo(self, woo: pd.core.series.Series) -> Tuple[List[Tuple[int, str]], Dict[str, any]]:
        woo_json = woo.to_dict()
        
        if 'all_foi_bodyText' not in woo_json or len(woo_json['all_foi_bodyText']) == 0:
            return None, None
        
        # Create a tuple with the index and the bodyText
        tuple_bodyText = [(i, s) for i, s in enumerate(woo_json['all_foi_bodyText'])]
        
        if len(tuple_bodyText) == 0:
            return None, None
        
        # Delete the 'all_foi_bodyText' key from the dictionary
        woo_json.pop('all_foi_bodyText', None)

        # Convert 'NaT' to 'NaN' in the dictionary, and timestamps to string
        self.convert_nat_to_nan(woo_json)
        self.convert_timestamp_to_str(woo_json)
       
        return tuple_bodyText, woo_json
    
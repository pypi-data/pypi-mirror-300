from dataclasses import dataclass
from typing import Optional


@dataclass
class WoeModulesApplicationSetting:
    # General setting
    project: str
    big_query_dataset: str

    # Query for import
    perim_query: str
    woe_query: Optional[str] = None
    beta_query: Optional[str] = None
    bucket_query: Optional[str] = None
    sample_query: Optional[str] = None

    # Name of tables to save
    save_table_name: Optional[str] = None

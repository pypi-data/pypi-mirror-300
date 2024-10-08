from datetime import date
from typing import Any, Dict

from pydantic import BaseModel


class DeprecationInfo(BaseModel):
    deprecation_date: date
    removal_date: date


class GlobalVersions(BaseModel):
    deprecated: Dict[str, DeprecationInfo]
    deployed: Dict[str, Any]

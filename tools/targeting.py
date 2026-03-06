# The prompt requested targeting tools in `tools/adsets.py` mapping to spec generation,
# but also listed `tools/targeting.py` in the project structure. This module provides specific
# targeting search wrappers that could be exposed separately from the adset builder.
# We will import the implementations from tools.adsets if they exist, or keep them here if decoupled.
# To ensure all functions exist where expected by the spec, we will import/export the duplicated ones.

from tools.adsets import (
    search_targeting_interests,
    search_targeting_behaviors,
    browse_targeting_categories,
    get_reach_estimate
)

__all__ = [
    "search_targeting_interests",
    "search_targeting_behaviors",
    "browse_targeting_categories",
    "get_reach_estimate"
]

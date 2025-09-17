from __future__ import annotations
from fastapi import Query

def pagination_params(
    page: int = Query(1, ge=1, description="1-based page index"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
):
    return page, page_size


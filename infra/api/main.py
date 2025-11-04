from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from google.cloud import bigquery
import os

PROJECT_ID = "ringed-pad-477122-k9"
DATASET_ID = "sales_analytics"
TABLE_ID   = "daily_sales"
TABLE_FQN  = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

app = FastAPI(title="Sales Analytics API", version="1.0.0")
bq = bigquery.Client(project=PROJECT_ID)

class StoreSummary(BaseModel):
    store_id: str
    row_count: int
    revenue: float


class ProductRow(BaseModel):
    product: str
    revenue: float
    qty: int
    
@app.get("/healthz")
@app.get("/healthz/")
def healthz():
    return {"status": "ok"}

# (you already have this, but keep it)
@app.get("/")
def root():
    return {"status": "ok", "service": "sales-api"}


# nice-to-have: root alias
@app.get("/")
def root():
    return {"status": "ok", "service": "sales-api"}



@app.get("/sales/summary", response_model=List[StoreSummary])
def sales_summary():
    sql = f"""
      SELECT store_id,
             COUNT(*) AS row_count,
             SUM(quantity * price) AS revenue
      FROM `{TABLE_FQN}`
      GROUP BY store_id
      ORDER BY revenue DESC
    """
    rows = bq.query(sql).result()
    out = [StoreSummary(store_id=r["store_id"],
                        row_count=r["row_count"],
                        revenue=float(r["revenue"] or 0)) for r in rows]
    return out


@app.get("/sales/top-products", response_model=List[ProductRow])
def top_products(store_id: str = Query(...), limit: int = Query(5, ge=1, le=50)):
    sql = f"""
      SELECT product,
             SUM(quantity) AS qty,
             SUM(quantity * price) AS revenue
      FROM `{TABLE_FQN}`
      WHERE store_id = @store_id
      GROUP BY product
      ORDER BY revenue DESC
      LIMIT @limit
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("store_id", "STRING", store_id),
            bigquery.ScalarQueryParameter("limit", "INT64", limit),
        ]
    )
    rows = bq.query(sql, job_config=job_config).result()
    out = [ProductRow(product=r["product"], qty=r["qty"], revenue=float(r["revenue"] or 0)) for r in rows]
    if not out:
        # nice signal when store has no data
        raise HTTPException(status_code=404, detail=f"No data for store_id={store_id}")
    return out

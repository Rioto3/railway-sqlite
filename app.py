from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import aiosqlite
import json
from typing import Dict, Any, List, Optional
import os

app = FastAPI(title="SQLite API Server", version="1.0.0")

DATABASE_PATH = "/data/main.db"

class QueryRequest(BaseModel):
    sql: str

class QueryResponse(BaseModel):
    columns: List[str]
    rows: List[Dict[str, Any]]
    row_count: int

async def execute_query(sql: str) -> QueryResponse:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(sql)
        
        if sql.strip().upper().startswith('SELECT'):
            rows = await cursor.fetchall()
            columns = [description[0] for description in cursor.description] if cursor.description else []
            return QueryResponse(
                columns=columns,
                rows=[dict(row) for row in rows],
                row_count=len(rows)
            )
        else:
            await db.commit()
            return QueryResponse(
                columns=[],
                rows=[],
                row_count=cursor.rowcount if cursor.rowcount else 0
            )

@app.get("/")
async def root():
    return {"message": "SQLite API Server", "version": "1.0.0"}

@app.get("/health")
async def health():
    try:
        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/query", response_model=QueryResponse)
async def execute_sql_query(request: QueryRequest):
    try:
        return await execute_query(request.sql)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"SQL Error: {str(e)}")

@app.get("/tables")
async def list_tables():
    try:
        result = await execute_query("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        return {"tables": [row["name"] for row in result.rows]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/tables/{table_name}/schema")
async def get_table_schema(table_name: str):
    try:
        result = await execute_query(f"PRAGMA table_info({table_name})")
        return {"table": table_name, "schema": result.rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/database/schema")
async def get_database_schema():
    try:
        result = await execute_query("SELECT sql FROM sqlite_master WHERE type='table' ORDER BY name")
        return {"schemas": [row["sql"] for row in result.rows if row["sql"]]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.on_event("startup")
async def startup_event():
    # Initialize database on startup if it doesn't exist
    if not os.path.exists(DATABASE_PATH):
        import subprocess
        subprocess.run(["python", "init_db.py"])

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
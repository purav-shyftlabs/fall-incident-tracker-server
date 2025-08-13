from fastapi import APIRouter
from app.services.database_service import database_service

router = APIRouter(prefix="/database", tags=["database"])

@router.get("/schema")
async def get_database_schema():
    """Get database schema"""
    schema_data = await database_service.get_database_schema()
    return {"schema": schema_data}

@router.get("/tables/{table_name}/schema")
async def get_table_schema(table_name: str):
    """Get schema for a specific table"""
    schema = await database_service.get_table_schema(table_name)
    return schema

@router.get("/tables/{table_name}/data")
async def get_table_data(table_name: str, limit: int = 100):
    """Get data from a specific table"""
    df = await database_service.fetch_table_data(table_name, limit)
    data = {
        "table_name": table_name,
        "rows": len(df),
        "columns": list(df.columns),
        "data": df.to_dict('records')
    }
    return data

@router.post("/execute-query")
async def execute_sql_query(query: str):
    """Execute a SQL query"""
    results = await database_service.execute_sql_query(query)
    return results

@router.get("/status")
async def get_database_status():
    """Get database status"""
    try:
        schema = await database_service.get_database_schema()
        return {
            "status": "connected",
            "tables": list(schema.keys())
        }
    except Exception as e:
        return {
            "status": "disconnected",
            "error": str(e)
        }

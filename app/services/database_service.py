import pandas as pd
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from app.config import settings

class DatabaseService:
    """Simple database service"""
    
    def __init__(self):
        self.db_url = settings.get_db_url()
        self.engine = None
    
    async def connect(self):
        """Connect to database"""
        if not self.engine:
            self.engine = create_async_engine(self.db_url)
    
    async def get_table_schema(self, table_name: str):
        """Get schema for a table"""
        await self.connect()
        async with self.engine.begin() as conn:
            # Get column info
            result = await conn.execute(text("""
                SELECT column_name, data_type
                FROM information_schema.columns 
                WHERE table_name = :table_name
                ORDER BY ordinal_position
            """), {"table_name": table_name})
            
            columns = []
            for row in result.fetchall():
                columns.append({
                    "name": row[0],
                    "type": row[1]
                })
            
            # Get row count
            count_result = await conn.execute(text(f'SELECT COUNT(*) FROM "{table_name}"'))
            row_count = count_result.scalar()
            
            return {
                "table_name": table_name,
                "columns": columns,
                "row_count": row_count
            }
    
    async def get_database_schema(self):
        """Get database schema"""
        schema_info = []
        schema_info.append("DATABASE SCHEMA:")
        schema_info.append("=" * 30)
        
        # Add table schemas
        tables = ["fall_incidents_primary", "fall_compliance_events"]
        
        for table_name in tables:
            try:
                schema = await self.get_table_schema(table_name)
                schema_info.append(f"\nTABLE: {schema['table_name']}")
                schema_info.append(f"ROWS: {schema['row_count']}")
                schema_info.append("COLUMNS:")
                
                for column in schema['columns']:
                    schema_info.append(f"  {column['name']}: {column['type']}")
                
            except Exception as e:
                schema_info.append(f"\nTABLE: {table_name} - Error: {str(e)}")
        
        return "\n".join(schema_info)
    
    async def execute_sql_query(self, sql_query: str):
        """Execute SQL query"""
        await self.connect()
        try:
            async with self.engine.begin() as conn:
                result = await conn.execute(text(sql_query))
                columns = result.keys()
                rows = result.fetchall()
                
                data = []
                for row in rows:
                    data.append(dict(zip(columns, row)))
                
                return {
                    "success": True,
                    "data": data,
                    "columns": list(columns),
                    "row_count": len(data)
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def fetch_table_data(self, table_name: str, limit: int = 100):
        """Fetch data from table"""
        await self.connect()
        query = f'SELECT * FROM "{table_name}" LIMIT {limit}'
        
        async with self.engine.begin() as conn:
            result = await conn.execute(text(query))
            rows = result.fetchall()
            columns = result.keys()
            
            df = pd.DataFrame(rows, columns=columns)
            return df
    
    async def fetch_all_tables_data(self):
        """Fetch data from all tables"""
        await self.connect()
        all_data = {}
        
        tables = ["fall_incidents_primary", "fall_compliance_events"]
        
        for table_name in tables:
            try:
                df = await self.fetch_table_data(table_name, 100)
                all_data[table_name] = df
            except Exception as e:
                print(f"Error fetching {table_name}: {str(e)}")
                continue
        
        return all_data
    
    def dataframes_to_csv_string(self, dataframes):
        """Convert DataFrames to CSV string"""
        csv_strings = []
        
        for table_name, df in dataframes.items():
            if df.empty:
                csv_strings.append(f"Table: {table_name}\nNo data\n")
                continue
            
            csv_strings.append(f"Table: {table_name}")
            csv_strings.append(f"Rows: {len(df)}, Columns: {len(df.columns)}")
            csv_strings.append("=" * 30)
            
            csv_data = df.to_csv(index=False)
            csv_strings.append(csv_data)
            csv_strings.append("\n" + "=" * 30 + "\n")
        
        return "\n".join(csv_strings)

# Create service instance
database_service = DatabaseService()

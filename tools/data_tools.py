import json
import concurrent.futures
from agno.tools import Toolkit
import clickhouse_connect
from clickhouse_client import config
from typing import List

class DataVentasTools(Toolkit):
    def __init__(self):
        super().__init__(name="DataVentasTools", cache_results=True, cache_ttl=300)
        self.register(self.run_select_query)
        self.register(self.list_schema)
        self.register(self.validate_and_rewrite_sql)
        self.register(self.run_query_batch)
        
    def create_clickhouse_client(self):
        """Crea y devuelve un cliente de ClickHouse utilizando la configuración"""
        client_config = config.get_client_config()
        try:
            client = clickhouse_connect.get_client(**client_config)
            # Probar la conexión
            version = client.server_version
            return client
        except Exception as e:
            print(f"Error al conectar a ClickHouse: {e}")
            raise

    def list_schema(self):
        """Schema Table ventas """
        
        return """
        Tabla: ventas
            Descripción: historial de transacciones de ventas FINALIZADAS 
            COLUMNAS:
            - orden (String): Orden/nota de venta
            - folio (UInt32): Folio único de transacción
            - fecha (String): Fecha de venta
            - idcliente (UInt32): ID cliente
            - nombreCliente (String): Nombre cliente
            - tienda (String): Tienda/sucursal
            - sku (UInt32): Código producto
            - producto (String): Nombre del producto
            - cantidad (UInt32): Unidades vendidas
            - precio (Float64): Precio unitario
            - descuento (Float64): Descuento aplicado
            - totalNetoItem (Float64): Total línea en valor neto
            - margen (Float64): Margen de contribución
            - categoria (String): Categoría del producto
            - subcategoria (String): Subcategoría del producto
            """

    def execute_query(self, query: str):
        """Ejecuta una consulta SQL y devuelve los resultados como una lista de diccionarios"""
        client = self.create_clickhouse_client()
        res = client.query(query, settings={"readonly": 1})
        column_names = res.column_names
        rows = []
        for row in res.result_rows:
            row_dict = {}
            for i, col_name in enumerate(column_names):
                row_dict[col_name] = row[i]
            rows.append(row_dict)
        return rows
    
    def run_select_query(self, query: str):
        """Ejecuta una consulta SELECT en la base de datos ClickHouse.
        
        Args:
            query (str): Solo el texto SQL (sin prefijos ni formato adicional)
            
        Returns:
            str: Resultados en formato JSON.
        """
        try:
            # Validar que sea una consulta SELECT
            clean_query = query.strip()
            if not clean_query.lower().startswith("select"):
                return "Error: Solo se permiten consultas SELECT por seguridad."
                
            result = self.execute_query(clean_query)
            json_result = json.dumps(result, ensure_ascii=False, indent=2)
            return json_result
        
        except concurrent.futures.TimeoutError:
            return "Error: Consulta cancelada por tiempo de espera excesivo."
        except Exception as err:
            return f"Error al ejecutar la consulta: {err}"
    
    def validate_and_rewrite_sql(self, query: str) -> str:
        """Valida y mejora la sintaxis de una consulta SQL para ClickHouse.
        
        Args:
            query (str): Consulta SQL a validar
            
        Returns:
            str: Consulta validada y reescrita o mensaje de error
        """
        try:
            # Eliminar espacios en blanco extra y normalizar
            clean_query = query.strip()
            
            # Verificar que sea una consulta SELECT
            if not clean_query.lower().startswith("select"):
                return "Error: Solo se permiten consultas SELECT por seguridad."
                
            # Aquí podrías agregar más validaciones específicas para ClickHouse
            # Por ejemplo, detectar y corregir funciones o sintaxis específicas
            
            return clean_query
        except Exception as err:
            return f"Error al validar la consulta: {err}"
    
    def run_query_batch(self, query_batch: List[dict]):
        """Ejecuta un lote de consultas SELECT en ClickHouse.
        
        Args:
            query_batch (List[dict]): Lista de diccionarios con formato {objetivo:"", query:""}
            
        Returns:
            str: JSON con lista de resultados con formato {objetivo:"", resultado:"", status:"success|error"}
        """
        if not isinstance(query_batch, list):
            return "Error: Se esperaba una lista de consultas."
            
        results = []
        
        for item in query_batch:
            if not isinstance(item, dict) or "objetivo" not in item or "query" not in item:
                results.append({
                    "objetivo": "desconocido",
                    "resultado": "Error: Formato incorrecto. Se esperaba {objetivo:'', query:''}",
                    "status": "error"
                })
                continue
                
            objetivo = item["objetivo"]
            query = item["query"]
            
            try:
                # Validar que sea una consulta SELECT
                clean_query = query.strip()
                if not clean_query.lower().startswith("select"):
                    results.append({
                        "objetivo": objetivo,
                        "resultado": "Error: Solo se permiten consultas SELECT por seguridad.",
                        "status": "error"
                    })
                    continue
                    
                query_result = self.execute_query(clean_query)
                results.append({
                    "objetivo": objetivo,
                    "resultado": query_result,
                    "status": "success"
                })
                
            except Exception as err:
                results.append({
                    "objetivo": objetivo,
                    "resultado": f"Error: {str(err)}",
                    "status": "error"
                })
        
        return json.dumps(results, ensure_ascii=False, indent=2)

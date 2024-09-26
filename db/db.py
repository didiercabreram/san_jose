
# Configuración de la conexión a la base de datos SQL Server
server = 'Vulcano'
database = 'DGEMPRES50'
username = 'estadistica'
password = '3st4d15t1c4'
driver = 'ODBC Driver 17 for SQL Server'

# Cadena de conexión
connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'

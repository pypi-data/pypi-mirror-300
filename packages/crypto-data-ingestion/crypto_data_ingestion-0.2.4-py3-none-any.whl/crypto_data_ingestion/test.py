from data_operations import *
from storage import *

storage = LocalStorage()

engine = DataProcessing(storage)

# Ler dados brutos
df = engine.read_raw_data(
    'json',
    'crypto-data',
    '10_landing/trending/2024/10/08/trending_coins_2024-10-08.json',
)

# Converter tipos de dados
df = df.convert_dtypes()

# Registrar DataFrame no DuckDB
engine.register_dataframe(df, 'trending_coins')

# Executar uma consulta SQL
query_result = engine.run_sql_query(
    'SELECT * FROM trending_coins WHERE market_cap > 1000000'
)

# Salvar a tabela Delta no MinIO
engine.save_delta_table(
    table_path='s3a://crypto-data/20_raw/trending_coins',
    write_mode='append',
    schema_mode='merge',
    data=query_result
)


# df = engine.read_delta_table('s3a://crypto-data/20_raw/trending_coins')

# print(df)
# data_utils

# Example
today = datetime.today().strftime('%Y-%m-%d')
fm = FileManager()

# SQL Client 
dbsettings = fm.read_yaml_config(config, 'postgres')
cli = SQLClient(dbsettings)
query = f"SELECT * FROM cbrf.currency WHERE valute_load ='{today}';"
res = cli.execute_one(query, True)
cli.close_connection()

# S3 Example
s3settings = fm.read_yaml_config(config, 's3')
s3cli = S3Client(s3settings)
s3files = s3cli.get_info_from_s3('zip')

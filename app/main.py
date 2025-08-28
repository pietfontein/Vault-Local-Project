import hvac
import os

VAULT_ADDR = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
VAULT_TOKEN = os.getenv("VAULT_TOKEN")

client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)

secret_path = 'secret/data/myapp'
secret = client.secrets.kv.v2.read_secret_version(path='myapp')

username = secret['data']['data']['username']
password = secret['data']['data']['password']

print(f"Retrieved secret: username={username}, password={password}")

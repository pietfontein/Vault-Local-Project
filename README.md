# Vault Local Project

This project demonstrates **local secret management** using **HashiCorp Vault** and a Python application.  
It allows you to **securely store and retrieve sensitive information**, such as credentials, entirely locally.  

Vault is a tool designed to **safely store secrets, manage access, and audit usage**, even in local development environments.

---

## **Project Structure**

vault-local-project/
│
├── vault/
│ └── config.hcl # Vault configuration
│
├── app/
│ └── main.py # Python app to read secrets
│
├── requirements.txt # Python dependencies
└── README.md

## **Why Use Vault Locally?**

- Keeps sensitive credentials out of code.  
- Provides a **centralized, auditable secret store**.  
- Prepares you for **production-grade secret management**.  
- Safe sandbox environment for learning Vault without deploying servers.

## **Step 1: Configure Vault**

Create a `vault/config.hcl` file:

```hcl
storage "file" {
  path = "./vault/data"  # Stores secrets on disk (safe for local dev)
}

listener "tcp" {
  address     = "192.------"  # Vault server address
  tls_disable = 1                  # Disable TLS for local dev
}

ui = true  # Enable web UI for easier inspection
````

**Explanation:**

* `storage "file"` keeps secrets locally.
* `listener "tcp"` starts Vault server on localhost.
* `tls_disable=1` is okay for local dev but **never use in production**.
* `ui = true` enables the web interface to view secrets visually.

---

## **Step 2: Start Vault Server**

```bash
cd vault
vault server -config=config.hcl
```

Open a new terminal and set environment variable:

```bash
export VAULT_ADDR='http://------'
```

**Why:**
Vault runs as a server. `VAULT_ADDR` tells the CLI and apps where to connect.

---

## **Step 3: Initialize and Unseal Vault**

```bash
vault operator init
```

* Vault outputs **unseal keys** and a **root token**.
* Unseal Vault:

```bash
vault operator unseal <unseal_key_1>
vault operator unseal <unseal_key_2>
vault operator unseal <unseal_key_3>
```

* Login with root token:

```bash
vault login <root_token>
```

**Explanation:**

* Vault encrypts all data with a master key.
* The master key is split into unseal keys to prevent accidental loss.
* Initialization and unsealing ensure only authorized users can start Vault.

---

## **Step 4: Enable Secrets Engine**

```bash
vault secrets enable -path=secret kv
```

**Explanation:**

* The KV (Key-Value) secrets engine stores arbitrary secrets.
* `-path=secret` defines the URL path to access secrets.

---

## **Step 5: Store a Secret**

```bash
vault kv put secret/myapp username="admin" password="mypassword123"
```

**Explanation:**

* Stores sensitive credentials securely.
* They are **encrypted at rest** by Vault.
* Easy to update or revoke later without changing code.

---

## **Step 6: Setup Python Application**

1. Create a virtual environment:

```bash
python -m venv env
source env/bin/activate  # Linux/Mac
```
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set Vault token environment variable:

```bash
export VAULT_TOKEN=<your_root_token>
```

**Explanation:**

* Virtual environments isolate dependencies.
* The Python app uses `hvac` library to authenticate and retrieve secrets from Vault.

---

## **Step 7: Python App to Retrieve Secrets**

`app/main.py`:

```python
import hvac
import os

VAULT_ADDR = os.getenv("VAULT_ADDR", "http://")
VAULT_TOKEN = os.getenv("VAULT_TOKEN")

client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)

secret = client.secrets.kv.v2.read_secret_version(path='myapp')

username = secret['data']['data']['username']
password = secret['data']['data']['password']

print(f"Retrieved secret: username={username}, password={password}")
```

Run the app:

```bash
python app/main.py
```

**Output:**

```
Retrieved secret: username=admin, password=mypassword123
```

**Explanation:**

* The app authenticates using Vault token.
* Reads the secret at `secret/myapp`.
* Secret values are safely retrieved **at runtime**, not hardcoded.

---

## **Step 8: Notes**

* This setup is for **local development**.
* Never commit Vault root tokens or unseal keys.
* For production, enable TLS, authentication backends, and access policies.

---

## **Step 9: Optional - Zip or Push to GitHub**

Or initialize git and push:

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <repo-url>
git branch -M main
git push -u origin main
```

---

## **Summary**

This project teaches:

* How Vault securely stores secrets.
* How to retrieve secrets in applications without exposing credentials.
* Local development setup that mirrors real-world secret management.
* Best practices for secret isolation and security
```

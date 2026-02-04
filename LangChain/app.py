import os
from pathlib import Path

# Load API_KEY from the environment or from the local app.env file
API_KEY = os.environ.get("API_KEY")

if not API_KEY:
    env_file = Path(__file__).with_name("app.env")
    if env_file.exists():
        with env_file.open() as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    if k.strip() == "API_KEY":
                        API_KEY = v.strip().strip('"').strip('\'')
                        break

# Ensure there's a defined variable even if empty
if not API_KEY:
    API_KEY = None

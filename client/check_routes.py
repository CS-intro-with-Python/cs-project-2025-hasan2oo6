import os
import requests

BASE = os.getenv("BASE_URL", "http://127.0.0.1:8000")

def main():
    r = requests.get(BASE + "/", timeout=10)
    assert r.status_code == 200, f"/ returned {r.status_code}"
    print("OK: / is reachable")

if __name__ == "__main__":
    main()

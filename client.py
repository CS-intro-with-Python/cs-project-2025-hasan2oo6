import requests
import sys



response = requests.get("http://localhost:5000/")

print("Received:", response.text)

if response.status_code != 200:
    print("Server error")
    sys.exit(1)   # FAIL workflow
else:
    print("Server OK")

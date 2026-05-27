import json
from urllib.request import urlopen

def main():
    with urlopen("http://localhost:8000/metrics/cpu?seconds=5") as response:
        payload = json.loads(response.read().decode("utf-8"))
        print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()

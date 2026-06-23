import json
import requests

from config import LLM_BACKEND, LLM_BASE_URL, LLM_MODEL, LLM_API_KEY


def main():
    print("Current backend config:")
    print("LLM_BACKEND:", LLM_BACKEND)
    print("LLM_BASE_URL:", LLM_BASE_URL)
    print("LLM_MODEL:", LLM_MODEL)
    print("LLM_API_KEY:", LLM_API_KEY)
    print()

    models_url = LLM_BASE_URL.rstrip("/") + "/models"

    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}"
    }

    try:
        response = requests.get(models_url, headers=headers, timeout=30)

        print("GET", models_url)
        print("HTTP status code:", response.status_code)
        print()

        if response.status_code == 200:
            data = response.json()
            print("Available models:")
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print("Raw response:")
            print(response.text)

    except Exception as e:
        print("Failed to connect to backend:")
        print(e)


if __name__ == "__main__":
    main()
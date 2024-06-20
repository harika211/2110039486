import requests # type: ignore

THIRD_PARTY_API_URL = 'http://example.com/api'  # Replace with the actual third-party URL

def fetch_number(numberid):
    try:
        response = requests.get(f"{THIRD_PARTY_API_URL}/{numberid}", timeout=0.5)
        response.raise_for_status()
        numbers = response.json().get('numbers', [])
        return numbers
    except requests.RequestException:
        return None

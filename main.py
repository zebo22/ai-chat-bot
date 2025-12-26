def get_ai_reply(text):
    response = requests.post(
        HF_MODEL,
        headers={"Authorization": f"Bearer {HF_API_KEY}"},
        json={"inputs": text},
        timeout=30
    )

    print("RAW HF RESPONSE:", response.text)

    try:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            return data[0].get("generated_text", "NO generated_text")
        return str(data)
    except Exception as e:
        return f"JSON error: {e}"
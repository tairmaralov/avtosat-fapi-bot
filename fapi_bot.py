from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "6d899f77-35a7-4cfb-a91d-ce981a686ebc"
BASE_URL = "https://fapi.iisis.ru/fapi/v2/productList"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    user_message = data.get("text", "").strip()

    BASE_URL = "https://fapi.iisis.ru/fapi/v2/productList"
    API_KEY = os.environ.get("FAPI_UI")  # ключ берём из переменных окружения

    params = {"n": user_message, "comparison": True, "ui": API_KEY}
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        print("🔹 URL:", response.url)
        print("🔹 Status:", response.status_code)
        print("🔹 Body:", response.text[:500])
    except Exception as e:
        print("❌ Ошибка запроса:", e)
        return jsonify({"text": f"Ошибка подключения к API: {e}"}), 500

    if response.status_code == 200:
        try:
            products = response.json()
        except Exception:
            return jsonify({"text": "Ошибка при чтении ответа API"})

        if isinstance(products, list) and len(products) > 0:
            code = products[0].get("n", "код не найден")
            return jsonify({"text": f"Код детали: {code}"})
        else:
            return jsonify({"text": "Ничего не найдено"})
    else:
        return jsonify({"text": f"Ошибка при обращении к API ({response.status_code})"})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

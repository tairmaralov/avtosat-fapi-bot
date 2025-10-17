from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "6d899f77-35a7-4cfb-a91d-ce981a686ebc"
BASE_URL = "https://fapi.iisis.ru/fapi/v2/productList"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    user_message = data.get("text")
    if not user_message:
        return jsonify({"text": "Введите название детали"})

    params = {"n": user_message, "comparison": True, "ui": API_KEY}
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        products = response.json()
        if isinstance(products, list) and len(products) > 0:
            code = products[0].get("n", "код не найден")
            return jsonify({"text": f"Код детали: {code}"})
        else:
            return jsonify({"text": "Ничего не найдено"})
    else:
        return jsonify({"text": "Ошибка при обращении к API"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

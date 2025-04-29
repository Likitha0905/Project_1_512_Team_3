from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", 3500)
ORDER_PROCESSOR_APP_ID = "order-processor"  # The Dapr app-id of the order-processor service

@app.route('/order', methods=['POST'])
def create_order():
    data = request.json
    item = data.get('item')
    quantity = data.get('quantity')

    if not item or not quantity:
        return jsonify({"error": "Please provide item and quantity"}), 400

    order_payload = {"item": item, "quantity": quantity}

    try:
        dapr_url = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/invoke/{ORDER_PROCESSOR_APP_ID}/method/process-order"
        response = requests.post(dapr_url, json=order_payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to invoke order-processor: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
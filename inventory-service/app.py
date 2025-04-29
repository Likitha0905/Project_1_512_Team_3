from flask import Flask, request, jsonify
import os
from dapr.clients import DaprClient

app = Flask(__name__)
DAPR_GRPC_PORT = os.getenv("DAPR_GRPC_PORT", 50002)
PUBSUB_NAME = "order-pubsub"    # The name of your Dapr pub/sub component
INVENTORY_STORE_NAME = "statestore" # Assuming we use the same state store

@app.route('/dapr/subscribe', methods=['GET'])
def subscribe():
    return jsonify([
        {
            "pubsubname": PUBSUB_NAME,
            "topic": "order-created",
            "route": "/inventory/update"
        }
    ])

@app.route('/inventory/update', methods=['POST'])
def update_inventory():
    try:
        event_data = request.get_json()
        item = event_data.get('item')
        quantity = event_data.get('quantity')
        order_id = event_data.get('order_id')

        if not item or quantity is None:
            return jsonify({"error": "Invalid order event data"}), 400

        with DaprClient() as d:
           
            print(f"Inventory updated for item '{item}' due to order {order_id}. Quantity: {quantity}")



        return jsonify({"message": f"Inventory update processed for order {order_id}"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to update inventory: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)
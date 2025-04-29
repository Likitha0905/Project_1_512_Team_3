from flask import Flask, request, jsonify
import os
from dapr.clients import DaprClient

app = Flask(__name__)
DAPR_GRPC_PORT = os.getenv("DAPR_GRPC_PORT", 50002)
STATE_STORE_NAME = "statestore"  # The name of your Dapr state store component
PUBSUB_NAME = "order-pubsub"    # The name of your Dapr pub/sub component
ORDER_CREATED_TOPIC = "order-created"

@app.route('/process-order', methods=['POST'])
def process_order():
    data = request.json
    item = data.get('item')
    quantity = data.get('quantity')

    if not item or not quantity:
        return jsonify({"error": "Please provide item and quantity"}), 400

    order_id = f"order-{int(time.time())}"
    order_details = {"order_id": order_id, "item": item, "quantity": quantity, "status": "pending"}

    try:
        with DaprClient() as d:
            # Save the order using Dapr state management
            d.save_state(STATE_STORE_NAME, order_id, order_details).result()

            # Publish an "order created" event using Dapr pub/sub
            d.publish_event(
                pubsub_name=PUBSUB_NAME,
                topic_name=ORDER_CREATED_TOPIC,
                event_data=jsonify(order_details).get_data(as_text=True),
                event_type="com.example.order.created"
            ).result()

        return jsonify({"message": f"Order {order_id} created and processing"}), 201
    except Exception as e:
        return jsonify({"error": f"Failed to process order: {e}"}), 500

if __name__ == '__main__':
    import time
    app.run(debug=True, port=5001)
    
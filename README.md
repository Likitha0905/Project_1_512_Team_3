# Project_1_512_Team_3
This project demonstrates a basic e-commerce order processing system built using Python and the Distributed Application Runtime (Dapr). It showcases inter-service communication using Dapr's Service Invocation, state management with Dapr's State Management, and event-driven architecture using Dapr's Pub/Sub.

## Project Components

The system consists of the following microservices:

1.  **`frontend-service` (Python):**
    * A simple web application that provides an endpoint to create new orders.
    * Uses Dapr's Service Invocation to communicate with the `order-processor` service.

2.  **`order-processor` (Python):**
    * A backend service responsible for receiving and processing order requests.
    * Uses Dapr's State Management to persist order details.
    * Uses Dapr's Pub/Sub to publish an "order created" event.

3.  **`inventory-service` (Python):**
    * A service that subscribes to the "order created" event.
    * Simulates updating inventory levels upon receiving a new order (currently logs the event).

## Dapr Building Blocks Demonstrated

* **Service Invocation:** The `frontend-service` calls the `order-processor` to handle order creation.
* **State Management:** The `order-processor` persists order information using an in-memory state store.
* **Pub/Sub:** The `order-processor` publishes an "order-created" event, which the `inventory-service` subscribes to.




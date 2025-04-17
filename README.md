# Project_1_512_Team_3
This is a simple microservices demo using Dapr, Python (Flask), and MongoDB, created as part of Project 1 for class 512.
This project contains two Python microservices:

1. user-service
   - Adds and retrieves user data from MongoDB.
   - Exposes two endpoints: `/add` (POST) and `/get/<name>` (GET).

2. api-gateway
   - Calls `user-service` using Dapr service invocation.
   - Has a single route: `/user/<name>` (GET), which internally calls the user-service.

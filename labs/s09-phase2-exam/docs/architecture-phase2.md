# ARCHITECTURE DIAGRAM — PHASE 2 END-TO-END REQUEST FLOW

```mermaid
graph TD
    Client["Client / Browser (curl)"] -->|1. HTTP Request Port 8080| Nginx["Nginx Reverse Proxy (Port 8080)"]
    Nginx -->|2. Check Config exam_phase2.conf| ProxyPass{"Proxy Pass Directive"}
    ProxyPass -->|3. Forward to 127.0.0.1:8000| PythonBackend["Python Backend App (Port 8000)"]
    PythonBackend -->|4. Return Response 200 OK| Nginx
    Nginx -->|5. Return Response HTTP 200 OK| Client

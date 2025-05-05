from flask import Flask, request, jsonify
import sqlite3
import json
import requests
from flasgger import Swagger

app = Flask(__name__)

# Initialize Swagger UI
swagger = Swagger(app)

# Function to search for the endpoint in the database
def search_endpoint(query):
    conn = sqlite3.connect("api_schema4_rmm.db")
    cursor = conn.cursor()
    cursor.execute("SELECT path, method, description, request_body, responses FROM api_endpoints WHERE path LIKE ?", (f"%{query}%",))
    results = cursor.fetchall()
    conn.close()

    return [{"path": path, "method": method, "description": description,
             "request_body": json.loads(request_body) if request_body != "None" else None,
             "responses": json.loads(responses)} for path, method, description, request_body, responses in results]

# Function to forward requests to the external API
def forward_request(endpoint, method, headers=None, data=None, params=None):
    url = f"https://api.trmm.org{endpoint}"
    if method.lower() == "get":
        response = requests.get(url, headers=headers, params=params)
    elif method.lower() == "post":
        response = requests.post(url, headers=headers, json=data)
    elif method.lower() == "put":
        response = requests.put(url, headers=headers, json=data)
    elif method.lower() == "delete":
        response = requests.delete(url, headers=headers)
    else:
        return jsonify({"error": "Unsupported HTTP method"}), 405
    
    # Forward the response from the external API back to the client
    return jsonify(response.json()), response.status_code

# API endpoint to handle the query and forward the request
@app.route('/query', methods=['GET'])
def query_api():
    """
    Query the API schema for an endpoint.
    ---
    parameters:
      - name: query
        in: query
        type: string
        required: true
        description: The path or query to search for in the API schema.
    responses:
      200:
        description: A list of matching API paths, methods, and descriptions.
        schema:
          type: array
          items:
            type: object
            properties:
              path:
                type: string
                description: API endpoint path.
              method:
                type: string
                description: HTTP method for the endpoint.
              description:
                type: string
                description: Description of the endpoint.
    security:
      - API Key Auth: []
    """
    query = request.args.get("query", "")
    results = search_endpoint(query)
    
    if not results:
        return jsonify({"error": "No matching endpoints found"}), 404
    
    # Extract endpoint and method from the results
    endpoint_info = results[0]  # You can customize this if there are multiple results
    endpoint = endpoint_info['path']
    method = endpoint_info['method'].lower()

    # Forward the request to the external API
    api_key = request.headers.get('X-API-KEY')
    headers = {"X-API-KEY": api_key}
    data = request.get_json() if request.method in ['POST', 'PUT'] else None
    params = request.args if request.method == 'GET' else None
    
    return forward_request(endpoint, method, headers=headers, data=data, params=params)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5086)

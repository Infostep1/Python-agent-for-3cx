
import requests
import json
import os
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 5000
BASE_URL = "https://gvgp.oncloud.gr/s1services"
USERNAME = "gvjp"
PASSWORD = "1234"
APP_ID = "157"

def login(username, password, appId):
    payload = {
        "service": "login",
        "username": username,
        "password": password,
        "appId": str(appId)
    }
    response = requests.post(BASE_URL, json=payload)
    response.raise_for_status()
    data = response.json()
    if not data.get("success"):
        raise Exception(f"Login failed: {data}")
    return data

def authenticate(clientID, company, branch, module, refid):
    payload = {
        "service": "authenticate",
        "clientID": clientID,
        "company": company,
        "branch": branch,
        "module": module,
        "refid": refid
    }
    response = requests.post(BASE_URL, json=payload)
    response.raise_for_status()
    data = response.json()
    if not data.get("success"):
        raise Exception(f"Authentication failed: {data}")
    return data["clientID"]

def get_customer_by_key(base_url, client_id, app_id, customer_key):
    payload = {
        "service": "getData",
        "clientID": client_id,
        "appId": app_id,
        "object": "CUSTOMER",
        "form": "",
        "key": customer_key,
        "locateinfo": "CUSTOMER:CODE,NAME,AFM"
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(base_url, data=json.dumps(payload), headers=headers)
    response.raise_for_status()
    result = response.json()
    if result.get("success"):
        return result.get("data")
    else:
        raise Exception(f"Soft1 getData error: {result.get('error', 'Unknown error')}")

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/trigger":
            try:
                login_data = login(USERNAME, PASSWORD, APP_ID)
                obj_info = login_data.get("objs", [{}])[0]
                new_client_id = authenticate(
                    login_data["clientID"],
                    obj_info.get("COMPANY"),
                    obj_info.get("BRANCH"),
                    obj_info.get("MODULE"),
                    obj_info.get("REFID")
                )
                customer_key = "3079"
                customer_data = get_customer_by_key(BASE_URL, new_client_id, APP_ID, customer_key)
                with open("customer_data.json", "w") as f:
                    json.dump(customer_data, f)
                webbrowser.open(f"http://localhost:{PORT}/static/login.html")
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Login and data fetch successful.")
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Error: {str(e)}".encode())

        elif self.path == "/customer-data":
            try:
                with open("customer_data.json") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(data.encode())
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Customer data not found")

        elif self.path == "/static/login.html":
            try:
                with open("static/login.html", "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"login.html not found")
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    print(f"Listening on http://localhost:{PORT}/trigger")
    server = HTTPServer(('0.0.0.0', PORT), RequestHandler)
    server.serve_forever()

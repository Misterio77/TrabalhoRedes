import requests
import telnetlib
import time

TELNET_HOSTNAME = "celaeno"

class Server:
    url = None
    def __init__(self, url):
        self.url = url

    def get_project(self, name):
        projects = requests.get(f"{self.url}/projects").json()
        data = next((p for p in projects if p["name"] == name), None)
        return Project(data, self.url)

    def create_project(self, name):
        payload = {"name": name}
        data = requests.post(f"{self.url}/projects", json=payload).json()
        return Project(data, self.url)

    def project(self, name):
        project = self.get_project(name)
        if not project:
            project = self.create_project(name)
        return project

class Project:
    data = None
    url = None
    def __init__(self, data, server_url):
        if data != None:
            self.data = data
            self.id = data["project_id"]
            self.url = f"{server_url}/projects/{self.id}"

    def get_node(self, name):
        nodes = requests.get(f"{self.url}/nodes").json()
        data = next((n for n in nodes if n["name"] == name), None)
        return Node(data, self.url)

    def create_node(self, name, payload):
        payload["name"] = name
        data = requests.post(f"{self.url}/nodes", json=payload).json()
        return Node(data, self.url)

    def node(self, name, payload, destroy=False):
        node = self.get_node(name)
        if destroy and node:
            node.destroy()
            node = None
        if not node:
            node = self.create_node(name, payload)
        return node

    def link_nodes(self, node1, adapter1, port1, node2, adapter2, port2):
        return requests.post(f"{self.url}/links", json={
            "nodes": [
                {
                    "node_id": node1.id,
                    "adapter_number": adapter1,
                    "port_number": port1,
                },
                {
                    "node_id": node2.id,
                    "adapter_number": adapter2,
                    "port_number": port2,
                }
            ]
        }).json()

class Node:
    data = None
    url = None
    def __init__(self, data, project_url):
        if data != None:
            self.data = data
            self.id = data["node_id"]
            self.url = f"{project_url}/nodes/{self.id}"

    def destroy(self):
        if self.url:
            requests.delete(self.url)

    def start(self):
        return requests.post(f"{self.url}/start").json()

    def stop(self):
        return requests.post(f"{self.url}/stop").json()

    def run_command(self, command):
        with telnetlib.Telnet(TELNET_HOSTNAME, self.data["console"]) as session:
            for line in command.splitlines():
                session.write(line.encode())
                session.write(b'\r\n')

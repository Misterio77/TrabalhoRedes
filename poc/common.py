import requests
import telnetlib
import time

TELNET_HOSTNAME = "celaeno"

# Projects 

def list_projects(server):
    return requests.get(f"{server}/projects").json()

def get_project_by_name(server, name):
    projects = list_projects(server)
    return next((p for p in projects if p["name"] == name), None)

def create_project(server, name):
    payload = {"name": name}
    return requests.post(f"{server}/projects", json=payload).json()

def get_project(server, name):
    project = get_project_by_name(server, name)
    if not project:
        project = create_project(server, name)
    return project

# Nodes

def list_nodes(server, project):
    project_id = project["project_id"]
    return requests.get(f"{server}/projects/{project_id}/nodes").json()

def get_node_by_name(server, project, name):
    nodes = list_nodes(server, project)
    return next((n for n in nodes if n["name"] == name), None)

def create_node(server, project, name, payload):
    payload["name"] = name
    project_id = project["project_id"]
    return requests.post(f"{server}/projects/{project_id}/nodes", json=payload).json()

def get_node(server, project, name, payload, destroy=False):
    node = get_node_by_name(server, project, name)
    if destroy and node:
        destroy_node(server, project, node)
        node = None
    if not node:
        node = create_node(server, project, name, payload)
    return node

def destroy_node(server, project, node):
    project_id = project["project_id"]
    node_id = node["node_id"]
    requests.delete(f"{server}/projects/{project_id}/nodes/{node_id}")

def start_node(server, project, node):
    project_id = project["project_id"]
    node_id = node["node_id"]
    return requests.post(f"{server}/projects/{project_id}/nodes/{node_id}/start").json()

def stop_node(server, project, node):
    project_id = project["project_id"]
    node_id = node["node_id"]
    return requests.post(f"{server}/projects/{project_id}/nodes/{node_id}/stop").json()

def run_node_command(server, project, node, command):
    with telnetlib.Telnet(TELNET_HOSTNAME, node["console"]) as session:
        for line in command.splitlines():
            session.write(line.encode())
            session.write(b'\r\n')

def link_nodes(server, project, node1, node1_int, node2, node2_int):
    project_id = project["project_id"]
    return requests.post(f"{server}/projects/{project_id}/links", json={
        "nodes": [
            {
                "adapter_number": 0,
                "port_number": node1_int,
                "node_id": node1["node_id"],
            },
            {
                "adapter_number": 0,
                "port_number": node2_int,
                "node_id": node2["node_id"],
            }
        ]
    }).json()

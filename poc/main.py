from common import get_node, get_project, start_node, run_node_command, link_nodes

SERVER = f"https://admin:icmc1234@gns3.m7.rs/v2"

project = get_project(SERVER, "pocpoc")

router1 = get_node(SERVER, project, "R1", {
    "compute_id": "local",
    "node_type": "dynamips",
    "x": 0,
    "properties": {
        "platform": "c3745",
        "nvram": 256,
        "image": "c3745-adventerprisek9-mz.124-25d.image",
        "ram": 256, 
        "slot0": "GT96100-FE",
        "slot1": "NM-1FE-TX",
        "slot2": "NM-4T",
        "system_id": "FTX0945W0MY",
        "startup_config_content": """
            hostname ciclano
        """,
    }
}, destroy=True)
start_node(SERVER, project, router1)

router2 = get_node(SERVER, project, "R2", {
    "compute_id": "local",
    "node_type": "dynamips",
    "x": 100,
    "properties": {
        "platform": "c3745",
        "nvram": 256,
        "image": "c3745-adventerprisek9-mz.124-25d.image",
        "ram": 256, 
        "slot0": "GT96100-FE",
        "slot1": "NM-1FE-TX",
        "slot2": "NM-4T",
        "system_id": "FTX0945W0MY",
        "startup_config_content": """
            hostname fulano
        """,
    }
}, destroy=True)
start_node(SERVER, project, router2)

# run_node_command(SERVER, project, router2, """
#     enable
#     conf t
#     hostname foobar
#     exit
#     exit
# """)

link_nodes(SERVER, project, router1, router2)

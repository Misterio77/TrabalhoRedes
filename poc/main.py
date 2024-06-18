from common import get_node, get_project, start_node, run_node_command, link_nodes, create_node

SERVER = f"https://admin:icmc1234@gns3.m7.rs/v2"

project = get_project(SERVER, "pocpoc")

router0 = get_node(SERVER, project, "R0", {
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
            ipv6 unicast-routing
            ipv6 router ospf 1
                router-id 10.0.0.0
            exit
            # lado conectado no roteador 1
            interface fastethernet 0/0
                ipv6 enable
                ipv6 ospf 1 area 0
                ipv6 address 2001:0:1::1/64
                no shutdown
            exit
            # lado conectado no roteador 2
            interface fastethernet 0/1
                ipv6 enable
                ipv6 ospf 1 area 0
                ipv6 address 2001:0:2::1/64
                no shutdown
            exit
        """,
    }
}, destroy=True)
start_node(SERVER, project, router0)

router1 = get_node(SERVER, project, "R1", {
    "compute_id": "local",
    "node_type": "dynamips",
    "x": -100,
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
            ipv6 unicast-routing
            ipv6 router ospf 1
                router-id 10.0.0.1
            exit

            interface fastethernet 0/0
                ipv6 enable
                ipv6 ospf 1 area 0
                ipv6 address 2001:0:1::2/64
                no shutdown
            exit

            interface fastethernet 0/1
                ipv6 enable
                ipv6 ospf 1 area 1
                ipv6 address 2001:1:1::1/64
                no shutdown
            exit
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
            ipv6 unicast-routing
            ipv6 router ospf 1
                router-id 10.0.0.2
            exit

            # lado conectado no roteador 0
            interface fastethernet 0/0
                ipv6 enable
                ipv6 ospf 1 area 0
                ipv6 address 2001:0:2::2/64
                no shutdown
            exit

            # lado conectado no switch
            interface fastethernet 0/1
                ipv6 enable
                ipv6 ospf 1 area 2
                ipv6 address 2001:2:1::1/64
                no shutdown
            exit
        """,
    }
}, destroy=True)
start_node(SERVER, project, router2)

link_nodes(SERVER, project, router0, 0, router1, 0)
link_nodes(SERVER, project, router0, 1, router2, 0)


alpine1 = get_node(SERVER, project, "alpine-linux-docker1", {
    "compute_id": "local",
    "node_type": "docker",
    "x": -100,
    "y": 100,
    "properties": {
        "image": "alpine",
        "console_type": "telnet",
    }
}, destroy=True)
start_node(SERVER, project, alpine1)
link_nodes(SERVER, project, router1, 1, alpine1, 0)

alpine2 = get_node(SERVER, project, "alpine-linux-docker2", {
    "compute_id": "local",
    "node_type": "docker",
    "x": 100,
    "y": 100,
    "properties": {
        "image": "alpine",
        "console_type": "telnet",
    }
}, destroy=True)
start_node(SERVER, project, alpine2)
link_nodes(SERVER, project, router2, 1, alpine2, 0)

run_node_command(SERVER, project, router0, """
    enable
        configure terminal
            interface fastethernet 0/0
                no shutdown
            exit
            interface fastethernet 0/1
                no shutdown
            exit
        exit
    exit
""")
run_node_command(SERVER, project, router1, """
    enable
        configure terminal
            interface fastethernet 0/0
                no shutdown
            exit
            interface fastethernet 0/1
                no shutdown
            exit
        exit
    exit
""")
run_node_command(SERVER, project, router2, """
    enable
        configure terminal
            interface fastethernet 0/0
                no shutdown
            exit
            interface fastethernet 0/1
                no shutdown
            exit
        exit
    exit
""")

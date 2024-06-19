from common import Server

server = Server("https://admin:icmc1234@gns3.m7.rs/v2")

project = server.project("pocpoc")

router0 = project.node("R0", {
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
router0.start()

router1 = project.node("R1", {
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
router1.start()

router2 = project.node("R2", {
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
router2.start()

project.link_nodes(router0, 0, 0, router1, 0, 0)
project.link_nodes(router0, 0, 1, router2, 0, 0)

alpine1 = project.node("alpine-linux-docker1", {
    "compute_id": "local",
    "node_type": "docker",
    "x": -100,
    "y": 100,
    "properties": {
        "image": "alpine",
        "console_type": "telnet",
    }
}, destroy=True)
alpine1.start()
project.link_nodes(router1, 0, 1, alpine1, 0, 0)

alpine2 = project.node("alpine-linux-docker2", {
    "compute_id": "local",
    "node_type": "docker",
    "x": 100,
    "y": 100,
    "properties": {
        "image": "alpine",
        "console_type": "telnet",
    }
}, destroy=True)
alpine2.start()
project.link_nodes(router2, 0, 1, alpine2, 0, 0)

router0.run_command("""
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
router1.run_command("""
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
router2.run_command("""
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

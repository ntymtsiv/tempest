from tempest import clients

class Resources():


    tempest_resources = {}
    CLIENTS = { "router" : "network_client",
				"interface" : "network_client" 
			  }
    @classmethod
    def set_resource(cls, key, value): 
	   cls.tempest_resources[key] = value

    @classmethod
    def tearDownTempestResources(cls):
        for resource_id in cls.tempest_resources:
            if cls.tempest_resources[resource_id] == "router":
                cls.delete_router_secondary_tear_down(resource_id)
            elif cls.tempest_resources[resource_id] == "network" or cls.tempest_resources[resource_id] == "bulk_network":
                cls.delete_network_secondary_tear_down(resource_id)
            elif cls.tempest_resources[resource_id] == "health_monitor":
                cls.delete_health_monitor_secondary_tear_down(resource_id)
            elif cls.tempest_resources[resource_id] == "member":
                cls.delete_member_secondary_tear_down(resource_id)
            elif cls.tempest_resources[resource_id] == "vip":
                cls.delete_vip_secondary_tear_down(resource_id)
            elif cls.tempest_resources[resource_id] == "vpn_service":
                cls.delete_vpn_service_secondary_tear_down(resource_id)
            elif cls.tempest_resources[resource_id] == "pool":
                cls.delete_pool_secondary_tear_down(resource_id)
            elif cls.tempest_resources[resource_id] == "quota":
                cls.delete_quota_secondary_tear_down(resource_id)
            elif cls.tempest_resources[resource_id] == "subnet":
                cls.delete_subnet_secondary_tear_down(resource_id)
            elif cls.tempest_resources[resource_id] == "floating_ip":
                cls.delete_floating_ip_secondary_tear_down(resource_id)
            elif cls.tempest_resources[resource_id] == "security_group":
                cls.delete_secgroup_secondary_tear_down(resource_id) 
            elif cls.tempest_resources[resource_id] == "security_group_rule":
                cls.delete_secgroup_rule_secondary_tear_down(resource_id)
            elif cls.tempest_resources[resource_id] == "port":
                cls.delete_port_secondary_tear_down(resource_id)
            # elif cls.tempest_resources[resource_id] == "bulk_port":
            #     cls.delete_bulk_port_secondary_tear_down(resource_id)
            # elif cls.tempest_resources[resource_id] == "bulk_subnet":
            #     cls.delete_bulk_subnet_secondary_tear_down(resource_id)
            # elif cls.tempest_resources[resource_id] == "bulk_network":
            #     cls.delete_bulk_network_secondary_tear_down(resource_id)
	  	  # else
	  	  # 	 raise('Resource type not supported')
	  	  
    # @classmethod   				
    # def delete_network_ports(cls, network_id):	  	     
    # 	 client = cls.get_client("network_client")
    # 	 _, body = client.show_network(network_id) 
    # 	 subnet_ids = body["network"]['subnets']
    # 	 for subnet_id in subnet_ids:
    # 	 	_, body = client.show_subnet(subnet_id) 
    # 	 	print body

    @classmethod   				
    def delete_router_secondary_tear_down(cls, router_id):
	   client = cls.get_client("network_client")
	   try:
	      if cls not in cls.list_router:
	      	raise AttributeError()	 
	   except AttributeError:
	      cls.router_list = []
	      #remove handling when in NetworkClientXML will be method list_routers()
	      try:
	          status_code, body =cls.client.list_routers()
	      except AttributeError:
	          os = clients.Manager(interface='json')
	          client = os.network_client
	          status_code, body = client.list_routers()
	      cls.router_list = cls.get_list_from_body(body["routers"])
	      cls.router_list.append(cls)
	   if router_id in cls.router_list:
	      cls.remove_router_interfaces(router_id)
	      client.delete_router(router_id)

    @classmethod   				
    def delete_port_secondary_tear_down(cls, port_id):
	   client = cls.get_client("network_client")
	   try:
	      if cls not in cls.port_list:
	      	raise AttributeError()	 
	   except AttributeError:
	      cls.port_list = []
	      status_code, body = cls.client.list_ports()
	      cls.port_list  = cls.get_list_from_body(body["ports"])
	      cls.port_list.append(cls)
	   if port_id in cls.port_list:
	      client.delete_port(port_id) 

    @classmethod   				
    def delete_floating_ip_secondary_tear_down(cls, floating_ip_id):
	   client = cls.get_client("network_client")
	   try:
	      if cls not in cls.floating_ip_list:
	      	raise AttributeError()	 
	   except AttributeError:
	      cls.floating_ip_list = []
	      status_code, body = cls.client.list_floating_ips()
	      cls.floating_ip_list  = cls.get_list_from_body(body["floatingips"])
	      cls.floating_ip_list.append(cls)
	   if floating_ip_id in cls.floating_ip_list:
	      client.delete_floating_ip(floating_ip_id) 


    @classmethod   				
    def delete_network_secondary_tear_down(cls, network_id):
	   client = cls.get_client("network_client")
	   try:
	      if cls not in cls.list_network:
	      	raise AttributeError()	 
	   except AttributeError:
	      cls.network_list = []
	      status_code, body = cls.client.list_networks()
	      cls.network_list  = cls.get_list_from_body(body["networks"])
	      cls.network_list.append(cls)
	   if network_id in cls.network_list:
	      cls.remove_floating_ips()
	#      cls.delete_network_ports(network_id)
	      client.delete_network(network_id)     

    @classmethod   				
    def delete_health_monitor_secondary_tear_down(cls, health_monitor_id):
	   client = cls.get_client("network_client")
	   try:
	      if cls not in cls.list_health_monitor:
	      	raise AttributeError()	 
	   except AttributeError:
	      cls.health_monitor_list = []
	      status_code, body = cls.client.list_health_monitors()
	      cls.health_monitor_list  = cls.get_list_from_body(body["health_monitors"])
	      cls.health_monitor_list.append(cls)
	   if health_monitor_id in cls.network_list:
	      client.delete_health_monitor(health_monitor_id)

    @classmethod   				
    def delete_member_secondary_tear_down(cls, member_id):
	   client = cls.get_client("network_client")
	   try:
	      if cls not in cls.list_member:
	      	raise AttributeError()	 
	   except AttributeError:
	      cls.member_list = []
	      status_code, body = cls.client.list_members()
	      cls.member_list  = cls.get_list_from_body(body["members"])
	      cls.member_list.append(cls)
	   if member_id in cls.member_list:
	      client.delete_member(member_id)

    @classmethod   				
    def delete_vip_secondary_tear_down(cls, vip_id):
	   client = cls.get_client("network_client")
	   try:
	      if cls not in cls.list_vip:
	      	raise AttributeError()	 
	   except AttributeError:
	      cls.vip_list = []
	      status_code, body = cls.client.list_vips()
	      cls.vip_list  = cls.get_list_from_body(body["vips"])
	      cls.vip_list.append(cls)
	   if vip_id in cls.vip_list:
	      client.delete_vip(vip_id)

    @classmethod   				
    def delete_pool_secondary_tear_down(cls, pool_id):
	   client = cls.get_client("network_client")
	   try:
	      if cls not in cls.list_pool:
	      	raise AttributeError()	 
	   except AttributeError:
	      cls.pool_list = []
	      status_code, body = cls.client.list_pools()
	      cls.pool_list  = cls.get_list_from_body(body["pools"])
	      cls.pool_list.append(cls)
	   if pool_id in cls.pool_list:
	      client.delete_pool(pool_id)

    @classmethod   				
    def delete_vpn_service_secondary_tear_down(cls, vpn_service_id):
	   client = cls.get_client("network_client")
	   try:
	      if cls not in cls.list_vpn_service:
	      	raise AttributeError()	 
	   except AttributeError:
	      cls.vpn_service_list = []
	      status_code, body =cls.client.list_vpn_services()
	      cls.vpn_service_list = cls.get_list_from_body(body["vpn_services"])
	      cls.vpn_services_list.append(cls)
	   if vpn_service_id in cls.vpn_service_list:
	      client.delete_vpn_service(vpn_service_id)  

    @classmethod   				
    def delete_quota_secondary_tear_down(cls, quota_id):
	   client = cls.get_client("network_client")
	   try:
	      if cls not in cls.quota_list:
	      	raise AttributeError()	 
	   except AttributeError:
	      cls.quota_list = []
	      status_code, body =cls.client.list_quotas()
	      cls.quota_list = cls.get_list_from_body(body["quotas"])
	      cls.quota_list.append(cls)
	   if quota_id in cls.quota_list:
	      client.delete_quota(quota_id)  

    @classmethod   				
    def delete_subnet_secondary_tear_down(cls, subnet_id):
	   client = cls.get_client("network_client")
	   try:
	      if cls not in cls.subnet_list:
	      	raise AttributeError()	 
	   except AttributeError:
	      cls.subnet_list = []
	      status_code, body =cls.client.list_subnets()
	      cls.subnet_list = cls.get_list_from_body(body["subnets"])
	      cls.subnet_list.append(cls)
	   if subnet_id in cls.subnet_list:
	      client.delete_subnet(subnet_id)  

    @classmethod   				
    def delete_secgroup_secondary_tear_down(cls, security_group_id): 
	   client = cls.get_client("network_client")
	   try:
	      if cls not in cls.secgroup_list:
	      	raise AttributeError()
	   except AttributeError:
	      cls.secgroup_list = []
	      status_code, body = cls.client.list_security_groups()
	      cls.secgroup_list = cls.get_list_from_body(body["security_groups"])
	      cls.secgroup_list.append(cls)
	   if security_group_id in cls.secgroup_list:
	      client.delete_security_group(security_group_id) 

    @classmethod   				
    def delete_secgroup_rule_secondary_tear_down(cls, secgroup_rule_id): 
	   client = cls.get_client("network_client")
	   try:
	      if cls not in cls.secgroup_rule_list:
	      	raise AttributeError()	      
	   except AttributeError:
	      cls.secgroup_rule_list = []
	      status_code, body = cls.client.list_security_group_rules()
	      cls.secgroup_rule_list = cls.get_list_from_body(body["security_group_rules"])
	      cls.secgroup_rule_list.append(cls)
	   if secgroup_rule_id in cls.secgroup_rule_list:
	      client.delete_security_group_rule(secgroup_rule_id) 

    @classmethod 
    def get_list_from_body(cls, resource_body):
	  resource_list = []
	  for b in resource_body:
	     resource_list.append(b["id"])
	  return resource_list

    @classmethod
    def get_client(cls, client_name):
	  os = clients.Manager(interface=cls._interface)
	  cls.network_cfg = os.config.network
	  if client_name == 'network_client':
	  	return os.network_client

#TODO: add teardown after fail in floating_ip tests
    @classmethod  
    def remove_floating_ips(cls):
		client = cls.get_client("network_client") 
		status_code, body = client.list_floating_ips()
		floating_ip_list  = cls.get_list_from_body(body["floatingips"])
		for floating_ip in floating_ip_list:
			client.delete_floating_ip(floating_ip)
			# if floating_ip in cls.tempest_resources:
			# 	del cls.tempest_resources[floating_ip]

    @classmethod  
    def remove_router_interfaces(cls, router_id):
		client = cls.get_client("network_client")         
		cls.remove_floating_ips()
		resp, body = client.list_router_interfaces(router_id)
		interfaces = body['ports']
		for i in interfaces:
			client.remove_router_interface_with_subnet_id(router_id, i['fixed_ips'][0]['subnet_id'])
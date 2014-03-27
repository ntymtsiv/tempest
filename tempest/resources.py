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
            elif cls.tempest_resources[resource_id] == "network":
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
            elif cls.tempest_resources[resource_id] == "security_group":
                cls.delete_secgroup_secondary_tear_down(resource_id) 
            elif cls.tempest_resources[resource_id] == "security_group_rule":
                cls.delete_secgroup_rule_secondary_tear_down(resource_id)
            elif cls.tempest_resources[resource_id] == "bulk_port":
                pass
            elif cls.tempest_resources[resource_id] == "bulk_subnet":
                pass
            elif cls.tempest_resources[resource_id] == "bulk_network":
                pass
	  	  # else
	  	  # 	 raise('Resource type not supported')
	  	     

    @classmethod   				
    def delete_router_secondary_tear_down(cls, router_id):
	   client = cls.get_client("network_client")
	   try:
		  cls.router_list
	   except AttributeError:
	      cls.router_list = []
	      status_code, body =cls.client.list_routers()
	      cls.router_list = cls.get_list_from_body(body["routers"])
	   if router_id in cls.router_list:
	      remove_router_interfaces(router_id)
	      client.delete_router(router_id)     

    @classmethod   				
    def delete_network_secondary_tear_down(cls, network_id):
	   client = cls.get_client("network_client")
	   try:
		     cls.network_list
	   except AttributeError:
	      cls.network_list = []
	      status_code, body = cls.client.list_networks()
	      cls.network_list  = cls.get_list_from_body(body["networks"])
	   if network_id in cls.network_list:
	      client.delete_network(network_id)     

    @classmethod   				
    def delete_health_monitor_secondary_tear_down(cls, health_monitor_id):
	   client = cls.get_client("network_client")
	   try:
		  cls.health_monitor_list
	   except AttributeError:
	      cls.health_monitor_list = []
	      status_code, body = cls.client.list_health_monitors()
	      cls.health_monitor_list  = cls.get_list_from_body(body["health_monitors"])
	   if health_monitor_id in cls.network_list:
	      client.delete_health_monitor(health_monitor_id)

    @classmethod   				
    def delete_member_secondary_tear_down(cls, member_id):
	   client = cls.get_client("network_client")
	   try:
		  cls.member_list
	   except AttributeError:
	      cls.member_list = []
	      status_code, body = cls.client.list_members()
	      cls.member_list  = cls.get_list_from_body(body["members"])
	   if member_id in cls.member_list:
	      client.delete_member(member_id)

    @classmethod   				
    def delete_vip_secondary_tear_down(cls, vip_id):
	   client = cls.get_client("network_client")
	   try:
		  cls.vip_list
	   except AttributeError:
	      cls.vip_list = []
	      status_code, body = cls.client.list_vips()
	      cls.vip_list  = cls.get_list_from_body(body["vips"])
	   if vip_id in cls.vip_list:
	      client.delete_vip(vip_id)

    @classmethod   				
    def delete_pool_secondary_tear_down(cls, pool_id):
	   client = cls.get_client("network_client")
	   try:
		  cls.pool_list
	   except AttributeError:
	      cls.pool_list = []
	      status_code, body = cls.client.list_pools()
	      cls.pool_list  = cls.get_list_from_body(body["pools"])
	   if pool_id in cls.pool_list:
	      client.delete_pool(pool_id)

    @classmethod   				
    def delete_vpn_service_secondary_tear_down(cls, vpn_service_id):
	   client = cls.get_client("network_client")
	   try:
		  cls.vpn_service_list
	   except AttributeError:
	      cls.vpn_service_list = []
	      status_code, body =cls.client.list_vpn_services()
	      cls.vpn_service_list = cls.get_list_from_body(body["vpn_services"])
	   if vpn_service_id in cls.vpn_service_list:
	      client.delete_vpn_service(vpn_service_id)  

    @classmethod   				
    def delete_quota_secondary_tear_down(cls, quota_id):
	   client = cls.get_client("network_client")
	   try:
		  cls.quota_list
	   except AttributeError:
	      cls.quota_list = []
	      status_code, body =cls.client.list_quotass()
	      cls.quota_list = cls.get_list_from_body(body["quotas"])
	   if quota_id in cls.quota_list:
	      client.delete_quota(quota_id)  

    @classmethod   				
    def delete_subnet_secondary_tear_down(cls, subnet_id):
	   client = cls.get_client("network_client")
	   try:
		  cls.subnet_list
	   except AttributeError:
	      cls.subnet_list = []
	      status_code, body =cls.client.list_subnets()
	      cls.subnet_list = cls.get_list_from_body(body["subnets"])
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
	      cls.secgroup_rule_list
	   except AttributeError:
	      cls.secgroup_rule_list = []
	      status_code, body = cls.client.list_security_group_rules()
	      cls.secgroup_rule_list = cls.get_list_from_body(body["security_group_rules"])
	   if secgroup_rule_id in cls.secgroup_rule_list:
	      client.delete_security_group_rule(secgroup_rule_id) 
	      cls.secgroup_rule_list.remove(secgroup_rule_id)

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

    def remove_router_interfaces(self, router_id):
		client = get_client("interface")               
		resp, body = client.list_router_interfaces(router_id)
		interfaces = body['ports']
		for i in interfaces:
			client.remove_router_interface_with_subnet_id(router_id, i['fixed_ips'][0]['subnet_id'])
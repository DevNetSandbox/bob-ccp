import json
import requests
requests.packages.urllib3.disable_warnings()

def login(ccp, user, password):
    s = requests.session()
    s.headers = {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
    }
    url = 'https://{0}/2/system/login/'.format(ccp)
    data = 'username={0}&password={1}'.format(user, password)
    print(data)
    r = s.post(url, data=data, verify=False)
    print(r.text)
    return s

def get_cluster_para(session, ccp):
    s = session
    s.headers = {
         "Content-Type":"application/json"
    }

    #privder uuid
    url = 'https://{0}/2/providerclientconfigs/'.format(ccp)
    r = s.get(url, verify=False)
    response = json.loads(r.text)
    provider_uuid = response[0]['uuid']

    #network uuid
    url = 'https://{0}/2/network_service/subnets/'.format(ccp)
    r = s.get(url, verify=False)
    response = json.loads(r.text)
    network_uuid = response[0]['uuid']
    print('provide_rclient_uuid={0},network_uuid={1}'.format(provider_uuid, network_uuid))

    return (provider_uuid, network_uuid)

def delete_cluster(session, ccp, cluster_name):
    url = 'https://{0}/2/clusters/'.format(ccp)
    s = session
    r = s.get(url, verify = False)
    response = json.loads(r.text)
    uuid = ''
    for cluster in response:
        print(cluster['name'], cluster['uuid'])
        if cluster['name'] == cluster_name:
            uuid = cluster['uuid']
            break
    if uuid!='':
        print('deleting cluster {0}...'.format(uuid))
        url = 'https://{0}/2/clusters/{1}'.format(ccp, uuid)
        r = s.delete(url, verify= False)
        print('deleted')
    else:
        print('cluster {0} is not found'.format(cluster_name))



def new_cluster(session, ccp, provider_uuid, network_uuid, cluster_name):
    url = 'https://{0}/2/clusters/'.format(ccp)
    name = cluster_name.lower()
    data = {
    "is_harbor_enabled":False,
    "provider_client_config_uuid":provider_uuid,
    "name":name,
    "kubernetes_version":"1.14.8",
    "ssh_key":"ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINksnIyqCWNUdHoXx3G8PVg8Z9tWnSGGI/r2F/REwh3a gitlab",
    "description":"Cluster created via API",
    "datacenter":"CCP",
    "cluster":"CCP",
    "resource_pool":"CCP/Resources",
    "networks":["VMNetwork"],
    "datastore":"CCPDatastore",
    "storage_class":"vsphere",
    "workers":1,
    "ssh_user":"ccpuser",
    "type":1,
    "masters":1,
    "deployer_type":"kubeadm",
    "ingress_vip_pool_id":network_uuid,
    "load_balancer_ip_num":4,
    "is_istio_enabled":False,
    "registries_root_ca":[""],
    "aws_iam_enabled":False,
    "aws_iam_role_arn":"",
    "worker_node_pool":{
        "vcpus":2,
        "memory":16384,
        "template":"ccp-tenant-image-1.14.8-ubuntu18-5.1.0"
    },
    "master_node_pool":{
        "vcpus":2,
        "memory":16384,
        "template":"ccp-tenant-image-1.14.8-ubuntu18-5.1.0"
    },
    "node_ip_pool_id":network_uuid,
    "network_plgin":{
        "name":"calico",
        "status":"",
        "details":"{\"pod_cidr\":\"192.168.0.0/16\"}"},
        "deployer":{
            "proxy_cmd":"StrictHostKeyChecking no\nHost 15.29.3?.* !15.29.30.* !15.29.31.*\n ProxyCommand nc --proxy 10.193.231.10:8111 --proxy-type socks4 %h %p",
            "provider_type":"vsphere",
            "provider":{
                "vsphere_datacenter":"CCP",
                "vsphere_datastore":"CCPDatastore",
                "vsphere_client_config_uuid":provider_uuid,
                "vsphere_working_dir":"/CCP/vm"
            }
        }
    }
    s = session
    r = s.post(url, json=data, verify=False, timeout=600)
    response = json.loads(r.text)
    print(response)

if __name__ == "__main__":
    with open('./config.json','r') as f:
        contents = f.read()
        configs = json.loads(contents)
        print('1. Login')
        session = login(configs['CCP_HOST'], configs['CCP_USER'], configs['CCP_PASSWORD'])
        print('2. Get Provider details')
        (provider, network) = get_cluster_para(session, configs['CCP_HOST'])
        print('3. Create new cluster, it requires time...')
        new_cluster(session,  configs['CCP_HOST'], provider, network, 'test-cluster')
        print('4. Delete the cluster last created')
        delete_cluster(session,  configs['CCP_HOST'], 'test-cluster')


	  
 

CCP_HOST='10.10.20.110'
CCP_PASSWORD='Cisco123'
curl -X POST --header 'Content-Type: application/x-www-form-urlencoded' --header 'Accept: application/json' -d "username=admin&password=$CCP_PASSWORD" "https://$CCP_HOST/2/system/login/" -k -c cookie.txt
#grab cluster uuid
CLUSTER_UUID=$(curl -sk -b cookie.txt -H "Content-Type:application/json" https://$CCP_HOST/2/clusters/ | jq '.[].uuid' | sed "s/^\([\"']\)\(.*\)\1\$/\2/g")
curl -sk -b cookie.txt https://$CCP_HOST/2/clusters/$CLUSTER_UUID/env -o kubeconfig.yaml
echo "kubeconfig file is saved to  kubeconfig.yaml, use export KUBECONFIG=./kubeconfig.yaml to refer it"
export KUBECONFIG=./kubeconfig.yaml

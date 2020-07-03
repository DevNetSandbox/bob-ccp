CCP_HOST='10.10.20.110'
CCP_PASSWORD='Cisco123'
curl -X POST --header 'Content-Type: application/x-www-form-urlencoded' --header 'Accept: application/json' -d "username=admin&password=$CCP_PASSWORD" "https://$CCP_HOST/2/system/login/" -k -c cookie.txt
curl -sk -b cookie.txt -H "Content-Type:application/json" https://$CCP_HOST/2/providerclientconfigs/ | jq '.[].uuid'

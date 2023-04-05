import shodan
import json
import sys
from tqdm import tqdm

# Initialize the api
API_KEY = ''
api = shodan.Shodan(API_KEY)

# Check to see if arguements exist
try:  
    input_file = sys.argv[1]
    output_file = sys.argv[2]
except IndexError:
    print('Missing arguments!\nExample usage: python3 shodan_host.py [input file] [output file]')
    sys.exit(1) 

try:
    # Open and read a file containing ip addresses 
    with open(input_file, 'r') as f:
        IP_SET = f.read().split('\n')
    
    # Remove all empty entries from IP_SET list
    for index,IP in enumerate(IP_SET):    
        if IP_SET[index] == '':
            del IP_SET[index]
    
    # Check each IP in IP_SET against the Shodan database   
    ip_dict = {}
    for ip_count,IP in enumerate(tqdm(IP_SET), start=1):
        try:
            host = api.host(IP)        
            
            # Parse data                
            ip = host['ip_str']
            org = host.get('org', 'n/a')
            os = host.get('os', 'n/a')
            
            # Add parsed data to ip_dict
            ip_dict.update({'IP' + str(ip_count): {'ip': ip, 'org': org, 'os': os}})
        
        # Write 'NO DATA' into ip_dict if there is not data in shodan
        except shodan.APIError as e:
            ip_dict.update({'IP' +str(ip_count): '{} : NO DATA'.format(IP)})
            continue
        
    # dump contents of ip_dict into 'shodan.json'
    with open(output_file, 'w') as outfile:
        json.dump(ip_dict, outfile)
                
except shodan.APIError as e:
    print('Error: {}'.format(e))

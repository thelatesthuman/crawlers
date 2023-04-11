import shodan
import csv
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
    ip_list = []
    org_list = []
    os_list = []
    for ip_count,IP in enumerate(tqdm(IP_SET), start=1):
        try:
            host = api.host(IP)        
            
            # Parse data                
            ip = host['ip_str']
            org = host.get('org', 'n/a')
            os = host.get('os', 'n/a')
            
            # Add parsed data to their respective lists
            ip_list.append(ip)
            org_list.append(org)
            os_list.append(os)
         
        # Write 'NO DATA' if there is not data in shodan
        except shodan.APIError as e:
            ip_list.append('NO DATA')
            org_list.append('NO DATA')
            os_list.append('NO DATA')
            continue
        
    # Format data into .csv format
    host_tuples = list(zip(ip_list, org_list, os_list))
    fields = ['IP', 'Organization', 'OS']
    with open(output_file, 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fields)
        writer.writeheader()
        for host_tuple in host_tuples:
            ip_dict = {'IP': host_tuple[0]}
            org_dict = {'Organization': host_tuple[1]}
            os_dict = {'OS': host_tuple[2]}
            writer.writerow({**ip_dict, **org_dict, **os_dict})        
except shodan.APIError as e:
    print('Error: {}'.format(e))

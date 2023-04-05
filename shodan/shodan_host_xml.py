import shodan
import sys
import xml.etree.ElementTree as ET
from tqdm import tqdm

# Initialize the api
API_KEY = ''
api = shodan.Shodan(API_KEY)

# Initialize ElementTree by creating root
root = ET.Element('hosts')

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
    
    # Remove any empty entries from the list 
    for index,IP in enumerate(IP_SET):
        if IP == '':
            del IP_SET[index]

    # Check each IP in IP_SET against the Shodan database   
    for ip_count,IP in enumerate(tqdm(IP_SET), start=1):
        try:
            host = api.host(IP)        
            
            # Parse data                
            ip = host['ip_str']
            org = host.get('org', 'n/a')
            os = host.get('os', 'n/a')
            
            # Format data into ElementTree
            host_elem = ET.SubElement(root, 'host')
            ip_elem = ET.SubElement(host_elem, 'ip')
            org_elem = ET.SubElement(host_elem, 'org')
            os_elem = ET.SubElement(host_elem, 'os')
            ip_elem.text = ip
            org_elem.text = org
            os_elem.text = os
            
     
        # Write 'NO DATA' into ElementTree if there is no data in shodan
        except shodan.APIError as e:
            host_elem = ET.SubElement(root, 'host')
            ip_elem = ET.SubElement(host_elem, 'ip')
            ip_elem.text = '{} : NO DATA'.format(IP)
            continue
        
    # dump contents of ET into xml file
    tree = ET.ElementTree(root)
    tree.write(output_file)
                
except shodan.APIError as e:
    print('Error: {}'.format(e))

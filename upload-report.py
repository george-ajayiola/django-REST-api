import requests
import sys
import os

file_name = sys.argv[1]
scan_type = ''

if file_name == 'gitleaks.json':
    scan_type = 'Gitleaks Scan'
elif file_name == 'trivy-results.sarif':
    scan_type = 'SARIF'
elif file_name == 'semgrep.json':
    scan_type = 'Semgrep JSON Report'

# Fetch token from environment variable
token = os.getenv('DEFECT_DOJO_TOKEN')
if not token:
    raise ValueError("DEFECT_DOJO_TOKEN is not set")

headers = {
    'Authorization': f'Token {token}'
}

url = 'http://74.179.80.149:8080/api/v2/import-scan/'

data = {
    'active': True,
    'verified': True,
    'scan_type': scan_type,
    'minimum_severity': 'Low',
    'engagement': 1
}

with open(file_name, 'rb') as f:
    files = {'file': f}
    response = requests.post(url, headers=headers, data=data, files=files)

if response.status_code == 201:
    print('Scan results imported successfully')
else:
    print(f'Failed to import scan results: {response.content}')

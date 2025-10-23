import requests
import time
import dotenv
import os

dotenv.load_dotenv()

def fetch_ipv4():
    response = requests.get('https://api.ipify.org?format=json')
    return response.json()['ip']

def save_ipv4(ip):
    with open('ipv4.txt', 'w') as file:
        file.write(ip)

def load_ipv4():
    try:
        with open('ipv4.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def get_dns_record_id(zone_id, record_name, api_token):
    """Fetch the DNS record ID for a given record name."""
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    params = {
        "name": record_name,
        "type": "A"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['result']:
            return data['result'][0]['id']
        else:
            print(f"No A record found for {record_name}", flush=True)
            return None
    else:
        print(f"Failed to fetch DNS record for {record_name}: {response.text}", flush=True)
        return None

def update_dns_record(zone_id, dns_id, record_name, ip, api_token):
    """Update a single DNS record."""
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{dns_id}"
    headers = {
        "Authorization": f"Bearer {api_token}", 
        "Content-Type": "application/json"
    }
    data = {
        "content": ip,
    }

    response = requests.patch(url, json=data, headers=headers)

    if response.status_code == 200:
        print(f"DNS record updated: {record_name} -> {ip}", flush=True)
    else:
        print(f"Failed to update {record_name}: {response.text}", flush=True)

def update_all_dns_records(ip):
    """Update all configured DNS records."""
    api_token = os.getenv('CLOUDFLARE_API_TOKEN')
    zone_id = os.getenv('CLOUDFLARE_ZONE_ID')
    dns_names = os.getenv('CLOUDFLARE_DNS_NAMES', '').split(',')

    # Strip whitespace from names
    dns_names = [name.strip() for name in dns_names if name.strip()]

    if not dns_names:
        print("No DNS names configured in CLOUDFLARE_DNS_NAMES", flush=True)
        return

    for record_name in dns_names:
        dns_id = get_dns_record_id(zone_id, record_name, api_token)
        if dns_id:
            update_dns_record(zone_id, dns_id, record_name, ip, api_token)
        else:
            print(f"Skipping {record_name} - could not find record", flush=True)

if __name__ == "__main__":
    while True:
        ip = fetch_ipv4()
        old_ip = load_ipv4()

        if ip != old_ip:
            print(f"IP changed from {old_ip} to {ip}", flush=True)
            save_ipv4(ip)
            update_all_dns_records(ip)

        time.sleep(10)

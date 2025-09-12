import requests
import time
import dotenv
import os

dotenv.load_dotenv()

def fetch_ipv4():
    response = requests.get('https://api.ipify.org?format=json')
    return response.json()['ip']

def save_ipv4(ip):
    ipv4 = ip 
    with open('ipv4.txt', 'w') as file:
        file.write(ipv4)

def load_ipv4():
    try:
        with open('ipv4.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def update_dns_record(ip):
    dns_id = os.getenv('CLOUDFLARE_DNS_ID')
    api_token = os.getenv('CLOUDFLARE_API_TOKEN')
    zone_id = os.getenv('CLOUDFLARE_ZONE_ID')
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
        print(f"DNS record updated to {ip}", flush=True)
    else:
        print(f"Failed to update DNS record: {response.text}", flush=True)

if __name__ == "__main__":
    while True:
        ip = fetch_ipv4()
        old_ip = load_ipv4()

        if ip != old_ip:
            print(f"IP changed from {old_ip} to {ip}", flush=True)
            save_ipv4(ip)
            update_dns_record(ip)

        time.sleep(10)

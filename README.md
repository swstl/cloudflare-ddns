# How to run - docker compose
```yaml
services:
  ddns:
    build: .
    env_file: .env
    restart: unless-stopped
    volumes:
      - ddns_state:/data

volumes:
  ddns_state:
```

```bash
docker compose up -d
```


From:
`https://developers.cloudflare.com/api/resources/dns/subresources/records/methods/update/`

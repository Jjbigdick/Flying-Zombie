# Flying-Zombie 

Cloud-Based Distributed Platform for Bypassing Enterprise Bot Detection

Scalable system automating interactions with bot-protected platforms (Cloudflare, Facebook) using managed browser instances.
Key Features

    Bot Detection Evasion:
        Successfully bypasses Cloudflare (5s challenge), Tinder Swiper, and Bet365 anti-scraping.
        Uses virtual displays (Xvfb) for undetectable browser rendering in cloud environments.
    Distributed Architecture:
        API Gateway: AsyncIO server with JWT authentication, IP whitelisting, and raw HTTP validation (blocks 99% malicious payloads).
        Workers: 10+ concurrent Selenium/Playwright instances (Chrome/Firefox) managed via multiprocessing.
    Security & Stability:
        SQL-based IP failure tracking (auto-block after 10 violations).
        Request rate limiting, randomized user-agent/viewport rotation.

Technical Architecture

1. Client Request → JWT Auth → Task Queue  
2. Worker Nodes:  
   - Virtual Display (Xvfb) → Chrome/Firefox → Human-like Interactions  
3. Anti-Detection:  
   - Viewport randomization  
   - Request throttling (simulate organic traffic)  
4. Response → Parsed HTML/API Data  

Deployment

    API: Flask + Gunicorn (4 workers, 12 threads).
    Infrastructure: Deployed on DigitalOcean (Ubuntu 22.04 + Xvfb).
    Scaling: Dockerized nodes with Redis task distribution.

Usage Example

import requests

# Bypass Cloudflare protection  
response = requests.post(
    "https://api.flying-zombie.com/v1/scrape",
    headers={"Authorization": "Bearer YOUR_JWT"},
    json={
        "url": "https://target-site.com",
        "action": "extract_data",
        "viewport_size": "1920x1080"
    }
)
print(response.json())  # Returns HTML + bypass metadata

![image](https://github.com/user-attachments/assets/75fd4969-15c9-4352-89fb-495f0566e222)

•	Architecture:
   - API Gateway: AsyncIO server handling JWT authentication, IP whitelisting, and raw HTTP socket validation to block malicious payloads.
   - Worker Orchestration: Managed 8+ concurrent headless browser instances (multiprocessing) to execute tasks (scraping, interactions) with 95% success rate against anti-bot systems.
   - Security Layer: Rate limiting, SQL-based IP failure tracking (block after 10 failures), and request parsing for server stability.  

•	Deployment: Exposed via Flask/Gunicorn REST API, and hosted on DigitalOcean for high availability.







Cloudflare:

![image](https://github.com/user-attachments/assets/a738e54e-3a46-4a38-b711-55878b1db190)


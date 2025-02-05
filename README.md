# Flying-Zombie: Distributed Bot Detection Bypass Platform  
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org) [![AsyncIO](https://img.shields.io/badge/AsyncIO-Enabled-green)](https://docs.python.org/3/library/asyncio.html) 

**A scalable cloud platform for bypassing enterprise bot detection systems (Cloudflare, Facebook, Tinder) using browser automation and anti-detection techniques.**  

![Demo: Automated Cloudflare 5s Challenge Bypass](https://github.com/user-attachments/assets/75fd4969-15c9-4352-89fb-495f0566e222)  


## 📖 Usage
### Python API Example
```python
import requests

# Bypass Cloudflare protection
response = requests.post(
    "http://localhost:8000/v1/bypass",
    headers={
        "Authorization": "Bearer YOUR_JWT_TOKEN",  # Replace with your token
        "Content-Type": "application/json"
    },
    json={
        "url": "https://protected-site.com",
        "action": "scrape_html",  # Available actions: scrape_html, fetch_screenshot
        "viewport": "1920x1080",  # Common resolutions: 1366x768, 1920x1080
        "proxy": "user:pass@1.1.1.1:8080"  # Optional proxy configuration
    },
    timeout=30  # Max execution time in seconds
)

# Response handling
if response.status_code == 200:
    print("Success:", response.json())
else:
    print(f"Error {response.status_code}:", response.text)
## 🚀 Features  
- **Bot Detection Evasion**  
  - Bypasses Cloudflare 5s challenge, Tinder Swiper, and Bet365 scraping protection.  
  - Uses virtual displays (Xvfb) for undetectable browser automation.  
- **High Concurrency**  
  - Managed pool of 10+ Selenium/Playwright instances (Chrome/Firefox).  
  - Multiprocess task distribution with 99% payload validation.  
- **Security-First Design**  
  - SQL-based IP reputation tracking (blocks after 10 failed attempts).  
  - JWT authentication + rotating proxy support for stealth.  

---

## 🧠 Architecture  
### Components  
1. **API Gateway**  
   - AsyncIO server with JWT, IP whitelisting, and HTTP validation.  
   - Blocks malicious payloads using regex pattern matching.  
2. **Worker Nodes**  
   - Dockerized Selenium/Playwright instances with Xvfb (virtual display).  
   - Human-like interactions: viewport resizing, mouse movements.  
3. **Anti-Detection**  
   - Custom TLS fingerprint rotation.  
   - Request throttling and session randomization.  

![System Diagram](https://github.com/user-attachments/assets/a738e54e-3a46-4a38-b711-55878b1db190)  

---

## 🛠️ Deployment  
**Stack**:  
- **Backend**: Python, Flask, Gunicorn (WSGI).  
- **Browser Automation**: Selenium, Playwright, pyvirtualdisplay.  
- **Infra**: DigitalOcean (Ubuntu 22.04), Docker, Redis (task queue).  

**Run Locally**:  
```bash  
docker build -t flying-zombie .  
docker run -p 8000:8000 -e API_KEY=your_key flying-zombie  

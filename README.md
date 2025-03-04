# Flying-Zombie: Distributed Bot Detection Bypass Platform  
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org) [![AsyncIO](https://img.shields.io/badge/AsyncIO-Enabled-green)](https://docs.python.org/3/library/asyncio.html) 

**API-Bound, Cloud-Based Distributed Platform. Managing 8+ Small Zombie Instances for Remote Data Farming and Bot-Detection Countering (Bet365, Facebook, Tinder, Cloudflare). Impelement ground-level HTTP socket checkers and SQL-based authentication for blocking malicious requests which further releasing system payload.**  

For persoanal interests only, user advised.

![Demo: Automated Cloudflare 5s Challenge Bypass](https://github.com/user-attachments/assets/75fd4969-15c9-4352-89fb-495f0566e222)  


## 📖 Usage
### Python API Example
```python
import requests

# Bypass Cloudflare protectiona
response = requests.post(
    "http://localhost:8000/v1/bypass",
    headers={
        "Authorization": "Bearer YOUR_JWT_TOKEN",  # Replace with your token
        "Content-Type": "application/json"
    },
    json={
        "url": "https://protected-site.com",
        "action": "scrape_html",  # Available actions: scrape_html, fetch_screenshot
        "proxy": "user:pass@1.1.1.1:8080"  # Optional proxy configuration
    },
    timeout=30  # Max execution time in seconds
)
```
### Response handling
```python
if response.status_code == 200:
    print("Success:", response.json())
else:
    print(f"Error {response.status_code}:", response.text)
```

### Response Structure
```json
{
  "status": "success",
  "html": "<html>...",  # Full page HTML after bypass
  "metrics": {...}      # Load times/fingerprint details
}
```
## 🚀 Features  
- **Bot Detection Evasion**  
  - Bypasses Cloudflare 5s challenge, Tinder Swiper, and Bet365 scraping protection.  
  - Uses virtual displays (Xvfb) for undetectable browser automation.
  - Rotating proxy support for stealth
- **Bot-Detection and Page Smart-Loading Mechanisms**
  - Dynamic determing if bot-detection evaded and page is loaded.
  - With a maximum 30s tiemr for server responses.
- **High Concurrency and dynamic Scalability**  
  - One distributed system handling a pool of 8+ Small Zombie instances (Chrome), depending on machine capability.  
  - Flask, Asyncio asynchornous handling requests.
- **Security-First Design**  
  - SQL-based IP reputation tracking (blocks after 10 failed attempts).
  - HTTP token filtering
- **User Firendly Design** 
  

---

## 🧠 Architecture  
### Components  
1. **API Gateway**  
   - AsyncIO server with JWT, IP whitelisting, and HTTP validation.  
   - Blocks malicious payloads using regex pattern matching.  
2. **Worker Nodes**  
   - Small Zombie instances with Xvfb (virtual display).  
   - Human-like interactions: viewport resizing, mouse movements.  
3. **Anti-Detection**  
   - Small Zombie Instances
   - Proxy Rotating via Proxy API

![System Diagram](https://github.com/user-attachments/assets/a738e54e-3a46-4a38-b711-55878b1db190)  

---

## 🛠️ Deployment  
**Stack**:  
**Concurrency & Scaling**:  
- AsyncIO (handles 150+ concurrent network requests)  
- Multiprocessing (isolates browser instances for stability)
- **Backend**: Python, Flask, Gunicorn (WSGI).  
- **Browser Automation**: Small Zombie, pyvirtualdisplay.  
- **Infra**: DigitalOcean (Ubuntu 22.04), Docker, Redis (task queue).  


---
## Small Zombie - DEMO
### Bet365 (Small Zombie Comparsion with Playwright)
https://streamable.com/lgpqvu
### Facebook
https://streamable.com/o2g281
### Cloudflare
https://streamable.com/b5xdjw

---
## Future Roadmap
- Desgin and tntegrated with ML Bot for dynamic handling page loading (which further improves loading time).
- Smart handling page loading such as detecting page loading status.

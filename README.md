# Flying-Zombie 

Cloud-based Scalable Bot-Detection Countering Platform

Cloud platform with Asyncio server, Worker Orchestration and custom automation framework (Small Zombie), automated farming website content by request command. Bypass enterprise bot-detection systems (Cloudflare, Facebook, Tinder, Bet365) with 95% success rate.

•	Architecture:

    o	API Gateway: AsyncIO server handling JWT authentication, IP whitelisting, and raw HTTP socket validation to block malicious payloads.  

    o	Worker Orchestration: Managed 8+ concurrent headless browser instances (multiprocessing) to execute tasks (scraping, interactions) with 95% success rate against anti-bot systems.

    o	Security: Rate limiting, SQL-based IP failure tracking (block after 10 failures), and request parsing for server stability.  

•	Deployment: Exposed via Flask/Gunicorn REST API, and hosted on DigitalOcean for high availability.

Sending Requests and getting content:

![image](https://github.com/user-attachments/assets/44cf2641-159c-493d-b549-5f492fae1bc3)


Cloud-based Headful Webdriver Pharsing (local view):

![image](https://github.com/user-attachments/assets/a738e54e-3a46-4a38-b711-55878b1db190)


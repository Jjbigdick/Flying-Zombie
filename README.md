# Flying-Zombie 

Cloud-based Scalable Bot-Detection Countering Platform

Designed and deployed a distributed cloud-based automation platform with custom automation framework (Small Zombie), to bypass enterprise bot-detection systems (Cloudflare, Facebook, Tinder, Bet365), achieveing 95% successe rate avoding detection.

•	Architecture:

    o	API Gateway: AsyncIO server handling JWT authentication, IP whitelisting, and raw HTTP socket validation to block malicious payloads.  

    o	Worker Orchestration: Managed 8+ concurrent headless browser instances (multiprocessing) to execute tasks (scraping, interactions) with 95% success rate against anti-bot systems.

    o	Security: Rate limiting, SQL-based IP failure tracking (block after 10 failures), and request parsing for server stability.  

•	Deployment: Exposed via Flask/Gunicorn REST API, and hosted on DigitalOcean for high availability.

Sending Requests:

![image](https://github.com/user-attachments/assets/1c0f8147-7de3-4544-a249-74eccc6cdf6b)

Getting Content:

![image](https://github.com/user-attachments/assets/377ba236-60ee-494f-8d2c-20f869235156)

Cloud-based Headful Webdriver Pharsing (luanching in local):

![image](https://github.com/user-attachments/assets/f393bd15-df53-47a6-80de-c89916fc9acb)


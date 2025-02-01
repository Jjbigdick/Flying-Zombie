# Flying-Zombie 

Cloud-based Scalable Bot-Detection Countering Platform

Designed and deployed a distributed cloud-based automation platform with custom automation framework (Small Zombie), to bypass enterprise bot-detection systems (Cloudflare, Facebook, Tinder, Bet365), achieveing 95% successe rate avoding detection.

•	Architecture:

    o	API Gateway: AsyncIO server handling JWT authentication, IP whitelisting, and raw HTTP socket validation to block malicious payloads.  

    o	Worker Orchestration: Managed 8+ concurrent headless browser instances (multiprocessing) to execute tasks (scraping, interactions) with 95% success rate against anti-bot systems.

    o	Security: Rate limiting, SQL-based IP failure tracking (block after 10 failures), and request parsing for server stability.  

•	Deployment: Exposed via Flask/Gunicorn REST API, and hosted on DigitalOcean for high availability.


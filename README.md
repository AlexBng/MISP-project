# Terrorism Data Scraper

This project is part of a university course on threat intelligence and aims to scrape data from online databases of terrorist groups and incidents using Python scripts. The collected data will be stored in [MISP objects](https://www.misp-project.org/objects.html), [MISP galaxies](https://www.misp-project.org/galaxy.html) or [taxonomies](https://www.misp-project.org/taxonomies.html) and then published on MISP.

## Progress

- 13/01/2023 : for the moment the script scrap.py is used to scrap the website [Global Terrorism Database](https://www.start.umd.edu/gtd/) with the libraries [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) and [requests](https://pypi.org/project/requests/). It stores the name of every terrorist groups (around 3000 groups) and the ids of their incidents. Then it stores separatly the characteristic of every incidents. Since I havn't that much informations about the terrorist groups, the idea is to first create a galaxy for the incidents and their characteristics in the "meta" field (including the group associated with it) and then i might scrap an other website to get more informations on the terrorist groups (and probably some synonyms of those groups name's) to create an other galaxy. From there I could use the "related" field to link the terrorist groups to their incidents and also use a taxonomie in the "tag" field to specify if the group claimed the responsability of the incident.

## Disclaimer

Please be aware that scraping data from online databases without permission may be against terms of service and may be illegal in some jurisdictions. You should always check the terms of service of the websites you are scraping and obtain permission if necessary.

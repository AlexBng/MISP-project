import requests
from bs4 import BeautifulSoup

# Récupération du code source de la page
url = "https://www.start.umd.edu/gtd/search/"
response = requests.get(url)

if response.status_code == 200:
    source_code = response.text
else:
    print("Error: Could not retrieve source code.")

# Création de l'objet BeautifulSoup à partir du code source
soup = BeautifulSoup(source_code, 'html.parser')

# Recherche du champ select ayant l'ID perpetrator
select_element = soup.select_one('#perpetrator')


# Extraction de toutes les options du champ select
options = select_element.find_all('option')
for option in options:
    print(option.text)

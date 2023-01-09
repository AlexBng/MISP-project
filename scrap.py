import requests
from bs4 import BeautifulSoup

# Récupération du code source de la page
url_advance_search = "https://www.start.umd.edu/gtd/search/"
response = requests.get(url_advance_search)

if response.status_code == 200:
    source_code = response.text
else:
    print("Error: Could not retrieve source code.")

# Création de l'objet BeautifulSoup à partir du code source
soup = BeautifulSoup(source_code, 'html.parser')

# Recherche du champ select ayant l'ID perpetrator
select_element = soup.select_one('#perpetrator')


# Création du dictionnaire
terrorist_groups = {}

# Extraction de toutes les options du champ select
options = select_element.find_all('option')
for option in options:
    # Ajout de chaque option au dictionnaire en utilisant la valeur de l'attribut value comme clé (clé = id, value = nom du groupe)
    terrorist_groups[option['value']] = option.text

# Affichage du dictionnaire
print(terrorist_groups)




# Create an empty dictionary to store the lists of incident ids for each group
group_incidents = {}

# Iterate through the keys (i.e., the group ids) in the terrorist_groups dictionary
for key in terrorist_groups:

    # Initialize an empty list to store the incident ids for the current group
    incidents = []

    # Retrieve the incidents for the group from the GTD website
    url_group_incidents = "https://www.start.umd.edu/gtd/search/Results.aspx?start_yearonly=&end_yearonly=&start_year=&start_month=&start_day=&end_year=&end_month=&end_day=&asmSelect0=&asmSelect1=&perpetrator="+key+"&dtp2=all&success=yes&casualties_type=b&casualties_max="
    response = requests.get(url_group_incidents)

    if response.status_code == 200:
        source_code = response.text
    else:
        print("Error: Could not retrieve source code.")

    # Parse the HTML response using BeautifulSoup
    soup = BeautifulSoup(source_code, 'html.parser')

    # Find the table with the class 'results'
    table = soup.find('table', class_='results')

    # Find the tbody within the table
    tbody = table.find('tbody')

    # Find all rows within the tbody
    rows = tbody.find_all('tr')

    # Iterate through the rows
    for row in rows:
        # Find the first td element in the row
        td = row.find('td')
        # Find the first a element within the td
        a = td.find('a')
        # Extract the incident id from the a element
        incident_id = a.text
        # Add the incident id to the list
        incidents.append(incident_id)

    # Add the list of incidents to the dictionary with the group id as the key
    group_incidents[key] = incidents

# Now, group_incidents is a dictionary with the group ids as the keys and the lists of incident ids as the values
print(group_incidents)

# url_incident = "https://www.start.umd.edu/gtd/search/IncidentSummary.aspx?gtdid=199203170009"
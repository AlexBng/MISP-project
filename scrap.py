import requests
import re
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

# Create an empty dictionary to store the characteristics of each incidents
incidents_characteristics = {}

i=0

# Iterate through the keys (i.e., the group ids) in the terrorist_groups dictionary
for key in terrorist_groups:

    if i==2:
        break
    i+=1
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
        # Find the first td element in the rows
        td = row.find('td')
        # Find the first a element within the td
        a = td.find('a')
        # Extract the incident id from the a element
        incident_id = a.text
        # Add the incident id to the list
        incidents.append(incident_id)

        # If the incident havn't been registered yet, we store it's id in the dictionary. We'll use it later to find characteristics about the incidents
        if incident_id not in incidents_characteristics:
            incidents_characteristics[incident_id] = None

    # Add the list of incidents to the dictionary with the group id as the key
    group_incidents[key] = incidents

# Now, group_incidents is a dictionary with the group ids as the keys and the lists of incident ids as the values


# Creation of a dictionary to store every characteristics of an incident (Sources is a list of URLs)
characteristics = {'Date': None, 'Country': None, 'Region': None, 'Province': None, 'City': None, 'TypeOfAttack': None, 'Successful': None, 
'TargetType': None, 'EntityName': None, 'SpecificDescription': None, 'TargetNationality': None, 'Hostages': None, 'Ransom': None, 'PropertyDamage': None, 
'PropertyDamageExtent': None, 'PropertyDamageValue': None, 'WeaponType': None, 'SubWeaponType': None, 'WeaponDetails': None, 'SuicideAttack': None, 
'PartOfMultipleIncident': None, 'Criterion1': None, 'Criterion2': None, 'Criterion3': None, 'ClaimedResponsibility': None, 
'PerpetratorsNumber': None, 'CapturedPerpetratorsNumber': None, 'CasualitiesNumber': None, 'FatalitiesNumber': None, 'PerpetratorsFatalitiesNumber': None, 
'InjuredNumber': None, 'PerpetratorsInjuredNumber': None, 'Sources': None}

for key in incidents_characteristics:

    url_incident = "https://www.start.umd.edu/gtd/search/IncidentSummary.aspx?gtdid=199211060007"

    response = requests.get(url_incident)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get every informations of the summary-overview
    for p in soup.select('.summary-overview p'):
        head = p.find("span", class_="leftHead").text
        span_text = p.find("span", class_="leftLarge").text
        if "When:" in head:
            characteristics['Date'] = span_text
        elif "Country:" in head:
            characteristics['Country'] = span_text
        elif "Region:" in head:
            characteristics['Region'] = span_text
        elif "Province/administrative region/u.s. state:" in head:
            characteristics['Province'] = span_text
        elif "City:" in head:
            characteristics['City'] = span_text

    # Get informations of WHAT
    characteristics['TypeOfAttack'] = soup.select_one('#popupTactics').find_parent('td').find_next_sibling('td').text
    characteristics['Successful'] = soup.select_one('#popupSuccess').find_parent('td').find_next_sibling('td').text
    characteristics['TargetType'] = soup.find("th", text=lambda text: "Target Type:" in text).text.replace("Target Type: ","")
    characteristics['EntityName'] = soup.find("td", text="Name of Entity").find_next_sibling("td").text
    characteristics['SpecificDescription'] = soup.find("td", text="Specific Description").find_next_sibling("td").text
    characteristics['TargetNationality'] = soup.find("td", text="Nationality of Target").find_next_sibling("td").text
    characteristics['Hostages'] = soup.find("td", text="Hostages").find_next_sibling("td").text
    characteristics['Ransom'] = soup.find("td", text="Ransom").find_next_sibling("td").text
    characteristics['PropertyDamage'] = soup.find("td", text="Property Damage").find_next_sibling("td").text
    characteristics['PropertyDamageExtent'] = soup.find("td", text="Extent of Property Damage").find_next_sibling("td").text
    characteristics['PropertyDamageValue'] = soup.find("td", text="Value of Property Damage").find_next_sibling("td").text


    print(characteristics)

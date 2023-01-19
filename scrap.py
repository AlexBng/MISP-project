import requests
import re
from bs4 import BeautifulSoup
import json


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
# print(terrorist_groups)




# Create an empty dictionary to store the lists of incident ids for each group
group_incidents = {}

# Create an empty dictionary to store the characteristics of each incidents
incidents_characteristics = {}

i=0

# Iterate through the keys (i.e., the group ids) in the terrorist_groups dictionary
for key in terrorist_groups:

    if i==200:
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
characteristics = {'Description':None, 'Date': None, 'Country': None, 'Region': None, 'Province': None, 'City': None, 'LocationDetails': None,
 'TypeOfAttack1': None, 'TypeOfAttack2': None, 'TypeOfAttack3': None, 'Successful': None, 
'TargetType1': None, 'TargetType2': None,'TargetType3': None,'EntityName1': None, 'EntityName2': None, 'EntityName3': None,
'SpecificDescription1': None, 'SpecificDescription2': None,'SpecificDescription3': None, 'TargetNationality1': None, 'TargetNationality2': None,
'TargetNationality3': None, 'Hostages': None, 'HostagesNumber':None, 'Ransom': None, 'PropertyDamage': None, 
'PropertyDamageExtent': None, 'PropertyDamageValue': None, 'WeaponType1': None, 'SubWeaponType1': None, 'WeaponType2': None, 'SubWeaponType2': None,
'WeaponType3': None, 'SubWeaponType3': None, 'WeaponType4': None, 'SubWeaponType4': None,'WeaponDetails': None, 'SuicideAttack': None, 
'PartOfMultipleIncident': None, 'Criterion1': None, 'Criterion2': None, 'Criterion3': None, 'DoubtTerrorismProper': None, 'GroupName' : None,
'PerpetratorsNumber': None, 'CapturedPerpetratorsNumber': None, 'CasualitiesNumber': None, 'FatalitiesNumber': None, 'PerpetratorsFatalitiesNumber': None, 
'InjuredNumber': None, 'PerpetratorsInjuredNumber': None, 'Sources': None}

with open('data.json', 'w') as f:
    f.truncate(0)

for key in incidents_characteristics:
    print(key)
    url_incident = "https://www.start.umd.edu/gtd/search/IncidentSummary.aspx?gtdid=" + key

    response = requests.get(url_incident)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get every informations of the summary-overview

    # The description isn't present everytime
    description = soup.select_one('#incidentSummary')
    if(description): 
        text = description.find('div').find('h1').next_sibling
        text = text.replace("\n\t\t","")
        characteristics['Description'] = text.replace("\n\t","")


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
        elif "Location Details:" in head:
            characteristics['LocationDetails'] = span_text

    # Get informations of WHAT

    # A minimum of 1 type of attack and a miximum of 3 is printed on the website
    attackType = soup.select('#popupTactics')
    characteristics['TypeOfAttack1'] = attackType[0].find_parent('td').find_next_sibling('td').text
    if(len(attackType) > 1):
        characteristics['TypeOfAttack2'] = attackType[1].find_parent('td').find_next_sibling('td').text
    if(len(attackType) > 2):
        characteristics['TypeOfAttack3'] = attackType[2].find_parent('td').find_next_sibling('td').text

    characteristics['Successful'] = soup.select_one('#popupSuccess').find_parent('td').find_next_sibling('td').text

    targetType = soup.find_all("th", text=lambda text: "Target Type:" in text)
    entityName = soup.find_all("td", text="Name of Entity")
    specificDescription = soup.find_all("td", text="Specific Description")
    targetNationality = soup.find_all("td", text="Nationality of Target")
    characteristics['TargetType1'] = targetType[0].text.replace("Target Type: ","")
    characteristics['EntityName1'] = entityName[0].find_next_sibling("td").text
    characteristics['SpecificDescription1'] = specificDescription[0].find_next_sibling("td").text
    characteristics['TargetNationality1'] = targetNationality[0].find_next_sibling("td").text
    if(len(targetType) > 1):
        characteristics['TargetType2'] = targetType[1].text.replace("Target Type: ","")
        characteristics['EntityName2'] = entityName[1].find_next_sibling("td").text
        characteristics['SpecificDescription2'] = specificDescription[1].find_next_sibling("td").text
        characteristics['TargetNationality2'] = targetNationality[1].find_next_sibling("td").text
    if(len(targetType) > 2):
        characteristics['TargetType3'] = targetType[2].text.replace("Target Type: ","")
        characteristics['EntityName3'] = entityName[2].find_next_sibling("td").text
        characteristics['SpecificDescription3'] = specificDescription[2].find_next_sibling("td").text
        characteristics['TargetNationality3'] = targetNationality[2].find_next_sibling("td").text


    hostage = soup.find("td", text="Hostages")
    if(hostage):
        characteristics['Hostages'] = hostage.find_next_sibling("td").text

    number = soup.find("td", text="Number of Hostages")
    if(number):
        characteristics['HostagesNumber'] = number.find_next_sibling("td").text
    # Ransom fields missing (ex : 197802190002)

    ransom = soup.find("td", text="Ransom")
    if(ransom):
        characteristics['Ransom'] = ransom.find_next_sibling("td").text

    propertyDamage = soup.find("td", text="Property Damage")
    if(propertyDamage):
        characteristics['PropertyDamage'] = propertyDamage.find_next_sibling("td").text

    extent = soup.find("td", text="Extent of Property Damage")
    if(extent):
        characteristics['PropertyDamageExtent'] = extent.find_next_sibling("td").text
    value = soup.find("td", text="Value of Property Damage")
    if(value):
        characteristics['PropertyDamageValue'] = value.find_next_sibling("td").text

    # Get informations of HOW
    # Between 1 and 4 weapon
    weapon = soup.find("th", text="Type").find_parent('tr').find_parent('thead').find_next_sibling('tbody').find_all("tr")
    characteristics['WeaponType1'] = weapon[0].find_all('td')[0].text
    characteristics['SubWeaponType1'] = weapon[0].find_all('td')[1].text
    if(len(weapon) > 1  and len(weapon[1].find_all('td')) == 2):
        characteristics['WeaponType2'] = weapon[1].find_all('td')[0].text
        characteristics['SubWeaponType2'] = weapon[1].find_all('td')[1].text
    if(len(weapon) > 2 and len(weapon[2].find_all('td')) == 2):
        characteristics['WeaponType3'] = weapon[2].find_all('td')[0].text
        characteristics['SubWeaponType3'] = weapon[2].find_all('td')[1].text
    if(len(weapon) > 3 and len(weapon[3].find_all('td')) == 2):
        characteristics['WeaponType4'] = weapon[3].find_all('td')[0].text
        characteristics['SubWeaponType4'] = weapon[3].find_all('td')[1].text

    details = soup.find("th", text="Weapon Details")
    if(details):
        characteristics['WeaponDetails'] = details.find_parent('tr').find_next_sibling('tr').find('td').text
    characteristics['SuicideAttack'] = soup.find("td", text="Suicide Attack?").find_next_sibling('td').text
    characteristics['PartOfMultipleIncident'] = soup.find("td", text="Part of Multiple Incident?").find_next_sibling('td').text
    characteristics['Criterion1'] = soup.select_one('#popupCriterionOne').find_parent('td').find_next_sibling('td').text
    characteristics['Criterion2'] = soup.select_one('#popupCriterionTwo').find_parent('td').find_next_sibling('td').text
    characteristics['Criterion3'] = soup.select_one('#popupCriterionThree').find_parent('td').find_next_sibling('td').text

    # Field not present everytime
    doubt = soup.select_one('#popupCriteriaDTP')
    if doubt:
        characteristics['DoubtTerrorismProper'] = doubt.find_parent('td').find_next_sibling('td').text

    # Get informations of WHO
    # Responsability and sub-name fields missing, multiple groups possible
    groups = []
    for tr in soup.find("th", text="Group Name").find_parent('tr').find_parent('thead').find_next_sibling('tbody').find_all("tr"):
        groups.append(tr.find_all('td')[0].text)
    characteristics['GroupName'] = groups

    characteristics['PerpetratorsNumber'] = soup.find("td", text="Number of Perpetrators").find_next_sibling('td').text
    characteristics['CapturedPerpetratorsNumber'] = soup.find("td", text="Number of Captured Perpetrators").find_next_sibling('td').text
    characteristics['CasualitiesNumber'] = soup.find("td", text="Total Number of Casualties").find_next_sibling('td').text
    characteristics['FatalitiesNumber'] = soup.find("td", text="Total Number of Fatalities").find_next_sibling('td').text
    characteristics['PerpetratorsFatalitiesNumber'] = soup.find("td", text="Number of Perpetrator Fatalities").find_next_sibling('td').text
    characteristics['InjuredNumber'] = soup.find("td", text="Total Number of Injured").find_next_sibling('td').text
    characteristics['PerpetratorsInjuredNumber'] = soup.find("td", text="Number of Perpetrators Injured").find_next_sibling('td').text

    # Creation of the description if it doesn't exist
    if(characteristics['Description'] == None):
        characteristics['Description'] = characteristics['Date'] + ": " + " ".join(characteristics['GroupName']) + " operated an attack in " + characteristics['Country'] + "."

    # Sources
    sources = []
    for tr in soup.find('caption', text='Sources').find_next_sibling('tbody').find_all('tr'):
        sources.append(tr.find('td').text)
    characteristics['Sources'] = sources

    print(characteristics)
    # Stock the data
    with open('data.json', 'a') as f:
        json.dump(characteristics, f)
        f.write("\n")

    # Reinitialisation
    for key in characteristics:
        characteristics[key] = None

#  all_files = glob.glob("/Users/bryanbaumgartner/Documents/Study/M2/TI/docker/scrapping/ammo/*.txt")
#     cluster_incidents = {
#     "description":"Description of terrorist incidents until 2020",
#     "icon":"bomb",
#     "name": "Terrorist incidents",
#     "namespace": "terrorism",
#     "authors": ["Alexandre BEINING"],
#     "type":"terrorism",
#     "source": "https://www.start.umd.edu/gtd/",
#     "uuid":"9cdaf175-a972-44a9-900d-df459087569f",
#     "version":"1"
# }
#     f = open("ammunitions.json", 'a')
#     for file in all_files :
#         with open(file, "r") as ammos :
#             if os.path.getsize(file) != 0 :
#                 lines = ammos.readlines()
#                 for ammo in lines :
#                     #do something with the data
#                     manu = ammo.split()[0].strip()
#                     name = ammo.split("-")[0].strip()
#                     caliber = vendors = name.split()[1:]
#                     caliber = ' '.join(caliber).strip()
#                     description = ammo.split("-")[1].replace("\n", "").strip()
#                     meta = {
#                         "manufacturer": manu,
#                         "name": name,
#                         "caliber": caliber,
#                         "description": description
#                     }

#                     new_value = {
#                         "meta": meta,
#                         "uuid": uuidgen(),
#                         "value": name
#                     }
#                     cluster_ammo_vendors["values"].append(new_value)
#     f.write (json.dumps(cluster_ammo_vendors))

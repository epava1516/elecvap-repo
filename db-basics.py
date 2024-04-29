import requests
from bs4 import BeautifulSoup
import json

# Función para extraer los datos de la tabla de componentes
def extract_component_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    component_table = soup.find('table', {'width': '100%'})
    component_rows = component_table.find_all('tr')[1:]  # Ignorar la primera fila de encabezados
    component_data = []
    for row in component_rows:
        columns = row.find_all('td')
        component = {
            'COMPONENTE': columns[0].text.strip(),
            'CAS': columns[1].text.strip(),
            'Tipo': columns[2].text.strip(),
            'Porcentaje': columns[3].text.strip(),
            'Descripcion': columns[4].text.strip()
        }
        component_data.append(component)
    return component_data

# Función para extraer los enlaces de SDS U.S
def extract_sds_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    sds_links = soup.find_all('a', href=True, string='SDS U.S')
    sds_urls = [link['href'] for link in sds_links]
    return sds_urls

# URL de ejemplo del sitio web
url = 'https://shop.perfumersapprentice.com/specsheetlist.aspx'

# Extraer los datos de la tabla de componentes
component_data = extract_component_data(url)

# Extraer los enlaces de SDS U.S
sds_urls = extract_sds_links(url)

# Combinar datos de componentes con enlaces de SDS U.S
for i, component in enumerate(component_data):
    component['SDS_U.S'] = sds_urls[i] if i < len(sds_urls) else ''

# Generar el JSON
data = {
    'Producto': 'Nombre del producto',
    'Componentes': component_data
}

# Guardar el JSON en un archivo
with open('datos.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

print('Datos extraídos y guardados en datos.json')

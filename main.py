from datetime import datetime
from bs4 import BeautifulSoup
from requests import get
from unidecode import unidecode

MAIN_URL = 'https://www.pyphoy.com'

# ['Ciudad', 'Armenia', 'Barbosa', 'Barranquilla', 'Bello', 'Bogotá', 'Bucaramanga', 'Buenaventura'
# , 'Caldas', 'Cali', 'Cartagena', 'Copacabana', 'Cúcuta', 'Dosquebradas', 'Envigado', 'Fusagasugá'
# , 'Girardota', 'Ibagué', 'Ipiales', 'Itagüí', 'La Estrella', 'Malambo', 'Manizales', 'Medellín',
#  'Ocaña', 'Pamplona', 'Pasto', 'Pereira', 'Popayán', 'Quibdó', 'Sabaneta', 'Santa Cruz de Lorica',
#  'Santa Marta', 'Soacha', 'Soledad', 'Tunja', 'Turbaco', 'Villavicencio']

# ['', 'armenia', 'barbosa', 'barranquilla', 'bello', 'bogota', 'bucaramanga', 'buenaventura'
# , 'caldas', 'cali', 'cartagena', 'copacabana', 'cucuta', 'dosquebradas', 'envigado', 'fusagasuga'
# , 'girardota', 'ibague', 'ipiales', 'itagui', 'la-estrella', 'malambo', 'manizales', 'medellin'
# , 'ocana', 'pamplona', 'pasto', 'pereira', 'popayan', 'quibdo', 'sabaneta', 'santa-cruz-de-lorica'
# , 'santa-marta', 'soacha', 'soledad', 'tunja', 'turbaco', 'villavicencio']

# accented_string = 'Ocaña'
# accented_string = accented_string.lower().replace(' ', '-')
# print(unidecode(accented_string))


def check_url_online():
    response = get(MAIN_URL)
    if response.status_code != 200:
        print("Error fetching page")
        raise ValueError('Web offline')
    else:
        return response.content


def get_city_list(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    # ciudades_text = [option.get_text() for option in soup.find_all('option')]
    ciudades_val = [option.get('value').replace('/','') for option in soup.find_all('option')]
    return ciudades_val


def validate_city(ciudad, page_content):
    # Validar si la ciudad esta en la lista de ciudades permitidas
    # Obtener lista de ciudades de manera activa de la pagina.

    ciudades_val = get_city_list(page_content)

    # accented_string = 'Ocaña'
    ciudad_normalized = unidecode(ciudad.lower().replace(' ', '-'))

    for ciudad_val in ciudades_val:
        if ciudad_normalized == ciudad_val:
            return ciudad_normalized
    print('No se pudo validar la ciudad.')
    return False


def validate_date(fecha):
    # Validar si la fecha ingresada esta en el formato correcto.
    try:
        fecha = datetime.strptime(fecha, '%Y-%m-%d')
    except ValueError:
        fecha = None
    except Exception:
        fecha = None
    return fecha



def check_pyp(ciudad,fecha):

    page_content = check_url_online()

    ciudad = validate_city(ciudad, page_content)
    fecha = validate_date(fecha)

    if fecha == None:
        print('Error en fecha')
        exit()
    elif ciudad == None:
        print('Error en ciudad')
        exit()

    #url = 'https://www.pyphoy.com/bello/particulares?fecha=2022-02-16'
    url = f'https://www.pyphoy.com/{ciudad}/particulares?fecha={fecha}'

    response = get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    placas = soup.select('#__next > div > div.sc-fe794954-0.cIVSel > main > article > div.sc-5a024460-0.fKtfLq.sc-910a33cd-0.gTHkiE.sc-5aa24f34-9.fhnWAu > div.sc-5a024460-1.eFWKPI.card-header > div > div > div.sc-43a2f702-0.brIPFA.sc-5aa24f34-2.bZLJNJ')
    placas = placas[0].get_text()

    texto = soup.select('#__next > div > div.sc-fe794954-0.cIVSel > main > article > header > div')
    texto = texto[0].get_text()

    return placas, texto




if __name__ == '__main__':
    placas, texto = check_pyp('Medellín', '2022-07-14')
    print(texto, placas)

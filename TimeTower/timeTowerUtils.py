from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

##############################################################################
# DEBUG
##############################################################################

DEBUG_MODE_LOCAL_FLAG = False  # Default : False, put to True to use local USA flag as placeholder to reduce data usage
DEBUG_MODE_LOCALHOST_LIVE = False  # Default : False, put to True to use a local WCA Live for testing/developing

##############################################################################

DNF_ATTEMPT = 30 * 60 * 100  # 30 min, so an avg5/mo3 goes higher than 10 min
DNF_RESULT = 10 * 60 * 100  # 10 min

CRITERIA = dict([
    ('333', 'average'),
    ('222', 'average'),
    ('444', 'average'),
    ('555', 'average'),
    ('666', 'mean'),
    ('777', 'mean'),
    ('333bf', 'single'),
    ('333fm', 'mean'),
    ('333oh', 'average'),
    ('clock', 'average'),
    ('minx', 'average'),
    ('pyram', 'average'),
    ('skewb', 'average'),
    ('sq1', 'average'),
    ('444bf', 'single'),
    ('555bf', 'single'),
    ('333mbf', 'single'),
])

COUNTRIES = dict([
    ('AF', ('Afghanistan', 'Asia')),
    ('AL', ('Albania', 'Europe')),
    ('DZ', ('Algeria', 'Africa')),
    ('AD', ('Andorra', 'Europe')),
    ('AO', ('Angola', 'Africa')),
    ('AG', ('Antigua and Barbuda', 'North America')),
    ('AR', ('Argentina', 'South America')),
    ('AM', ('Armenia', 'Europe')),
    ('AU', ('Australia', 'Oceania')),
    ('AT', ('Austria', 'Europe')),
    ('AZ', ('Azerbaijan', 'Europe')),
    ('BS', ('Bahamas', 'North America')),
    ('BH', ('Bahrain', 'Asia')),
    ('BD', ('Bangladesh', 'Asia')),
    ('BB', ('Barbados', 'North America')),
    ('BY', ('Belarus', 'Europe')),
    ('BE', ('Belgium', 'Europe')),
    ('BZ', ('Belize', 'North America')),
    ('BJ', ('Benin', 'Africa')),
    ('BT', ('Bhutan', 'Asia')),
    ('BO', ('Bolivia', 'South America')),
    ('BA', ('Bosnia and Herzegovina', 'Europe')),
    ('BW', ('Botswana', 'Africa')),
    ('BR', ('Brazil', 'South America')),
    ('BN', ('Brunei', 'Asia')),
    ('BG', ('Bulgaria', 'Europe')),
    ('BF', ('Burkina Faso', 'Africa')),
    ('BI', ('Burundi', 'Africa')),
    ('CV', ('Cabo Verde', 'Africa')),
    ('KH', ('Cambodia', 'Asia')),
    ('CM', ('Cameroon', 'Africa')),
    ('CA', ('Canada', 'North America')),
    ('CF', ('Central African Republic', 'Africa')),
    ('TD', ('Chad', 'Africa')),
    ('CL', ('Chile', 'South America')),
    ('CN', ('China', 'Asia')),
    ('CO', ('Colombia', 'South America')),
    ('KM', ('Comoros', 'Africa')),
    ('CG', ('Congo', 'Africa')),
    ('CR', ('Costa Rica', 'North America')),
    ('CI', ('Côte d\'Ivoire', 'Africa')),
    ('HR', ('Croatia', 'Europe')),
    ('CU', ('Cuba', 'North America')),
    ('CY', ('Cyprus', 'Europe')),
    ('CZ', ('Czech Republic', 'Europe')),
    ('KP', ('Democratic People\'s Republic of Korea', 'Asia')),
    ('CD', ('Democratic Republic of the Congo', 'Africa')),
    ('DK', ('Denmark', 'Europe')),
    ('DJ', ('Djibouti', 'Africa')),
    ('DM', ('Dominica', 'North America')),
    ('DO', ('Dominican Republic', 'North America')),
    ('EC', ('Ecuador', 'South America')),
    ('EG', ('Egypt', 'Africa')),
    ('SV', ('El Salvador', 'North America')),
    ('GQ', ('Equatorial Guinea', 'Africa')),
    ('ER', ('Eritrea', 'Africa')),
    ('EE', ('Estonia', 'Europe')),
    ('SZ', ('Eswatini', 'Africa')),
    ('ET', ('Ethiopia', 'Africa')),
    ('FM', ('Federated States of Micronesia', 'Oceania')),
    ('FJ', ('Fiji', 'Oceania')),
    ('FI', ('Finland', 'Europe')),
    ('FR', ('France', 'Europe')),
    ('GA', ('Gabon', 'Africa')),
    ('GM', ('Gambia', 'Africa')),
    ('GE', ('Georgia', 'Europe')),
    ('DE', ('Germany', 'Europe')),
    ('GH', ('Ghana', 'Africa')),
    ('GR', ('Greece', 'Europe')),
    ('GD', ('Grenada', 'North America')),
    ('GT', ('Guatemala', 'North America')),
    ('GN', ('Guinea', 'Africa')),
    ('GW', ('Guinea Bissau', 'Africa')),
    ('GY', ('Guyana', 'South America')),
    ('HT', ('Haiti', 'North America')),
    ('HN', ('Honduras', 'North America')),
    ('HK', ('Hong Kong, China', 'Asia')),
    ('HU', ('Hungary', 'Europe')),
    ('IS', ('Iceland', 'Europe')),
    ('IN', ('India', 'Asia')),
    ('ID', ('Indonesia', 'Asia')),
    ('IR', ('Iran', 'Asia')),
    ('IQ', ('Iraq', 'Asia')),
    ('IE', ('Ireland', 'Europe')),
    ('IL', ('Israel', 'Europe')),
    ('IT', ('Italy', 'Europe')),
    ('JM', ('Jamaica', 'North America')),
    ('JP', ('Japan', 'Asia')),
    ('JO', ('Jordan', 'Asia')),
    ('KZ', ('Kazakhstan', 'Asia')),
    ('KE', ('Kenya', 'Africa')),
    ('KI', ('Kiribati', 'Oceania')),
    ('KR', ('Republic of Korea', 'Asia')),
    ('XK', ('Kosovo', 'Europe')),
    ('KW', ('Kuwait', 'Asia')),
    ('KG', ('Kyrgyzstan', 'Asia')),
    ('LA', ('Laos', 'Asia')),
    ('LV', ('Latvia', 'Europe')),
    ('LB', ('Lebanon', 'Asia')),
    ('LS', ('Lesotho', 'Africa')),
    ('LR', ('Liberia', 'Africa')),
    ('LY', ('Libya', 'Africa')),
    ('LI', ('Liechtenstein', 'Europe')),
    ('LT', ('Lithuania', 'Europe')),
    ('LU', ('Luxembourg', 'Europe')),
    ('MO', ('Macau, China', 'Asia')),
    ('MG', ('Madagascar', 'Africa')),
    ('MW', ('Malawi', 'Africa')),
    ('MY', ('Malaysia', 'Asia')),
    ('MV', ('Maldives', 'Asia')),
    ('ML', ('Mali', 'Africa')),
    ('MT', ('Malta', 'Europe')),
    ('MH', ('Marshall Islands', 'Oceania')),
    ('MR', ('Mauritania', 'Africa')),
    ('MU', ('Mauritius', 'Africa')),
    ('MX', ('Mexico', 'North America')),
    ('MD', ('Moldova', 'Europe')),
    ('MC', ('Monaco', 'Europe')),
    ('MN', ('Mongolia', 'Asia')),
    ('ME', ('Montenegro', 'Europe')),
    ('MA', ('Morocco', 'Africa')),
    ('MZ', ('Mozambique', 'Africa')),
    ('MM', ('Myanmar', 'Asia')),
    ('NA', ('Namibia', 'Africa')),
    ('NR', ('Nauru', 'Oceania')),
    ('NP', ('Nepal', 'Asia')),
    ('NL', ('Netherlands', 'Europe')),
    ('NZ', ('New Zealand', 'Oceania')),
    ('NI', ('Nicaragua', 'North America')),
    ('NE', ('Niger', 'Africa')),
    ('NG', ('Nigeria', 'Africa')),
    ('MK', ('North Macedonia', 'Europe')),
    ('NO', ('Norway', 'Europe')),
    ('OM', ('Oman', 'Asia')),
    ('PK', ('Pakistan', 'Asia')),
    ('PW', ('Palau', 'Oceania')),
    ('PS', ('Palestine', 'Asia')),
    ('PA', ('Panama', 'North America')),
    ('PG', ('Papua New Guinea', 'Oceania')),
    ('PY', ('Paraguay', 'South America')),
    ('PE', ('Peru', 'South America')),
    ('PH', ('Philippines', 'Asia')),
    ('PL', ('Poland', 'Europe')),
    ('PT', ('Portugal', 'Europe')),
    ('QA', ('Qatar', 'Asia')),
    ('RO', ('Romania', 'Europe')),
    ('RU', ('Russia', 'Europe')),
    ('RW', ('Rwanda', 'Africa')),
    ('KN', ('Saint Kitts and Nevis', 'North America')),
    ('LC', ('Saint Lucia', 'North America')),
    ('VC', ('Saint Vincent and the Grenadines', 'North America')),
    ('WS', ('Samoa', 'Oceania')),
    ('SM', ('San Marino', 'Europe')),
    ('ST', ('São Tomé and Príncipe', 'Africa')),
    ('SA', ('Saudi Arabia', 'Asia')),
    ('SN', ('Senegal', 'Africa')),
    ('RS', ('Serbia', 'Europe')),
    ('SC', ('Seychelles', 'Africa')),
    ('SL', ('Sierra Leone', 'Africa')),
    ('SG', ('Singapore', 'Asia')),
    ('SK', ('Slovakia', 'Europe')),
    ('SI', ('Slovenia', 'Europe')),
    ('SB', ('Solomon Islands', 'Oceania')),
    ('SO', ('Somalia', 'Africa')),
    ('ZA', ('South Africa', 'Africa')),
    ('SS', ('South Sudan', 'Africa')),
    ('ES', ('Spain', 'Europe')),
    ('LK', ('Sri Lanka', 'Asia')),
    ('SD', ('Sudan', 'Africa')),
    ('SR', ('Suriname', 'South America')),
    ('SE', ('Sweden', 'Europe')),
    ('CH', ('Switzerland', 'Europe')),
    ('SY', ('Syria', 'Asia')),
    ('TW', ('Chinese Taipei', 'Asia')),
    ('TJ', ('Tajikistan', 'Asia')),
    ('TZ', ('Tanzania', 'Africa')),
    ('TH', ('Thailand', 'Asia')),
    ('TL', ('Timor-Leste', 'Asia')),
    ('TG', ('Togo', 'Africa')),
    ('TO', ('Tonga', 'Oceania')),
    ('TT', ('Trinidad and Tobago', 'North America')),
    ('TN', ('Tunisia', 'Africa')),
    ('TR', ('Turkey', 'Europe')),
    ('TM', ('Turkmenistan', 'Asia')),
    ('TV', ('Tuvalu', 'Oceania')),
    ('UG', ('Uganda', 'Africa')),
    ('UA', ('Ukraine', 'Europe')),
    ('AE', ('United Arab Emirates', 'Asia')),
    ('GB', ('United Kingdom', 'Europe')),
    ('UY', ('Uruguay', 'South America')),
    ('US', ('United States', 'North America')),
    ('UZ', ('Uzbekistan', 'Asia')),
    ('VU', ('Vanuatu', 'Oceania')),
    ('VA', ('Vatican City', 'Europe')),
    ('VE', ('Venezuela', 'South America')),
    ('VN', ('Vietnam', 'Asia')),
    ('YE', ('Yemen', 'Asia')),
    ('ZM', ('Zambia', 'Africa')),
    ('ZW', ('Zimbabwe', 'Africa'))
])

CONTINENTS = ['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']

SEPARATOR = '-----'
REGION_OPTIONS = ['World'] + [SEPARATOR] + CONTINENTS + [SEPARATOR] + [country[0] for country in COUNTRIES.values()]

DEFAULT_BACKGROUND_COLOR = '#FFFFFF'
DEFAULT_BG_LOCAL_NAME = '#000000'
DEFAULT_BG_LOCAL_RESULT = '#555555'
DEFAULT_BG_FOREIGNER_NAME = '#444444'
DEFAULT_BG_FOREIGNER_RESULT = '#999999'
DEFAULT_WIDTH_RANKING = 50
DEFAULT_WIDTH_FLAG_RECTANGLE = 60
DEFAULT_HEIGHT_FLAG = 30
DEFAULT_WIDTH_NAME = 100
DEFAULT_WIDTH_FULL_NAME = 300
DEFAULT_WIDTH_COUNT = 50
DEFAULT_WIDTH_RESULT = 100
DEFAULT_WIDTH_FULL_RESULT = 300
DEFAULT_FONT_FAMILY = 'Arial'
DEFAULT_FONT_SIZE_BIG = 15
DEFAULT_FONT_SIZE_SMALL = 12
DEFAULT_HEIGHT = 50
DEFAULT_HEIGHT_SEPARATOR = 10
DEFAULT_COLOR_LOCAL_NAME = '#FFFFFF'
DEFAULT_COLOR_LOCAL_RESULT = '#FFFFFF'
DEFAULT_COLOR_FOREIGNER_NAME = '#FFFFFF'
DEFAULT_COLOR_FOREIGNER_RESULT = '#FFFFFF'
DEFAULT_MAX_NUMBER = 16
DEFAULT_DURATION_X = 1000
DEFAULT_DURATION_Y = 1000
DEFAULT_FPS_X = 50
DEFAULT_FPS_Y = 50

LAYOUT_MAX_WIDTH = 200
LAYOUT_MAX_HEIGHT = 200
LAYOUT_MAX_EXTENDED_WIDTH = 500
LAYOUT_MAX_FONT = 50
LAYOUT_CANVAS_WIDTH = 1000
LAYOUT_CANVAS_HEIGHT = 400


def getQueryResult(query):
    if (DEBUG_MODE_LOCALHOST_LIVE):
        url = 'http://localhost:4000/api'
    else:
        url = 'https://live.worldcubeassociation.org/api'
    transport = AIOHTTPTransport(url=url)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    return client.execute(gql(query))


def getReadableResult(result):
    if (result >= DNF_RESULT):
        return 'DNF'
    output = ''
    if (result >= 6000):
        output = output + f'{int(result / 6000)}:'
    result = result % 6000
    output = output + f'{int(result / 100):02}.{result % 100:02}'
    return output


def getAllResults(results, criteria):
    outputArray = []
    minFound = False
    maxFound = False
    if len(results) <= 3 or criteria != 'average':
        minFound = True
        maxFound = True
    for result in results:
        if not maxFound and (result == max(results) or result >= DNF_RESULT):
            maxFound = True
            outputArray.append(f'({getReadableResult(result)})')
        elif not minFound and (result == min(results)):
            minFound = True
            outputArray.append(f'({getReadableResult(result)})')
        else:
            outputArray.append(f'{getReadableResult(result)}')
    return ' '.join(outputArray)

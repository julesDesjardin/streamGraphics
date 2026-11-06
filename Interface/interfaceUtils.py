import tkinter as tk
from . import WCIFParse

EVENTS = dict([
    ('3x3x3', '333'),
    ('2x2x2', '222'),
    ('4x4x4', '444'),
    ('5x5x5', '555'),
    ('6x6x6', '666'),
    ('7x7x7', '777'),
    ('3x3x3 Blindfolded', '333bf'),
    ('3x3x3 Fewest Moves', '333fm'),
    ('3x3x3 One-handed', '333oh'),
    ('Clock', 'clock'),
    ('Megaminx', 'minx'),
    ('Pyraminx', 'pyram'),
    ('Skewb', 'skewb'),
    ('Square-1', 'sq1'),
    ('4x4x4 Blindfolded', '444bf'),
    ('5x5x5 Blindfolded', '555bf'),
    ('3x3x3 Multiblind', '333mbf')
])

SEED_TYPE = dict([
    ('333', 'average'),
    ('222', 'average'),
    ('444', 'average'),
    ('555', 'average'),
    ('666', 'average'),
    ('777', 'average'),
    ('333bf', 'single'),
    ('333fm', 'average'),
    ('333oh', 'average'),
    ('clock', 'average'),
    ('minx', 'average'),
    ('pyram', 'average'),
    ('skewb', 'average'),
    ('sq1', 'average'),
    ('444bf', 'average'),
    ('555bf', 'average'),
    ('333mbf', 'average'),
])

MAX_RANKING = 999999
MAX_SEED = 10000

CAMERAS_ROWS = 1
CAMERAS_COLS = 1
CAMERAS_COUNT = CAMERAS_ROWS * CAMERAS_COLS

FLASK_PORT = 5000

BUTTONS_ROWS = 4
BUTTONS_COLS = 7

FRAME_THICKNESS = 2
BUTTON_THICKNESS = 2
BUTTON_WIDTH = 110
BUTTON_HEIGHT = 30
BUTTON_PADX = 5
BUTTON_PADY = 5
LABEL_HEIGHT = 30

import tkinter as tk
import tkinter.messagebox
from tkinter.colorchooser import askcolor
import requests

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


def cleverInt(string):
    if string == '' or int(string) == 0:
        return 1
    else:
        return int(string)


def setModifiersVariables(modifiers, boldVar, italicVar):
    if 'bold' in modifiers:
        boldVar.set(True)
    else:
        boldVar.set(False)
    if 'italic' in modifiers:
        italicVar.set(True)
    else:
        italicVar.set(False)


def getModifiers(bold, italic):
    modifiers = []
    if bold:
        modifiers.append('bold')
    if italic:
        modifiers.append('italic')
    return ' '.join(modifiers)


def setAnchorVariables(anchor, XVar, YVar):
    if anchor == 'center':
        XVar.set('Center')
        YVar.set('Center')
    else:
        if 'w' in anchor:
            XVar.set('Left')
        elif 'e' in anchor:
            XVar.set('Right')
        else:
            XVar.set('Center')
        if 'n' in anchor:
            YVar.set('Top')
        elif 's' in anchor:
            YVar.set('Bottom')
        else:
            YVar.set('Center')


def getAnchor(XVar, YVar):
    anchor = ''
    if YVar == 'Top':
        anchor = anchor + 'n'
    elif YVar == 'Bottom':
        anchor = anchor + 's'
    if XVar == 'Left':
        anchor = anchor + 'w'
    elif XVar == 'Right':
        anchor = anchor + 'e'
    if anchor == '':
        anchor = 'center'
    return anchor


def getJustify(anchor):
    if anchor == 'center':
        return tk.LEFT
    if 'w' in anchor:
        return tk.LEFT
    if 'e' in anchor:
        return tk.RIGHT
    return tk.CENTER


checkSettings = []


def addCheckSettingsChanged(root, settingsChanged, saveSettings, name):
    checkSettings.append((settingsChanged, saveSettings, name))
    root.protocol('WM_DELETE_WINDOW', lambda: checkSettingsChanged(root, checkSettings))


def checkSettingsChanged(root, checkSettings):
    destroy = True
    for (settingsChanged, saveSettings, name) in checkSettings:
        if settingsChanged.get():
            confirmation = tkinter.messagebox.askyesnocancel(
                title='Unsaved settings', message=f'You currently have unsaved {name} settings! Do you want to save your {name} settings before quitting?', icon=tkinter.messagebox.WARNING)
            if confirmation is None:
                destroy = False
                break
            else:
                if confirmation:
                    saveSettings()
    if destroy:
        root.destroy()


def colorButtonCommand(button, var, title):
    colors = askcolor(var.get(), title=title)
    if colors[1] is not None:
        button.configure(background=colors[1])
        var.set(colors[1])


def getTextColorFromBackground(bg):
    red = int(bg[1:3], 16)
    green = int(bg[3:5], 16)
    blue = int(bg[5:7], 16)
    if (red * 0.299 + green * 0.587 + blue * 0.114) > 186:
        return '#000000'
    else:
        return '#ffffff'


def getFlagURL(country):
    if country == 'TW':
        return 'https://assets.worldcubeassociation.org/assets/c278ac8/packs/static/ChineseTaipei-1ba9a456aa87a706b47b.svg'
    else:
        return f'https://flagcdn.com/w320/{country.lower()}.png'


SINGULAR_URL_START = 'https://datastream.singular.live/datastreams/'


def sendPayload(datastream, payload):
    response = requests.put(
        SINGULAR_URL_START + datastream,
        json=payload,
        timeout=10
    )

    print('Sending payload:')
    print(payload)
    response.raise_for_status()


CURRENT_VERSION = 30


def resultToString(result):
    if result == 'DNF':
        return 'DNF'
    elif result >= 6000:
        return f"{int(result / 6000)}:{((result % 6000) / 100):05.2f}"
    return f"{((result % 6000) / 100):.2f}"


def replaceText(text, wcif, id, seed, event, round, customTexts):
    if int(round) > 1:
        previousRound = int(round) - 1
    else:
        previousRound = None
    previousRank = WCIFParse.getRoundRank(wcif, id, event, previousRound)
    prSingleInt = WCIFParse.getPb(wcif, id, event, 'single')
    prAverageInt = WCIFParse.getPb(wcif, id, event, 'average')
    WCAID = WCIFParse.getWCAID(wcif, id)
    text = text.replace('%WCAID', WCAID)
    text = text.replace('%prSingle', resultToString(prSingleInt))
    text = text.replace('%prAverage', resultToString(prAverageInt))
    text = text.replace('%nrSingle', f"{WCIFParse.getRanking(wcif,id,event,'single','national')}")
    text = text.replace('%nrAverage', f"{WCIFParse.getRanking(wcif,id,event,'average','national')}")
    text = text.replace('%crSingle', f"{WCIFParse.getRanking(wcif,id,event,'single','continental')}")
    text = text.replace('%crAverage', f"{WCIFParse.getRanking(wcif,id,event,'average','continental')}")
    text = text.replace('%wrSingle', f"{WCIFParse.getRanking(wcif,id,event,'single','world')}")
    text = text.replace('%wrAverage', f"{WCIFParse.getRanking(wcif,id,event,'average','world')}")
    text = text.replace('%seed', f"{seed}")
    text = text.replace('%previousRank', f"{previousRank}")
    text = text.replace('%previousSingle', resultToString(WCIFParse.getRoundResult(wcif, id, event, previousRound, 'single')))
    text = text.replace('%previousAverage', resultToString(WCIFParse.getRoundResult(wcif, id, event, previousRound, 'average')))
    if WCAID in customTexts[EVENTS[event]]:
        text = text.replace('%custom', customTexts[EVENTS[event]][WCAID])
    else:
        text = text.replace('%custom', '')
    return text

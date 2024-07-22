import tkinter as tk
import WCIFParse

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
    ('333bf', 'average'),
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

CAMERAS_ROWS = 2
CAMERAS_COLS = 2
CAMERAS_COUNT = CAMERAS_ROWS * CAMERAS_COLS

BUTTONS_ROWS = 4
BUTTONS_COLS = 7

FRAME_THICKNESS = 2
BUTTON_THICKNESS = 2
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 30
BUTTON_PADX = 5
BUTTON_PADY = 5
LABEL_HEIGHT = 30


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
    text = text.replace('%previousSingle', resultToString(WCIFParse.getRoundResult(wcif, id, event, round, 'single')))
    text = text.replace('%previousAverage', resultToString(WCIFParse.getRoundResult(wcif, id, event, round, 'average')))
    if WCAID in customTexts[EVENTS[event]]:
        text = text.replace('%custom', customTexts[EVENTS[event]][WCAID])
    else:
        text = text.replace('%custom', '')
    return text

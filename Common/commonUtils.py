import tkinter as tk


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

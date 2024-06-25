import tkinter as tk
import tkinter.messagebox
from tkinter.colorchooser import askcolor


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

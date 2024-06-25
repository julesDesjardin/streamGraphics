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

from django import template
from .letters_words import words, letters


register = template.Library()

CURRENCIES_SYMBOLS = {
    'like': 'Лайк(ов)',
    'ball': 'Балл(ов)'
}


@register.filter()
def currency(value, code='like'):
    postfix = CURRENCIES_SYMBOLS[code]
    return f'{value} {postfix}'


@register.filter(name='matrix')
def currency(message: str):
    global string2
    ln = len(words)
    filtred_message = ''
    string = ''
    pattern = '*'
    for i in message:
        string += i
        string2 = string.lower()

        flag = 0
        for j in words:
            if string2 not in j:
                flag += 1
            elif string2 == j:
                filtred_message += string[:1] + pattern * (len(string)-1)
                flag -= 1
                string = ''

        if flag == ln:
            filtred_message += string
            string = ''

    if string2 != '' and string2 not in words:
        filtred_message += string
    elif string2 != '' and string2 in words:
        filtred_message += pattern * len(string)

    return filtred_message


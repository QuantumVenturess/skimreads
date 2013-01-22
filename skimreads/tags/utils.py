import re

def banned_words():
    regex = r"""
    ass|bitch|cock|cunt|dick|fag|fuck|gay|queer|shit|pussy|tit|vagina
    """
    return re.compile(regex, re.VERBOSE)

def only_letters():
    return re.compile(r'^[A-Za-z]+$')
from django.core.exceptions import ObjectDoesNotExist
from tags.models import Tag
from users.utils import add_rep

import re

def auto_tag(request, reading):
    """Automatically generate a tag and tie
    based on the reading's title."""
    try:
        # check to see if user already tied a tag to this reading
        existing_tie = reading.tie_set.get(user=request.user)
    except ObjectDoesNotExist:
        title = reading.title.lower()
        pattern = re.compile(
            '|'.join([tag.name for tag in Tag.objects.all()]))
        # match the title against all tag names
        result = re.search(pattern, title)
        # if there is a match
        if result:
            match = title[result.start():result.end()]
            try:
                # check to see if there is a tag with that name
                tag = Tag.objects.get(name=match)
                try:
                    # if there is a tie with that tag already, do nothing
                    tie = reading.tie_set.get(tag=tag)
                except ObjectDoesNotExist:
                    # tie a tag to reading
                    tie = reading.user.tie_set.create(reading=reading, tag=tag)
                    # add rep
                    add_rep(request, t=tie)
            except ObjectDoesNotExist:
                pass

def banned_words():
#    regex = r"""
#    ass|bitch|cock|cunt|dick|fag|fuck|gay|queer|shit|pussy|tit|vagina
#    """
#    return re.compile(regex, re.VERBOSE)
    return re.compile(r'xxxyyyzzz')

def only_letters():
#    return re.compile(r'^[A-Za-z]+$')
    return re.compile(r'^[0-9A-Za-z _-]+$')
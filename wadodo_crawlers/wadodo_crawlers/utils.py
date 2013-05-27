__all__ = [
    'replace_nbrs'
]


def replace_nbrs(string):
    """
    Replace non breaking space HTML entities with actual whitespace.
    """
    return string.replace(u'\xa0', u' ')


class JoinAddress(object):
    def __init__(self):
        pass

    def __call__(self, values):
        """
        Join address in the following format:
        ['Address', 'City', 'State', 'Zip Code']
        """
        length = len(values)

        if length <= 3:
            # No zip code
            return ', '.join(values)
        elif length == 4:
            # ZIP code included
            return ', '.join(values[:3]) + ' ' + values[3]
        else:
            # TODO
            print length
            print values

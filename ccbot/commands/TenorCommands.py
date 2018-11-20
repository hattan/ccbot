from services.TenorCommand import TenorCommand

class WhoMe(TenorCommand):
    """Returns a Dr. Who random image"""
    def __init__(self):
        TenorCommand.__init__(self, 'whome','dr.+who')

class BobMe(TenorCommand):
    """Returns a Spongebob Square Pants random image"""
    def __init__(self):
        TenorCommand.__init__(self, BobMe.__name__, 'spongebob')


class MadMaxMe(TenorCommand):
    """Returns a Mad Max random image"""
    def __init__(self):
        TenorCommand.__init__(self, MadMaxMe.__name__, 'madmax')


class StaloneMe(TenorCommand):
    """Returns a Silvester Stalone random image"""
    def __init__(self):
        TenorCommand.__init__(self, StaloneMe.__name__, 'stalone')


class MarxMe(TenorCommand):
    """Returns a Groucho Marx random image"""
    def __init__(self):
        TenorCommand.__init__(self, MarxMe.__name__, 'groucho+marx')


class StoogeMe(TenorCommand):
    """Returns a Three Stooges random image"""
    def __init__(self):
        TenorCommand.__init__(self, StoogeMe.__name__, 'three+stooges')


class AlfMe(TenorCommand):
    """Returns an Alf random image"""
    def __init__(self):
        TenorCommand.__init__(self, AlfMe.__name__, 'alf')


class ElfMe(TenorCommand):
    """Returns an Elf random image"""
    def __init__(self):
        TenorCommand.__init__(self, ElfMe.__name__, 'elf')


class HanukkahMe(TenorCommand):
    """Returns a Hanukkah random image"""
    def __init__(self):
        TenorCommand.__init__(self, HanukkahMe.__name__, 'hanukkah')


class KwanzaaMe(TenorCommand):
    """Returns a Kwanzaa random image"""
    def __init__(self):
        TenorCommand.__init__(self, KwanzaaMe.__name__, 'kwanzaa')


class KillMe(TenorCommand):
    """Returns a Kill Bill random image"""

    def __init__(self):
        TenorCommand.__init__(self, KillMe.__name__, 'killbill')


class TrekMe(TenorCommand):
    """Returns a StarTrek random image"""

    def __init__(self):
        TenorCommand.__init__(self, TrekMe.__name__, 'startrek')


class UrkelMe(TenorCommand):
    """Returns a Steve Urkle random image"""

    def __init__(self):
        TenorCommand.__init__(self, UrkelMe.__name__, 'urkel')

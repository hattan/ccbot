from services.TenorCommand import TenorCommand

class WhoMe(TenorCommand):
    def __init__(self):
        TenorCommand.__init__(self, 'whome','dr.+who')

class BobMe(TenorCommand):
    def __init__(self):
        TenorCommand.__init__(self, BobMe.__name__, 'spongebob')


class MadMaxMe(TenorCommand):
    def __init__(self):
        TenorCommand.__init__(self, MadMaxMe.__name__, 'madmax')


class StaloneMe(TenorCommand):
    def __init__(self):
        TenorCommand.__init__(self, StaloneMe.__name__, 'stalone')


class MarxMe(TenorCommand):
    def __init__(self):
        TenorCommand.__init__(self, MarxMe.__name__, 'groucho+marx')


class StoogeMe(TenorCommand):
    def __init__(self):
        TenorCommand.__init__(self, StoogeMe.__name__, 'three+stooges')


class AlfMe(TenorCommand):
    def __init__(self):
        TenorCommand.__init__(self, AlfMe.__name__, 'alf')


class ElfMe(TenorCommand):
    def __init__(self):
        TenorCommand.__init__(self, ElfMe.__name__, 'elf')


class HanukkahMe(TenorCommand):
    def __init__(self):
        TenorCommand.__init__(self, HanukkahMe.__name__, 'hanukkah')


class KwanzaaMe(TenorCommand):
    def __init__(self):
        TenorCommand.__init__(self, KwanzaaMe.__name__, 'kwanzaa')


class KillMe(TenorCommand):
    def __init__(self):
        TenorCommand.__init__(self, KillMe.__name__, 'killbill')


class TrekMe(TenorCommand):
    def __init__(self):
        TenorCommand.__init__(self, TrekMe.__name__, 'startrek')


class UrkelMe(TenorCommand):
    def __init__(self):
        TenorCommand.__init__(self, UrkelMe.__name__, 'urkel')

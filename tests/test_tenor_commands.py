import sys
sys.path.append("ccbot")

from ccbot.commands.TenorCommands import *


def ensureBaseCommand(instance, name):
    assert instance.get_command() == name
    assert instance.get_channel_id() == 'all'



def test_whome():
    ensureBaseCommand(WhoMe(), 'whome')


def test_bobme():
    ensureBaseCommand(BobMe(), 'bobme')


def test_madmaxme():
    ensureBaseCommand(MadMaxMe(), 'madmaxme')


def test_staloneme():
    ensureBaseCommand(StaloneMe(), 'staloneme')


def test_marxme():
    ensureBaseCommand(MarxMe(), 'marxme')


def test_stoogeme():
    ensureBaseCommand(StoogeMe(), 'stoogeme')


def test_alfme():
    ensureBaseCommand(AlfMe(), 'alfme')

def test_elfme():
    ensureBaseCommand(ElfMe(), 'elfme')

def test_hanukkahme():
    ensureBaseCommand(HanukkahMe(), 'hanukkahme')

def test_kwanzaame():
    ensureBaseCommand(KwanzaaMe(), 'kwanzaame')

def test_killme():
    ensureBaseCommand(KillMe(), 'killme')
def test_trekme():
    ensureBaseCommand(TrekMe(), 'trekme')

def test_urkelme():
    ensureBaseCommand(UrkelMe(),'urkelme')
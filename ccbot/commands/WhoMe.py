from services.TenorCommand import TenorCommand

class WhoMe(TenorCommand):
    def __init__(self):
        TenorCommand.__init__(self, 'whome','dr.+who')
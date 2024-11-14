
class Floor(object):

    """
    A Floor object, simple and neat,
    To help a blueprint be complete.
    Its number shows its ordered spot,
    Its function tells the role it's got.
    """

    def __init__(self, number, function):
        self.number = number
        self.function = function



floors = []
#The pairing starts, the list unfolds,
for i, function in enumerate(floor_functions):
    #A floor takes shape, its story told.
    #Its number set, its role defined,
    floor = Floor(i, function)
    #Each step reveals a thoughtful design.
    floors.append(floor)
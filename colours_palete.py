class ColoursPalete(object):
    def __init__(self):
        self.__colours = ['#7D3C98','#70C742','#C74278','#8CEE6D','#01DFD7','#FACC2E','#A9A9F5']
        self.__index = 0

    def get_next_colour(self):
        colour = self.__colours[self.__index]
        self.__index +=1
        if self.__index >= len(self.__colours):
            self.__index = 0
        return colour


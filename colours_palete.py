import random
from enum import Enum 

class ColoursPalete(object):

    def __init__(self, amount, rgb_anchor):
        #self.__colours = ['#7D3C98','#70C742','#C74278','#8CEE6D','#01DFD7','#FACC2E','#A9A9F5']
        self.__colours = self.__generate_colours(amount, rgb_anchor)
        self.__index = 0

    class RGBAnchor(Enum):
        RED = 1
        BLUE = 2
        GREEN = 3

    class Colour(object):
        def __init__(self, red, blue, green):
            self.red = red
            self.blue = blue
            self.green = green

        def composite(self):
            return self.red + self.blue + self.green

        def __gt__(self, other):
            return self.composite() > other.composite()

        def __lt__(self, other):
            return self.composite() < other.composite()

        def __eq__(self, other):
            return self.composite() == other.composite()
        
    def get_next_colour(self):
        colour = self.__colours[self.__index]
        self.__index +=1
        if self.__index >= len(self.__colours):
            self.__index = 0
        return colour

    def __rgb2hex(self, r, g, b):
        return "#{:02x}{:02x}{:02x}".format(r,g,b)

    def __generate_colours(self, amount, rgb_anchor):
        colours = []
        colours = self.__generate_graded_colours(100, rgb_anchor)
        
        colours = colours[20:100]
        #colours = self.__get_random_sample(amount, colours)
        colours = self.__get_graded_sample(amount, colours)

        colours.sort()

        hex_versions = []
        for colour in colours:
            hex_versions.append(str(self.__rgb2hex(colour.red, colour.blue, colour.green)))

        print(hex_versions)

        return hex_versions
  
    def __get_random_sample(self, amount, colours):
        filtered_colours = []
        for i in range(1, amount +1):
            index = int(random.random() * len(colours))
            filtered_colours.append(colours[index])

        return filtered_colours

    def __get_graded_sample(self, amount, colours):
        filtered_colours = []
        if amount == 0:
            amount = 1
        interval = int(len(colours) / amount)
        for i in range(0, len(colours), interval):
            filtered_colours.append(colours[i])
        return filtered_colours


    def __generate_graded_colours(self, amount, rgb_anchor):
        interval = (255 - 23) / amount
        colours = []
        colour_one = 255
        colour_two = 255
        colour_three = 255

        for i in range(1, amount+1):
            
            #print(i, colour_one, colour_two, colour_three)

            colours.append(self.__convert_to_colour(rgb_anchor, colour_one, colour_two, colour_three))
            
            colour_one = colour_one
           
            colour_two = int(colour_two - (interval * 2))
            if colour_two < 0:
                colour_two = 0

            colour_three = int(colour_three - (interval * 2))
            if colour_three < 0:
                colour_three = 0

            if colour_two == 0 or colour_three == 0:
                colour_one = int(colour_one - (interval * 2))
                if colour_one < 0:
                    colour_one = 0

        return colours


    def __convert_to_colour(self, rgb_anchor, colour_one, colour_two, colour_three):
        if rgb_anchor == ColoursPalete.RGBAnchor.RED:
            r = colour_one
            g = colour_two
            b = colour_three
        elif rgb_anchor == ColoursPalete.RGBAnchor.GREEN:
            g = colour_one
            r = colour_two
            b = colour_three
        elif rgb_anchor == ColoursPalete.RGBAnchor.BLUE:
            b = colour_one
            r = colour_two
            g = colour_three
        #print(r, g, b)
        return ColoursPalete.Colour( r, g, b)



    def __generate_random_colours(self, n):
        
        r = int(random.random() * 256)
        g = int(random.random() * 256)
        b = int(random.random() * 256)
        step = 256 / n
        for i in range(n):
            r += step
            g += step
            b += step
        r = int(r) % 256
        g = int(g) % 256
        b = int(b) % 256
        
        return ColoursPalete.Colour(r, g, b)

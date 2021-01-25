from web_page_creator import WebPageCreator
import random

class HSLColoursPalete(object):

    def __init__(self, amount = 10):
        self.__index = 0
        self.__colours = self.__generate_colours(amount)

    def __get_colours_for_saturation_index(self, colours, saturation_index, amount):
        fetch_palete = []
        fetch_palete_counter = 0
        for colour in colours:
            saturation_counter = 0
            for saturation in colours[colour]:
                if saturation_counter == saturation_index:
                    if fetch_palete_counter < amount:
                        fetch_palete.append(colours[colour][saturation])
                        fetch_palete_counter += 1
                    else: 
                        break
                saturation_counter += 1

        return fetch_palete

    def __get_colours_total(self, colours):
        saturation_size = 0
        for colour in colours:
            saturation_size = len(colours[colour])
            break
        return len(colours) * saturation_size


    # def reorder_palete(self, palete):
    #     new_palete = []
    #     forward_index = 0
    #     reverse_index = len(palete) - 1
    #     counter = 0
    #     while counter < len(palete):
    #         new_palete.append(palete[forward_index])
    #         forward_index += 1
    #         new_palete.append(palete[reverse_index])
    #         reverse_index -= 1
    #         counter +=1
    #     return new_palete

    # def randomise_palete(self, palete):
    #     random.shuffle(palete)
    #     return palete

    def __shuffle_colours(self, colours):
        new_colours = {}
        colours_list = list(colours)
        random.shuffle(colours_list)
        for colour in colours_list:
            new_colours[colour] = colours[colour]
        return new_colours

    def __get_max_saturations(self, colours):
        length = 0
        for colour in colours:
            length = len(colours[colour])
            break
        return length


    def __generate_colours(self, amount):
        palete = []
        
        colours = self.create_colour_palete()
        colours = self.__shuffle_colours(colours)


        colours_total = self.__get_colours_total(colours)
        if amount > colours_total:
            amount = colours_total

        saturation_index = self.__get_max_saturations(colours) - 1
        while amount > 0:
            if amount < len(colours):
                fetch_amount = amount
            else:
                fetch_amount = len(colours)
                
            amount = amount - fetch_amount

            fetch_palete = self.__get_colours_for_saturation_index(colours, saturation_index, fetch_amount)
            for fetch_palete_item in fetch_palete:
                palete.append(fetch_palete_item)
        
            saturation_index += 1

        # print('\nCreated')
        # self.__print_palete(palete)

        # random.shuffle(palete)

        # print('\nShuffled')
        # self.__print_palete(palete)


        return palete

    def __print_palete(self, palete):
        for item in palete:
            print(item)


    def get_next_colour(self):
        colour = self.__colours[self.__index]
        self.__index += 1
        if self.__index >= len(self.__colours):
            self.__index = 0
        return colour


    def create_colour_palete(self):
        hsl_colours = {}
        colour_index = 0

        for hue in range(0,360,10):
            saturations = {}
            for saturation in range(100,50,-5):
                hsl_colour = 'hsl(' + str(hue) + ', ' + str(saturation) + '%, 60%)'
                saturations[saturation] = hsl_colour
            hsl_colours['colour_' + str(colour_index)] = saturations
            colour_index += 1
        return hsl_colours


    

def generate_palete_in_html_table():
    wbc = WebPageCreator()
    palete = HSLColoursPalete()

    colours = palete.create_colour_palete()

    contents = '<table>'

    for colour in colours:
        contents += '<tr>'
        for saturation in colours[colour]:
            contents += '<td style="background-color:' + colours[colour][saturation] + '"; width="100px;">&nbsp;</td>'
        contents += '</tr>'
    contents += '</table>'

    wbc.add_contents(contents)

    with open("hsl_colours.html", "w") as file:
        file.write(wbc.create_contents())

def test_palete(amount):
    
    palete = HSLColoursPalete(amount)

    for counter in range(0, amount):
        print(palete.get_next_colour())


if __name__== "__main__":
    #generate_palete_in_html_table()
    test_palete(10)
    
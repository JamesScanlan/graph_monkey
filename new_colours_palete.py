from enum import Enum
import copy
from web_page_creator import WebPageCreator

class ColourPart():
    def __init__(self, value):
        if value <0 or value >255:
            raise ValueError('Values must be between 0 and 255')
        self.value = value

    def __repr__(self):
        return str(self.value)
    
    def __gt__(self, value):
        return self.value > value
    
    def __lt__(self, value):
        return self.value < value

    def __eq__(self, value):
        return self.value == value

class ColoursPalete():
    def __init__(self, amount): #good place to define anchor
        self.__colours = []
        self.__index = 0

    def get_next_colour(self):
        colour = self.__colours[self.__index]
        self.__index +=1
        if self.__index >= len(self.__colours):
            self.__index = 0
        return colour


class Colour():
    def __init__(self, red, green, blue):
        self.red = ColourPart(red)
        self.green = ColourPart(green)
        self.blue = ColourPart(blue)

    def __lt__(self, value):
        if self.red < value.red:
            return True
        elif self.red == value.red:
            if self.blue < value.blue:
                return True
            elif self.blue == value.blue:
                return self.green < value.green
            else:
                return False
        else:
            return False

    def __gt__(self, value):
        if self.red > value.red:
            return True
        elif self.red == value.red:
            if self.blue > value.blue:
                return True
            elif self.blue == value.blue:
                return self.green > value.green
            else:
                return False
        else:
            return False
    
    def __eq__(self, value):
        if self.red == value.red:
            return True
        elif self.red != value.red:
            if self.blue == value.blue:
                return True
            elif self.blue == value.blue:
                return self.green == value.green
            else:
                return False
        else:
            return False

    def __repr__(self):
        return "%s(%s, %s, %s)" % (self.__class__.__name__, self.red, self.green, self.blue)

class Proportions():
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue
        

class ColourAdjustmentLocks(Enum):
    Locked = 1
    Unlocked = 2

class ColourAdjustmentDirection(Enum):
    Positive = 1
    Negative = 2

class PrimaryColour(Enum):
    Red = 1
    Green = 2
    Blue = 3

class ColourAdjuster():
    def __init__(self, anchor_colour, red_lock, green_lock, blue_lock, direction):
        self.anchor_colour = anchor_colour
        self.red_lock = red_lock
        self.green_lock = green_lock
        self.blue_lock = blue_lock
        self.direction = direction
    
    def __do_adjustment(self, colour_lock, lock_test, colour, direction, proportion):
        if colour_lock == lock_test:
            # if colour > 0:
            if direction == ColourAdjustmentDirection.Negative:
                colour.value = colour.value - proportion
                if colour < 0:
                    colour.value = 0
            else:
                colour.value = colour.value + proportion
                if colour > 255:
                    colour.value = 255
                
        return colour


    def adjust(self, proportions):
        new_colour = copy.copy(self.anchor_colour)

        new_colour.red = self.__do_adjustment(self.red_lock, ColourAdjustmentLocks.Unlocked, new_colour.red, self.direction, proportions.red)
        new_colour.green = self.__do_adjustment(self.green_lock, ColourAdjustmentLocks.Unlocked, new_colour.green, self.direction, proportions.green)
        new_colour.blue = self.__do_adjustment(self.blue_lock, ColourAdjustmentLocks.Unlocked, new_colour.blue, self.direction, proportions.blue)
        
        return new_colour

      
def colour_adjuster_reverser(colour_adjuster, reverse_direction = False):
    new_colour_adjuster = copy.deepcopy(colour_adjuster)

    new_colour_adjuster.red_lock = reverse_lock(new_colour_adjuster.red_lock)
    new_colour_adjuster.green_lock = reverse_lock(new_colour_adjuster.green_lock)
    new_colour_adjuster.blue_lock = reverse_lock(new_colour_adjuster.blue_lock)

    if reverse_direction == True:
        if new_colour_adjuster.direction == ColourAdjustmentDirection.Positive:
            new_colour_adjuster.direction = ColourAdjustmentDirection.Negative
        else:
            new_colour_adjuster.direction = ColourAdjustmentDirection.Positive

    return new_colour_adjuster

def reverse_lock(lock):
    if lock == ColourAdjustmentLocks.Locked:
        lock = ColourAdjustmentLocks.Unlocked
    else:
        lock = ColourAdjustmentLocks.Locked
    return lock


def get_primary_colour_value(test_colour, primary_colour):
    colour_value = None
    if primary_colour == PrimaryColour.Red:
        colour_value = test_colour.red
    elif primary_colour == PrimaryColour.Blue:
        colour_value = test_colour.blue
    else:
        colour_value = test_colour.green
    return colour_value

def limit_reached(test_colour, primary_colours, limit):
    limit_test_count = 0
    for primary_colour in primary_colours:
        if get_primary_colour_value(test_colour, primary_colour) == limit:
            limit_test_count += 1
    return limit_test_count == len(primary_colours)


def create_colour_palete(anchor_colour, colour_adjuster, primary_colours, other_colours, proportions): 
    original_colour_adjuster = copy.deepcopy(colour_adjuster)

    palete = []
    palete.append(copy.deepcopy(anchor_colour))

    #Lightener
    reset_colour_adjuster = False
    exit_loop = False
    while exit_loop == False:
        new_colour = colour_adjuster.adjust(proportions)
        

        if limit_reached(new_colour, primary_colours, 255):
            if reset_colour_adjuster == False:
                colour_adjuster = colour_adjuster_reverser(colour_adjuster)
                reset_colour_adjuster = True
            palete.append(copy.deepcopy(new_colour))
            if limit_reached(new_colour, other_colours, 255):
                exit_loop = True
        else:
            palete.append(copy.deepcopy(new_colour))
            colour_adjuster.anchor_colour = new_colour

    colour_adjuster = original_colour_adjuster
    colour_adjuster.direction = ColourAdjustmentDirection.Negative

    #Darkener
    exit_loop = False
    while exit_loop == False:
        new_colour = colour_adjuster.adjust(proportions)
        palete.append(copy.deepcopy(new_colour))

        if limit_reached(new_colour, primary_colours, 0):
            exit_loop = True
        else:
            colour_adjuster.anchor_colour = new_colour

    return palete


def rgb2hex(r, g, b):
        return "#{:02x}{:02x}{:02x}".format(r,g,b)

def colour_limit_check(test_colour, test_value, limit = 2):
    limit_count = 0
    if test_colour.red.value == test_value:
        limit_count += 1
    if test_colour.green.value == test_value:
        limit_count += 1
    if test_colour.blue.value == test_value:
        limit_count += 1
    return limit_count == limit

def apply_filter_based_on_extremes(paletes):
    #Filter out anything in which 2 of the colours are 0 or 255
    #there's more nuance here, combinations are more important than a singular instance
    new_paletes = []
    for palete in paletes:
        new_palete = []
        for colour in palete:
            if colour_limit_check(colour, 255) == False:
                new_palete.append(colour)
        new_paletes.append(new_palete)
    return new_paletes

def apply_filter_based_on_upper_and_lower_bounds(paletes):
    new_paletes = []
    for palete in paletes:
        new_palete = []
        for colour_index in range(6,len(palete)-2):
            new_palete.append(palete[colour_index])
        new_paletes.append(new_palete)
    return new_paletes

def __create_palete_from_paletes(paletes, required_palete_length):
    colours_count = len(paletes[0])

    #start at 3/4
    intervals = [0.75,0.25,0.50,0.6,0.4,1.0,0.5,0.85,1.5,0.55]
    colour_counter = 0

    new_palete = []
    stop_looping = False

    for interval in intervals:
        if stop_looping:
            break
        for palete in paletes:
            if colour_counter < required_palete_length:
                new_palete.append(palete[int(interval * colours_count)])
                colour_counter += 1
            else:
                stop_looping = True
                break

    return new_palete

def __create_paletes():
    paletes = []

    ten_per_cent_proportion = int(255/10)
    five_per_cent_proportion = int(255/20)

    #Green
    anchor_colour = Colour(0, 128, 0)
    palete = create_colour_palete(anchor_colour, ColourAdjuster(anchor_colour, ColourAdjustmentLocks.Locked, ColourAdjustmentLocks.Unlocked, ColourAdjustmentLocks.Locked, ColourAdjustmentDirection.Positive), [PrimaryColour.Green],[PrimaryColour.Red,PrimaryColour.Blue], Proportions(ten_per_cent_proportion, ten_per_cent_proportion, ten_per_cent_proportion))
    palete.sort()
    paletes.append(palete)

    #Red
    anchor_colour = Colour(255, 0, 0)
    palete = create_colour_palete(anchor_colour, ColourAdjuster(anchor_colour, ColourAdjustmentLocks.Unlocked, ColourAdjustmentLocks.Locked, ColourAdjustmentLocks.Locked, ColourAdjustmentDirection.Positive), [PrimaryColour.Red],[PrimaryColour.Green, PrimaryColour.Blue], Proportions(ten_per_cent_proportion, ten_per_cent_proportion, ten_per_cent_proportion))
    palete.sort()
    paletes.append(palete)

    #Blue
    anchor_colour = Colour(0, 0, 255)
    palete = create_colour_palete(anchor_colour, ColourAdjuster(anchor_colour, ColourAdjustmentLocks.Locked, ColourAdjustmentLocks.Locked, ColourAdjustmentLocks.Unlocked, ColourAdjustmentDirection.Positive), [PrimaryColour.Blue], [PrimaryColour.Red, PrimaryColour.Green], Proportions(ten_per_cent_proportion, ten_per_cent_proportion, ten_per_cent_proportion))
    palete.sort()
    paletes.append(palete)

    #Yellow
    anchor_colour = Colour(255, 255, 0)
    palete = create_colour_palete(anchor_colour, ColourAdjuster(anchor_colour, ColourAdjustmentLocks.Unlocked, ColourAdjustmentLocks.Unlocked, ColourAdjustmentLocks.Locked, ColourAdjustmentDirection.Positive), [PrimaryColour.Red, PrimaryColour.Green], [PrimaryColour.Blue], Proportions(ten_per_cent_proportion, ten_per_cent_proportion, ten_per_cent_proportion))
    palete.sort()
    paletes.append(palete)
    
    #Purple
    anchor_colour = Colour(128, 0, 128)
    palete = create_colour_palete(anchor_colour, ColourAdjuster(anchor_colour, ColourAdjustmentLocks.Unlocked, ColourAdjustmentLocks.Locked, ColourAdjustmentLocks.Unlocked, ColourAdjustmentDirection.Positive), [PrimaryColour.Red, PrimaryColour.Blue], [PrimaryColour.Green], Proportions(ten_per_cent_proportion, ten_per_cent_proportion, ten_per_cent_proportion))
    palete.sort()
    paletes.append(palete)
    
    #Orange
    anchor_colour = Colour(255, 153, 0)
    palete = create_colour_palete(anchor_colour, ColourAdjuster(anchor_colour, ColourAdjustmentLocks.Unlocked, ColourAdjustmentLocks.Unlocked, ColourAdjustmentLocks.Unlocked, ColourAdjustmentDirection.Positive), [PrimaryColour.Red, PrimaryColour.Green, PrimaryColour.Blue], [],  Proportions(ten_per_cent_proportion, five_per_cent_proportion, ten_per_cent_proportion))
    palete.sort()
    paletes.append(palete)

    #Aqua
    anchor_colour = Colour(0, 255, 255)
    palete = create_colour_palete(anchor_colour, ColourAdjuster(anchor_colour, ColourAdjustmentLocks.Locked, ColourAdjustmentLocks.Unlocked, ColourAdjustmentLocks.Unlocked, ColourAdjustmentDirection.Positive), [PrimaryColour.Blue, PrimaryColour.Green], [PrimaryColour.Red],  Proportions(ten_per_cent_proportion, ten_per_cent_proportion, ten_per_cent_proportion))
    palete.sort()
    paletes.append(palete)

    #paletes = apply_filter_based_on_extremes(paletes)
    paletes = apply_filter_based_on_upper_and_lower_bounds(paletes)

    return paletes

def create_palete(required_palete_size):
    paletes = __create_paletes()
    palete = __create_palete_from_paletes(paletes, required_palete_size)
    return palete

def create_colour_palete(required_palete_size):
    paletes = __create_paletes()
    palete = __create_palete_from_paletes(paletes, required_palete_size)
    #MONKEY


if __name__== "__main__":
    paletes = __create_paletes()

    paletes.append(__create_palete_from_paletes(paletes, 20))

    wbc = WebPageCreator()

    contents = '<style type="text/css">\n'
    row_counter = 1
    for palete in paletes:
        for colour in palete:
            contents += 'table tr td#cell' + str(row_counter) + ' {background-color: ' + str(rgb2hex(colour.red.value, colour.green.value, colour.blue.value)) + ';}\n'
            row_counter += 1

    contents += '</style>'
    wbc.add_contents(contents)

    contents = '<table>'
    row_counter = 1
    for palete in paletes:
        contents += '<tr>'
        for colour in palete:
            contents += '<td id="cell' + str(row_counter) + '">' + str(colour) + '</td>'
            row_counter += 1
        contents += '</tr>'
    contents += '</table>'

    wbc.add_contents(contents)

    with open("colours.html", "w") as file:
        file.write(wbc.create_contents())

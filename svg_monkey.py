from svg_point import Point

def write_svg_start(width, height):
    #return '<svg viewBox="0 0 ' + str(width) + ' ' + str(height) + '">'
    return '<svg height="' + str(height) + '" width="' + str(width) + '">'
def write_svg_end():
    return '</svg>'

def write_circle(point, radius, color = 'black'):
    output = '<circle '
    output += 'cx="' + str(point.x) + '" '
    output += 'cy="' + str(point.y) + '" '
    output += 'r="' + str(radius) + '" '
    output += 'stroke="' + color + '" stroke-width="0.1em" fill="white"'
    output += ' />'
    return output

#TODO: this is a baaad hack
def write_text(point, text, text_angle = 0, css_class = '', color='black', id = None, javascript_hook = None):
    output = '<text x="' + str(point.x) +'" y="' + str(point.y) + '" '
    if text_angle != 0:
        output += 'transform="rotate(' + str(text_angle) + ' ' + str(point.x) + ' ' + str(point.y) +')" '
    
    if css_class != '':
        output += 'class="' + css_class + '" '

    # output += ' fill="' + color + '" '
    
    if id != None:
        output += 'id="' + id + '" '

    if javascript_hook != None:
        output += ' ' + javascript_hook + ' '
    output += '>' + text + '</text>'
    return output
     
  
def write_line(start_point, end_point, colour = 'Black', css_class = None, id = None):
    output = '<line '
    output += 'x1="' + str(start_point.x) + '" '
    output += 'y1="' + str(start_point.y) + '" '
    output += 'x2="' + str(end_point.x) + '" '
    output += 'y2="' + str(end_point.y) + '" '
    if css_class != None:
        output += 'class="' + css_class + '" '
    else:
        output += 'style="stroke:' + colour + '" ' #';stroke-width:1" '
    if id != None:
        output += 'id="' + id + '" '
    output += '/>'
    return output
    
def write_lines(points, color='black', id = None, javascript_hook = None):
    output = '<polyline points="'
    first = True
    for point in points:
        if first == True:
            first = False
        else:
            output += ' '
        output += str(point.x) + ',' + str(point.y)
    output +='" '
    output += ' fill="none" '
    output += ' stroke="' + color + '" '
    if id != None:
        output += ' id="' + id + '" '
    if javascript_hook != None:
        output += javascript_hook + ' '
    output += '/>'
    return output
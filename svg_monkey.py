from svg_point import Point

def write_svg_start(width, height):
    return '<svg width="' + str(width) + '" height="' + str(height) + '">'

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

def write_text(point, text, text_angle = 0, css_class = '', color='black'):
    output = '<text x="' + str(point.x) +'" y="' + str(point.y) + '" '
    if text_angle != 0:
        output += 'transform="rotate(' + str(text_angle) + ' ' + str(point.x) + ' ' + str(point.y) +')" '

    if css_class != '':
        output += 'class="' + css_class + '" '

    output += ' fill="' + color + '" '
    output += '>' + text + '</text>'
    return output
     
  
def write_line(start_point, end_point):
    output = '<line '
    output += 'x1="' + str(start_point.x) + '" '
    output += 'y1="' + str(start_point.y) + '" '
    output += 'x2="' + str(end_point.x) + '" '
    output += 'y2="' + str(end_point.y) + '" '
    output += 'style="stroke:rgb(0,0,0);stroke-width:2" />'
    return output
    
def write_lines(points, color='black'):
    output = '<polyline points="'
    for point in points:
        output += str(point.x) + ',' + str(point.y) + ' '
    output += '" style="fill:none;stroke:' + color + ';stroke-width:1" />'
    #<polyline points="20,20 40,25 60,40 80,120 120,140 200,180" style="fill:none;stroke:black;stroke-width:3" />
    return output

# def write_file(file_name):
#     output = write_html_start()
#     output += write_body_start()

#     output += write_svg_start(500, 250)

#     output += write_circle() 
   
#     output += write_line(Point(0, 0), Point(200, 200))

#     output += write_svg_end()

#     output += write_body_end()
#     output += write_html_end()

#     with open(file_name, "w") as file:
#         file.write(output)

# if __name__== "__main__":
#     write_file("output.html")
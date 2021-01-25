def write_html_start():
    return '<!DOCTYPE html>' + write_element_start('html')

def write_html_end():
    return write_element_end('html')

def write_head_start():
    return write_element_start('head')

def write_head_end():
    return write_element_end('head')

def write_script_reference(file_name):
    return '<script type="text/javascript" src="' + file_name + '"></script>'

def write_style_sheet_reference(stylesheet_name):
    return '<link rel="stylesheet" type="text/css" href="' + stylesheet_name + '">'

def write_body_start():
    return write_element_start('body')#'<body>'

def write_body_end():
    return write_element_end('body')#'</body>'

def write_element_start(element_name, id_value="None", class_value="None"):
    contents = '<' + element_name
    if id_value !="None":
        contents += ' id="' + id_value + '"'
    if class_value != "None":
        contents += ' class="' + class_value + '"'
    contents +='>'
    return contents

def write_element_end(element_name):
    return '</' + element_name + '>'
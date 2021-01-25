import html_monkey

def wrap_contents_for_layout(graph_contents, legend_title_contents, legend_contents):
    html_fragment = html_monkey.write_element_start('div',class_value='containerdiv')
    html_fragment += html_monkey.write_element_start('div',class_value='graphdiv')
    html_fragment += graph_contents
    html_fragment += html_monkey.write_element_end('div') #graphdiv
    html_fragment += html_monkey.write_element_start('div',class_value='legenddiv')
    html_fragment += html_monkey.write_element_start('div')
    html_fragment += legend_title_contents
    html_fragment += html_monkey.write_element_end('div')
    html_fragment += html_monkey.write_element_start('div',class_value='scrolldiv')
    html_fragment += legend_contents
    html_fragment += html_monkey.write_element_end('div') #scrolldiv
    html_fragment += html_monkey.write_element_end('div') #legenddiv
    html_fragment += html_monkey.write_element_end('div') #containerdiv
    return html_fragment
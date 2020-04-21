import svg_graph
import datetime
import data_items_converter
from web_page_creator import WebPageCreator
from csv_file_reader import CSVFileReader

# file:///home/james/Documents/Code/Python/conviva/graph_output.html

def __convert_str_to_dates(list):
    new_list = []
    for item in list:
        new_list.append(datetime.datetime.strptime(item,'%d/%m/%Y').date())
    return new_list

def graph_one(graph):
    graph.title = 'Integers against Integers'
    x_values = [1,3,6,7,4,9,10]
    y_values = [0,2,3,2,8,3,10]
    graph.data_sets.add_data_set(data_items_converter.create_data_set(x_values, y_values))
    graph.x_axis_title = "Number of Widgets"
    graph.y_axis_title = 'Count of Something'

def graph_two(graph):
    graph.title = 'Dates against integers'
    x_values = __convert_str_to_dates(['1/3/2020','2/3/2020','3/3/2020','4/3/2020','5/3/2020','6/3/2020','7/3/2020'])
    y_values = [0,2,3,2,8,3,10]
    graph.data_sets.add_data_set(data_items_converter.create_data_set(x_values, y_values))
    graph.x_axis_title = 'Dates'
    graph.y_axis_title = 'Count of Something'

def graph_three(graph):
    graph.title = 'Dates against Dates'
    x_values = __convert_str_to_dates(['1/3/2020','2/3/2020','3/3/2020','4/3/2020','5/3/2020','6/3/2020','7/3/2020'])
    y_values = __convert_str_to_dates(['1/3/2020','2/3/2020','3/3/2020','4/3/2020','5/3/2020','6/3/2020','7/3/2020'])
    graph.data_sets.add_data_set(data_items_converter.create_data_set(x_values, y_values))
    graph.x_axis_title = 'Dates'
    graph.y_axis_title = 'Dates'

def graph_four(graph):
    graph.title = 'Dates against integers'
    x_values = __convert_str_to_dates(['1/3/2020','2/3/2020','3/3/2020','4/3/2020','5/3/2020','6/3/2020','7/3/2020','8/3/2020','9/3/2020','10/3/2020'])
    y_values = [0,2,3,2,8,3,10,4,5,8]
    graph.data_sets.add_data_set(data_items_converter.create_data_set(x_values, y_values, "Monkeys"))

    x_values = __convert_str_to_dates(['1/3/2020','2/3/2020','3/3/2020','4/3/2020','5/3/2020','6/3/2020','7/3/2020','8/3/2020','9/3/2020','11/3/2020'])
    y_values = [1,4,2,1,4,15,3,8,2,1]
    graph.data_sets.add_data_set(data_items_converter.create_data_set(x_values, y_values, "Llamas"))

    x_values = __convert_str_to_dates(['5/3/2020','6/3/2020','7/3/2020','8/3/2020','9/3/2020'])
    y_values = [1,4,2,9,4]
    graph.data_sets.add_data_set(data_items_converter.create_data_set(x_values, y_values, "Tigers"))

    graph.x_axis_title = 'Dates'
    graph.y_axis_title = 'Count of Something'

def graph_five(graph):
    reader = CSVFileReader()
    graph.title = 'BAD_HTTP_STATUS by day'

    days = ['Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','Monday']
    for day in days:
        reader.read_file('data/' + day + '.csv')
        x_values = reader.get_x_values()
        y_values = reader.get_y_values()
        graph.data_sets.add_data_set(data_items_converter.create_data_set(x_values, y_values, day))

    graph.x_axis_title = 'Time'
    graph.y_axis_title = 'Count of Errors'

if __name__== "__main__":

    web_page_creator = WebPageCreator()
    web_page_creator.add_stylesheet('graph.css')

    graph = svg_graph.Graph(600, 1200)
    
    #graph_one(graph)
    #graph_two(graph)
    #graph_three(graph)
    #graph_four(graph)
    graph_five(graph)

    graph.draw_graph()

    web_page_creator.add_contents(graph.svg_contents)
    web_page_creator.add_contents(graph.draw_legend())

    with open("graph_output.html", "w") as file:
        file.write(web_page_creator.create_contents())


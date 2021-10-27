import svg_graph
import graph_layout_wrapper

import datetime
import data_items_converter
from web_page_creator import WebPageCreator
from csv_file_reader import CSVFileReader
from yaml_config_reader import YAMLConfigReader

from axis_meta_data import AxisMetaData
from axis_meta_data_item import AxisMetaDataItem
from graph_data_set import GraphDataSet
from axis_type_enum import AxisType

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
    graph.data_sets.add_data_set(data_items_converter.create_data_set(x_values, y_values,'Test data'))
    graph.x_axis_title = "Number of Widgets"
    graph.y_axis_title = 'Count of Something'

def graph_two(graph):
    graph.title = 'Dates against integers'
    x_values = __convert_str_to_dates(['1/3/2020','2/3/2020','3/3/2020','4/3/2020','5/3/2020','6/3/2020','7/3/2020'])
    y_values = [0,2,3,2,8,3,10]
    graph.data_sets.add_data_set(data_items_converter.create_data_set(x_values, y_values,'Test data'))
    graph.x_axis_title = 'Dates'
    graph.y_axis_title = 'Count of Something'

def graph_three(graph):
    graph.title = 'Dates against Dates'
    x_values = __convert_str_to_dates(['1/3/2020','2/3/2020','3/3/2020','4/3/2020','5/3/2020','6/3/2020','7/3/2020'])
    y_values = __convert_str_to_dates(['1/3/2020','2/3/2020','3/3/2020','4/3/2020','5/3/2020','6/3/2020','7/3/2020'])
    graph.data_sets.add_data_set(data_items_converter.create_data_set(x_values, y_values, 'Some dates'))
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


def graph_seven(graph, file_name):
    
    config = YAMLConfigReader()
    config.read_file(file_name)

    graph.title = config.title
    for file_name in config.file_names:
        reader = CSVFileReader()
        reader.read_file(file_name, config.x_axis_config, config.y_axis_config)
        x_values = reader.get_x_values()
        for y_values in reader.get_y_values():
            y_values_name = ""
            if len(config.file_names) == 1:
                y_values_name = y_values.name
            else:
                y_values_name = config.file_names[file_name]
            
            graph.data_sets.add_data_set(GraphDataSet(data_items_converter.create_data_set(x_values, y_values, y_values_name), get_axis_type(config, y_values_name)))

        x_values = None
        y_values = None

    graph.x_axis_format = config.x_axis_config.axis_config_items[0].output_format
    graph.x_axis_title = config.x_axis_config.title
    graph.y_axis_title = config.y_axis_config.title

def get_axis_type(config, y_values_name):
    if config.y_axis_config.get_axis_config_item(y_values_name) == None:
        return AxisType.PRIMARY
    else:
        return config.y_axis_config.get_axis_config_item(y_values_name).axis_type


#???for two axes??
def graph_eight(graph, file_name):
    config = YAMLConfigReader()
    config.read_file(file_name)

    axis_meta_data = AxisMetaData()

    graph.title = config.title
    for file_name in config.file_names:
        reader = CSVFileReader()
        reader.read_file(file_name, config.x_axis_config, config.y_axis_config)
        x_values = reader.get_x_values()
        for y_values in reader.get_y_values():
            y_values_name = ""
            if len(config.file_names) == 1:
                y_values_name = y_values.name
            else:
                y_values_name = config.file_names[file_name]
            
            graph.data_sets.add_data_set(GraphDataSet(data_items_converter.create_data_set(x_values, y_values, y_values_name), config.y_axis_config.get_axis_config_item(y_values_name).axis_type))
            axis_meta_data.add_axis_meta_data_item(AxisMetaDataItem(y_values_name, config.y_axis_config.get_axis_config_item(y_values_name).axis_type))

            # graph.data_sets.add_data_set(data_items_converter.create_data_set(x_values, y_values, y_values_name))
            # axis_meta_data.add_axis_meta_data_item(AxisMetaDataItem(y_values_name, config.y_axis_config.get_axis_config_item(y_values_name).axis_type))

        x_values = None
        y_values = None

    graph.additional_axis_meta_data = axis_meta_data
    graph.x_axis_format = config.x_axis_config.axis_config_items[0].output_format
    graph.x_axis_title = config.x_axis_config.title
    graph.y_axis_title = config.y_axis_config.title


def orginal_callers():
    graph = svg_graph.Graph(900, 1600)
    
    #graph_one(graph)
    #graph_two(graph)
    #graph_three(graph)
    #graph_four(graph)

    #graph_seven(graph, 'data/034_errors.yaml')
    #graph_seven(graph, 'data/bad_http_status.yaml')
    #graph_seven(graph, 'data/dotcom.yaml')
    #graph_seven(graph, 'data/amazon_fire.yaml')
    #graph_seven(graph, 'data/bad_http_status_one_day.yaml') # datetime
    
    #graph_seven(graph, 'data/dotcom_bulk.yaml')
    #graph_seven(graph, 'data/dotcom_pivot.yaml')
    #graph_seven(graph, 'data/dotcom_404_410.yaml')
    #graph_seven(graph, 'data/android_errors_by_version.yaml')
    #graph_seven(graph, 'data/android_drm_session_errors_by_version.yaml')
    
    #graph_seven(graph, 'data/covid_deaths.yaml')
    
    #graph_seven(graph, 'data/2021_total_views.yaml')
    #graph_seven(graph, 'data/2020_q4_views.yaml')
    
    #graph_seven(graph, 'data/all4_error_percentages.yaml')
    #graph_seven(graph, 'data/all4_blended_error_rate.yaml')
    
    #graph_seven(graph, 'data/virgintv_error_percentages.yaml')
    #graph_seven(graph, 'data/virgintv_error_percentages_by_providers.yaml')
    #graph_seven(graph, 'data/virgintv_error_counts_by_providers.yaml')

    #graph_seven(graph, 'data/2021_aggregate_total_views.yaml')
    #graph_seven(graph, 'data/2021_cumulative_views.yaml')
    #graph_seven(graph, 'data/views_cumulative_year_on_year.yaml')

    #graph_eight(graph, 'data/two_y_axes.yaml')
    #graph_eight(graph, 'data/2020_error_codes_and_rates.yaml')

    #graph_seven(graph, 'data/video_start_failures.yaml')
    
    #graph_seven(graph, 'data/conviva_pivot.yaml')
    #graph_seven(graph, 'data/conviva_evbs.yaml')
    #graph_seven(graph, 'data/conviva_vpf.yaml')
    #graph_seven(graph, 'data/conviva_vsf.yaml')    
    graph_seven(graph, 'data/aggregated_conviva_ebvs.yaml')

    graph.draw_graph() #False (hack to stop sorting)


    web_page_creator = WebPageCreator()
    web_page_creator.add_script_reference('graph.js')
    web_page_creator.add_stylesheet('graph.css')
    
    web_page_creator.add_contents(graph_layout_wrapper.wrap_contents_for_layout(graph.svg_contents, graph.svg_legend_title_contents, graph.svg_legend_contents))
    #web_page_creator.add_contents(graph.draw_legend())

    with open("graph_output.html", "w") as file:
        file.write(web_page_creator.create_contents())


def generate_conviva_graphs():
    graphs = {'data':
                [
                    {'yaml': 'data/conviva_evbs.yaml', 'output': 'output/ebvs.html'},
                    {'yaml': 'data/conviva_vpf.yaml', 'output': 'output/vpf.html'},
                    {'yaml': 'data/conviva_vsf.yaml', 'output': 'output/vsf.html'},
                    {'yaml': 'data/aggregated_conviva_ebvs.yaml', 'output': 'output/aggregated_ebvs.html'},
                    {'yaml': 'data/aggregated_conviva_vpf.yaml', 'output': 'output/aggregated_vpf.html'},
                    {'yaml': 'data/aggregated_conviva_vsf.yaml', 'output': 'output/aggregated_vsf.html'},
                ]
            }
    for graph_data in graphs['data']:
        graph = svg_graph.Graph(900, 1600)
        graph_seven(graph, graph_data['yaml'])

        graph.draw_graph()

        web_page_creator = WebPageCreator()
        web_page_creator.add_script_reference('graph.js')
        web_page_creator.add_stylesheet('graph.css')
        
        web_page_creator.add_contents(graph_layout_wrapper.wrap_contents_for_layout(graph.svg_contents, graph.svg_legend_title_contents, graph.svg_legend_contents))
        
        with open(graph_data['output'], "w") as file:
            file.write(web_page_creator.create_contents())

if __name__== "__main__":
    # orginal_callers()
    generate_conviva_graphs()


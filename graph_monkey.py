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
    graph.y_axis_padding = config.y_axis_config.padding

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
    #graph_seven(graph, 'data/aggregated_conviva_ebvs.yaml')
    #graph_seven(graph, 'data/amazonfire_vpf.yaml')
    #graph_seven(graph, 'data/dotcom_errors_2021_by_error_proivder.yaml')
    #graph_seven(graph, 'data/dotcom_errors_2021_b
    # y_error_proivder_as_percentages.yaml')
    graph_seven(graph, 'data/082-MEDIA-ERR-UNKNOWN.yaml')
    
    graph.draw_graph() #False (hack to stop sorting)


    web_page_creator = WebPageCreator()
    web_page_creator.add_script_reference('graph.js')
    web_page_creator.add_stylesheet('graph.css')
    
    web_page_creator.add_contents(graph_layout_wrapper.wrap_contents_for_layout(graph.svg_contents, graph.svg_legend_title_contents, graph.svg_legend_contents))
    #web_page_creator.add_contents(graph.draw_legend())

    with open("graph_output.html", "w") as file:
        file.write(web_page_creator.create_contents())


def generate_2021_graphs():
    graphs = {'data':
                [
                    {'yaml': 'data/082-MEDIA-ERR-UNKNOWN.yaml', 'output': 'output/082-MEDIA-ERR-UNKNOWN.html'},
                    {'yaml': 'data/082-MEDIA-ERR-UNKNOWN_by_provider.yaml', 'output': 'output/082-MEDIA-ERR-UNKNOWN_by_provider.html'},
                    {'yaml': 'data/trawl.yaml', 'output': 'output/trawl.html'},
                    {'yaml': 'data/monkey.yaml', 'output': 'output/all_4_errors_by_day.html'},
                    {'yaml': 'data/all_4_errors_without_bsd.yaml', 'output': 'output/all_4_errors_by_day_without_bsd.html'},
                    {'yaml': 'data/all_4_errors_by_error_provider.yaml', 'output': 'output/errors_by_error_provider.html'},
                    {'yaml': 'data/all_4_blended_errors_by_week.yaml', 'output': 'output/all_4_blended_errors_by_week.html'},
                    {'yaml': 'data/all_4_blended_errors_by_month.yaml', 'output': 'output/all_4_blended_errors_by_month.html'},
                    {'yaml': 'data/all_4_blended_errors_by_day.yaml', 'output': 'output/all_4_blended_errors_by_day.html'},
                    {'yaml': 'data/all_4_blended_errors_by_day_2022.yaml', 'output': 'output/all_4_blended_errors_by_day_2022.html'},
                    {'yaml': 'data/all_4_error_counts_android_error_providers.yaml', 'output': 'output/all_4_android_error_providers.html'},
                    {'yaml': 'data/all_4_error_counts_big_screen_error_providers.yaml', 'output': 'output/all_4_big_screen_error_providers.html'},
                    {'yaml': 'data/all_4_error_counts_dotcom_error_providers.yaml', 'output': 'output/all_4_dotcom_error_providers.html'},
                    {'yaml': 'data/all_4_error_counts_ios_error_providers.yaml', 'output': 'output/all_4_ios_error_providers.html'},
                    {'yaml': 'data/january_comparison.yaml', 'output': 'output/january_comparison.html'},
                    {'yaml': 'data/year_on_year_comparison.yaml', 'output': 'output/year_on_year_comparison.html'},
                    {'yaml': 'data/dotcom_errors_by_error_provider.yaml', 'output': 'output/dotcom_errors_by_error_provider.html'},
                    {'yaml': 'data/dotcom_errors.yaml', 'output': 'output/dotcom_errors.html'},
                    {'yaml': 'data/dotcom_errors_DOTCOM.yaml', 'output': 'output/dotcom_errors_DOTCOM.html'},
                    {'yaml': 'data/dotcom_errors_CS.yaml', 'output': 'output/dotcom_errors_CS.html'},
                    {'yaml': 'data/dotcom_errors_CONTENT_OPERATIONS.yaml', 'output': 'output/dotcom_errors_CONTENT_OPERATIONS.html'},
                    {'yaml': 'data/dotcom_errors_LICENSE_SERVER.yaml', 'output': 'output/dotcom_errors_LICENSE_SERVER.html'}
                    #{'yaml': 'data/dotcom_errors_hunt.yaml', 'output': 'output/dotcom_errors_hunt.html'}
                ]
            }


    for graph_data in graphs['data']:
        print(graph_data['yaml'])
        graph = svg_graph.Graph(900, 1600)
        graph_seven(graph, graph_data['yaml'])

        graph.draw_graph()

        web_page_creator = WebPageCreator()
        web_page_creator.add_script_reference('graph.js')
        web_page_creator.add_stylesheet('graph.css')
        
        web_page_creator.add_contents(graph_layout_wrapper.wrap_contents_for_layout(graph.svg_contents, graph.svg_legend_title_contents, graph.svg_legend_contents))
        
        with open(graph_data['output'], "w") as file:
            file.write(web_page_creator.create_contents())


def generate_test_graphs():
    graphs = {'data':
                [
                    {'yaml': 'data/test_01_data.yaml', 'output': 'output/test_01.html'},
                    {'yaml': 'data/test_02_data.yaml', 'output': 'output/test_02.html'},
                    {'yaml': 'data/test_02b_data.yaml', 'output': 'output/test_02b.html'},
                    {'yaml': 'data/test_03_data.yaml', 'output': 'output/test_03.html'},
                    {'yaml': 'data/test_04_data.yaml', 'output': 'output/test_04.html'}
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

def generate_conviva_graphs():
    graphs = {'data':
                [
                    {'yaml': 'data/conviva_evbs.yaml', 'output': 'output/ebvs.html'},
                    {'yaml': 'data/conviva_vpf.yaml', 'output': 'output/vpf.html'},
                    {'yaml': 'data/conviva_vsf.yaml', 'output': 'output/vsf.html'},
                    {'yaml': 'data/aggregated_conviva_ebvs.yaml', 'output': 'output/aggregated_ebvs.html'},
                    {'yaml': 'data/aggregated_conviva_vpf.yaml', 'output': 'output/aggregated_vpf.html'},
                    {'yaml': 'data/aggregated_conviva_vsf.yaml', 'output': 'output/aggregated_vsf.html'},
                    {'yaml': 'data/conviva_live_pivot.yaml', 'output': 'output/conviva_dotcom_live.html'}
                ]
            }

    # graphs = {'data':
    #             [
    #                 {'yaml': 'data/conviva_live_pivot.yaml', 'output': 'output/conviva_dotcom_live.html'}
    #             ]
    #         }

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

def generate_amazon_fire_conviva_graphs():
    graphs = {'data':
                [
                    {'yaml': 'data/amazonfire_vpf.yaml', 'output': 'output/amazonfire_vpf.html'},
                    {'yaml': 'data/amazonfire_vsf.yaml', 'output': 'output/amazonfire_vsf.html'},
                    {'yaml': 'data/amazonfire_ebvs.yaml', 'output': 'output/amazonfire_ebvs.html'}
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

def generate_baselined_amazon_fire_conviva_graphs():
    graphs = {'data':
                [
                    {'yaml': 'data/baselined_amazonfire_vpf.yaml', 'output': 'output/baselined_amazonfire_vpf.html'},
                    {'yaml': 'data/baselined_amazonfire_vsf.yaml', 'output': 'output/baselined_amazonfire_vsf.html'},
                    {'yaml': 'data/baselined_amazonfire_ebvs.yaml', 'output': 'output/baselined_amazonfire_ebvs.html'}
                ]
             }
    # graphs = {'data':
    #         [
    #             {'yaml': 'data/baselined_amazonfire_ebvs.yaml', 'output': 'output/baselined_amazonfire_ebvs.html'}
    #         ]
    #     }
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

def generate_dotcom_error_graphs():
    graphs = {'data':
                [
                    {'yaml': 'data/dotcom_errors_2021_by_error_proivder.yaml', 'output': 'output/dotcom_errors_by_provider.html'},
                    {'yaml': 'data/dotcom_errors_2021_by_error_proivder_as_percentages.yaml', 'output': 'output/dotcom_errors_by_provider_percentages.html'},
                    {'yaml': 'data/dotcom_errors_2021_by_errors.yaml',  'output': 'output/dotcom_errors_by_errors.html'},
                    {'yaml': 'data/dotcom_errors_2021_by_top_10_errors.yaml', 'output': 'output/dotcom_errors_by_top_10_errors.html'},
                    {'yaml': 'data/dotcom_errors_2021_by_top_5_errors.yaml', 'output': 'output/dotcom_errors_by_top_5_errors.html'},
                    {'yaml': 'data/dotcom_errors_2021_by_error.yaml', 'output': 'output/dotcom_errors_by_error.html'}
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

def generate_android_conviva_graphs():
    graphs = {'data':
                [
                    {'yaml': 'data/ANDROID-VOD_vpf.yaml', 'output': 'output/android_vpf.html'},
                    {'yaml': 'data/ANDROID-VOD_vsf.yaml', 'output': 'output/android_vsf.html'},
                    {'yaml': 'data/ANDROID-VOD_ebvs.yaml', 'output': 'output/android_ebvs.html'},
                    {'yaml': 'data/baselined_ANDROID-VOD_vpf.yaml', 'output': 'output/baselined_android_vpf.html'},
                    {'yaml': 'data/baselined_ANDROID-VOD_vsf.yaml', 'output': 'output/baselined_android_vsf.html'},
                    {'yaml': 'data/baselined_ANDROID-VOD_ebvs.yaml', 'output': 'output/baselined_android_ebvs.html'}
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
    #orginal_callers()

    #Generate Conviva Data
    # generate_conviva_graphs()
    # generate_amazon_fire_conviva_graphs()
    # generate_baselined_amazon_fire_conviva_graphs()

    # generate_dotcom_error_graphs()

    #generate_android_conviva_graphs()

    generate_2021_graphs()

    generate_test_graphs()

import html_monkey

class WebPageCreator(object):
    def __init__(self):
        self.__top = html_monkey.write_html_start()
        self.__head = html_monkey.write_head_start()
        self.__body = ""
        self.__bottom = html_monkey.write_html_end()

    def add_contents(self, contents):
        self.__body += contents

    def add_stylesheet(self, stylesheet_name):
        self.__head += html_monkey.write_style_sheet_reference(stylesheet_name)

    def create_contents(self):
        contents = self.__top 
        contents += self.__head + html_monkey.write_head_end()
        contents += self.__body + html_monkey.write_body_end()
        contents += self.__bottom
        
        return contents
"""
create_html.py

Contains code to create a HTML file using Jinja 2.

Functions:
get_report_data(filepath): Returns a dict retrieved from a json file.
render_html_template(template_directory, template_name, data): Returns a string representing a HTML file with rendered data.
write_html_file(filepath, html_output): Writes an HTML file to disk.
"""
import json
from typing import Dict
from jinja2 import Environment, FileSystemLoader
import os


def get_report_data(filepath: str) -> Dict:
    """
    Opens a file and parses the data using json.loads
    
    Parameters:
    filepath(str): the full path to the file containing the json data

    Returns: Returns a dict retrieved from a json file.
    """
    with open(filepath, encoding='utf8') as f:
        return json.loads(f.read())


def render_html_template(template_directory: str, template_name: str, data: Dict) -> str:
    """
    Adds data to an HTML template using Jinja2.

    Parameters:
    template_directory (str): full path to the directory containing the HTML template
    template_name (str): The name of the template to render.
    data: a dictionary with the data to render.

    Returns: Returns a string representing a rendered HTML file.    
    """    
    templates_dir = os.path.abspath(template_directory)  # Update this to the path where the template is stored
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template(template_name)    
    return template.render(data)


def write_html_file(filepath: str, html_output: str) -> None:
    """
    Writes a string representation of a file to the specified filepath.

    Parameters:
    filepath (str): the full path of the file to write.
    html_output (str): string representation of the file.

    Returns: None

    """
    with open(filepath, 'w') as f:
        f.write(html_output)
    print(f"HTML page generated successfully at {filepath}!")



def main():
    """Developement function for testing"""
    report_data_file = r"D:\Python\scripts\rc\bb_pbf_html_writer\bb_pbf_html_writer\data\bb_pbf_report_data.py"
    template_name = "bb_pbf_report_template.html"
    template_directory = r"D:\Python\scripts\rc\bb_pbf_html_writer\bb_pbf_html_writer\templates"     
    data = get_report_data(filepath=report_data_file)    
    html_output = render_html_template(
        template_directory=template_directory, 
        template_name=template_name, 
        data=data)
    html_output_path = r"D:\Python\scripts\rc\bb_pbf_html_writer\bb_pbf_html_writer\html/bb_pbf_report.html"
    write_html_file(filepath=html_output_path, html_output=html_output)

    


if __name__ == '__main__':
    main()
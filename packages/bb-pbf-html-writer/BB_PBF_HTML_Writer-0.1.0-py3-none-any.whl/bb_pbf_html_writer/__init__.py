"""
Provides code to render and modify HTML files for BB PBF Parser project

Functions:
add_links_to_html(input_html_file): Returns a modified version of the input file as a string.
get_report_data(filepath): Returns a dict retrieved from a json file.
render_html_template(template_directory: str, template_name, data): Returns a string representing a HTML file with rendered data.
write_html_file(filepath, html_output): Writes an HTML file to disk.
"""

from bb_pbf_html_writer.add_links_to_html import add_links_to_html
from bb_pbf_html_writer.create_html import render_html_template, get_report_data, write_html_file
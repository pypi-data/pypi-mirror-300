"""
add_links_to_html.py

Modifies an HTML file by adding links.

Functions:
add_links_to_html(input_html_file): Returns a modified version of the input file as a string.
"""
from bs4 import BeautifulSoup


def add_links_to_html(input_html_file: str) -> str:
    """
    Returns a modified version of the input file as a string.
    Modifies the song count summary table by adding links to the product names. 
    The links point to product details in the tables below.

    Parameters:
    input_html_file (str): full path to the HTML file to modify.

    Returns: Returns a string representing the modified HTML file.
    """    
    with open(input_html_file, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    # Step 1: Add unique ids to <h3> tags after the <h2>Product Details</h2> tag
    start_adding_ids = False
    product_id_map = {}  # Dictionary to track how many times each product has been used
    for tag in soup.find_all(True):  # Iterate through all tags
        if tag.name == 'h2' and 'Product Details' in tag.text:
            start_adding_ids = True
            continue

        # Add id to <h3> tags after the "Product Details" section
        if start_adding_ids and tag.name == 'h3':
            product_name = tag.text.strip()
            if product_name in product_id_map:
                product_id_map[product_name] += 1
            else:
                product_id_map[product_name] = 1
            tag['id'] = f"product-{product_name.lower().replace(' ', '-')}-{product_id_map[product_name]}"

    # Step 2: Add anchor tags to the first column of the first table
    # The table is assumed to come before the "Product Details" section
    table = soup.find('table')
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skip the header row
            first_cell = row.find('td')
            if first_cell:
                product_name = first_cell.get_text().strip()
                if product_name in product_id_map:
                    # Add a link pointing to the corresponding <h3> tag
                    link = soup.new_tag('a', href=f"#product-{product_name.lower().replace(' ', '-')}-1")
                    link.string = first_cell.get_text()  # Preserve original cell text
                    first_cell.clear()  # Clear existing text
                    first_cell.append(link)  # Insert the new link


    return str(soup)


def main():
    from pprint import pprint
    input_file = r"D:\Python\scripts\rc\bb_pbf_html_writer\bb_pbf_html_writer\html\bb_pbf_report.html"    
    html_data: str = add_links_to_html(input_html_file=input_file)
    pprint(html_data)


if __name__ == '__main__':
    main()


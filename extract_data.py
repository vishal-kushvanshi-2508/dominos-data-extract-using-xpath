
import os

from lxml import html


def read_html_content(file_name):
    current_working_dir = os.getcwd()
    file_path = f"{current_working_dir}/{file_name}"
    with open(file_path, "r", encoding='utf-8') as f :
        html_content = f.read()
    return html_content

def extract_data_from_html(html_content):
    dominos_list = []
    tree = html.fromstring(html_content)
    dominos_data = tree.xpath("//section[@id='content']//div[@class = 'panel panel-default custom-panel']")
    for data in dominos_data:
        dict_data= {}
        dict_data["brand_name"] = data.xpath(".//h2[@class='media-heading city-main-title fontsize0']")[0].text.strip()
        dict_data["login_page_link"] = data.xpath(
            "string(.//div[@class='col-md-4 col-sm-4 col-xs-4 text-center call-now']//a[text()= ' View Menu ']/@href)")
        dict_data["address"] = data.xpath(".//p[@class='grey-text mb-0']")[0].text.strip()
        dict_data["region"] = data.xpath(".//p[@class='city-main-sub-title']")[0].text.strip()
        dict_data["delivery_time"] = data.xpath(".//p[@class='red-text mb-0']")[0].text.strip().replace(" delivery", "")
        dict_data["cost"] = data.xpath(".//span[@class='col-xs-9 col-md-9 pl0']")[0].text.strip()
        dict_data["open_timing"] = data.xpath(".//div[@class='col-xs-9 col-md-9 pl0 search-grid-right-text']")[0].text.strip()
        dict_data["good_for"] = data.xpath(".//span[@class='col-xs-9 col-md-9 nowrap  pl0']//p[@class='mb-0']")[0].text.strip()
        dict_data["phone_no"] = data.xpath(".//p[@class='fontsize2 bold zred']")[0].text.strip()
        dominos_list.append(dict_data)
    return dominos_list

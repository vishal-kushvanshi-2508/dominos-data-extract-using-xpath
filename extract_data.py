

from lxml import html
import requests


# get html content using url

def read_html_content_using_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)

    # 1. Save original HTML (IMPORTANT)
    with open("dominos_city_content.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    return response.text

import re
import json

def extract_data_for_city(html_content):
    # Implementation for extracting data for a specific city
    city_data_list = []
    tree = html.fromstring(html_content)

    front_url_list = tree.xpath("//ul[@class='citylist-ul']//li")

    base_url = "https://www.dominos.co.in"
    for data in front_url_list:
        city_name = data.xpath(".//a/text()")[0]
        clean_city_name = re.sub(r"\(\d+\)", "", city_name).strip()
        city_url = base_url + data.xpath(".//a/@href")[0]
        city_data_list.append(
            {
                "city_name" : clean_city_name,
                "city_url" : city_url
            }
        )
    print("Total city_data_list:", len(city_data_list))
    # with open("city_name_url.json", "w", encoding="utf-8") as f:
    #     json.dump(city_data_list, f, indent=4)
    
    return city_data_list


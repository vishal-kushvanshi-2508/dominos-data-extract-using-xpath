
import os
import requests

from lxml import html

from store_data_database import product_data_insert

from store_data_database import *




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





import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


# ---------- WORKER FUNCTION ----------
def process_city(city, headers, folder_name):
    city_name = city["city_name"]
    city_url = city["city_url"]

    try:
        response = requests.get(city_url, headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"Failed: {city_name} ({response.status_code})")
            return []

        # safe filename
        safe_city_name = city_name.replace(" ", "_").lower()
        file_path = os.path.join(folder_name, f"{safe_city_name}.html")

        # save html
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(response.text)

        # extract data
        dominos_data = extract_data_from_html(response.text)

        return dominos_data

    except Exception as e:
        print(f"Error for {city_name}: {e}")
        return []




# ---------- MAIN FUNCTION ----------
def create_html_files(city_data_list):

    folder_name = "city_html_files"
    os.makedirs(folder_name, exist_ok=True)


    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://stores.burgerking.in/location/haryana',
        'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
    }

    dominos_all_data_list = []

    # Thread pool
    with ThreadPoolExecutor(max_workers=10) as executor:

        futures = [
            executor.submit(process_city, city, headers, folder_name)
            for city in city_data_list
        ]
        
        # print("futures len : ", len(futures))
        for future in as_completed(futures):
            
            result = future.result()   # list from each thread
            dominos_all_data_list.extend(result)

    # insert after all threads complete
    if dominos_all_data_list:
        product_data_insert(list_data=dominos_all_data_list)

    print("Total records:", len(dominos_all_data_list))














### without threading code 






# def create_html_files(city_data_list):

#     folder_name = "city_html_files"
#     os.makedirs(folder_name, exist_ok=True)

#     headers = {
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#         'accept-language': 'en-US,en;q=0.9',
#         'cache-control': 'no-cache',
#         'pragma': 'no-cache',
#         'priority': 'u=0, i',
#         'referer': 'https://stores.burgerking.in/location/haryana',
#         'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#         'sec-fetch-dest': 'document',
#         'sec-fetch-mode': 'navigate',
#         'sec-fetch-site': 'same-origin',
#         'sec-fetch-user': '?1',
#         'upgrade-insecure-requests': '1',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
#     }

#     dominos_all_data_list = []
#     # count = 0
#     request_count = 0 
#     for city in city_data_list:
#         city_name = city["city_name"]
#         city_url = city["city_url"]

#         # if count == 1 :
#         #     break
#         # count += 1

#         try:
#             response = requests.get(city_url, headers=headers, timeout=10)

#             if response.status_code != 200:
#                 print(f"Failed: {city_name} ({response.status_code})")
#                 continue

#             # safe filename
#             # safe_city_name = re.sub(r'[^a-zA-Z0-9_]', '', city_name.replace(" ", "_")).lower()
#             safe_city_name = city_name.replace(" ", "_").lower()

#             file_path = os.path.join(folder_name, f"{safe_city_name}.html.gz")


#             dominos_data = extract_data_from_html(response.text)
#             # dominos_list.append(dominos_data_dict)
#             dominos_all_data_list.extend(dominos_data)
            

#             with open(file_path, "w", encoding="utf-8") as f:
#                 f.write(response.text)

#             print(f"Saved: {file_path}")

#         except Exception as e:
#             print(f"Error for {city_name}: {e}")

#         if request_count >= 100:
#                 product_data_insert(list_data=dominos_all_data_list)
#                 dominos_all_data_list.clear()
#                 request_count = 0
#         request_count += 1
#     if dominos_all_data_list:
#         product_data_insert(list_data=dominos_all_data_list)


#     # print("total dominos : ", dominos_list)
#     # print("total dominos : ", len(dominos_list))
#     return 







from extract_data import *
import time
from store_data_database import *
from pages_request_city_data import *

file_name = "Domino's Pizza Restaurants in Mumbai _ Nearby Pizza Shops in Mumbai – Domino’s India.html"
url = "https://www.dominos.co.in/store-location/"

def main():
    ## city name and url for table crate
    create_table_city()
    print("table and db create")
    
    html_content = read_html_content_using_url(url)
    # print(html_content)
    city_data_list = extract_data_for_city(html_content)
    city_url_name_insert(list_data=city_data_list)
    
    city_data_list = fetch_table_data()
    # print(city_data_list)
    print("city_data_list : ", len(city_data_list))
    
    create_table_product()

    create_html_files(city_data_list)


if __name__ == "__main__":
    start = time.time()
    main()

    end = time.time()
    print("time different  : ", end - start)



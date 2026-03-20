

from typing import List, Tuple

import mysql.connector # Must include .connector


city_table_name = "city_name_url"


DB_CONFIG = {
    "host" : "localhost",
    "user" : "root",
    "password" : "actowiz",
    "port" : "3306",
    "database" : "dominos_city_data"
}

def get_connection():
    try:
        ## here ** is unpacking DB_CONFIG dictionary.
        connection = mysql.connector.connect(**DB_CONFIG)
        ## it is protect to autocommit
        connection.autocommit = False
        return connection
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise

def create_db():
    connection = get_connection()
    # connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS dominos_city_data;")
    connection.commit()
    connection.close()
# create_db()



def create_table_city():
    connection = get_connection()
    cursor = connection.cursor()

    ## delete table if exist ....
    delete_query = f"DROP TABLE IF EXISTS {city_table_name}"
    cursor.execute(delete_query)

    try:
        query =  f"""
                CREATE TABLE IF NOT EXISTS {city_table_name}(
                id INT AUTO_INCREMENT PRIMARY KEY,
                city_name VARCHAR(200),
                city_url TEXT 
        ); """
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Table creation failed")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

batch_size_length = 100
def data_commit_batches_wise(connection, cursor, sql_query : str, sql_query_value: List[Tuple], batch_size: int = batch_size_length ):
    ## this is save data in database batches wise.
    batch_count = 0
    for index in range(0, len(sql_query_value), batch_size):
        batch = sql_query_value[index: index + batch_size]
        cursor.executemany(sql_query, batch)
        batch_count += 1
        connection.commit()
    return batch_count


def city_url_name_insert(list_data : list):
    connection = get_connection()
    cursor = connection.cursor()
    dict_data = list_data[0]
    columns = ", ".join(list(dict_data.keys()))
    values = "".join([len(dict_data.keys()) * '%s,']).strip(',')
    parent_sql = f"""INSERT INTO {city_table_name} ({columns}) VALUES ({values})"""
    try:
        product_values = []
        for dict_data in list_data:
            product_values.append( (
                dict_data.get("city_name") ,
                dict_data.get("city_url")
            ))

        try:
            batch_count = data_commit_batches_wise(connection, cursor, parent_sql, product_values)
            print(f"Parent batches executed count={batch_count}")
        except Exception as e:
            print(f"batch can not. Error : {e} ")

        cursor.close()
        connection.close()

    except Exception as e:
        ## this exception execute when error occur in try block and rollback until last save on database .
        connection.rollback()
        # print(f"Transaction failed, rolled back. Error: {e}")
        print("Transaction failed. Rolling back")
    except:
        print("except error raise ")
    finally:
        connection.close()



def fetch_table_data():
    connection = get_connection()
    cursor = connection.cursor()
    query = f"SELECT id, city_name, city_url FROM {city_table_name}"
    cursor.execute(query)

    rows = cursor.fetchall()

    result = []

    for row in rows:
        data = {
            # "id": row[0],
            "city_name": row[1],
            "city_url": row[2]
        }
        result.append(data)

    cursor.close()
    connection.close()
    return result









product_table_name = "product_detail"


### product table code 

def create_table_product():
    connection = get_connection()
    cursor = connection.cursor()

    ## delete table if exist ....
    delete_query = f"DROP TABLE IF EXISTS {product_table_name}"
    cursor.execute(delete_query)

    try:
        query =  f"""
                CREATE TABLE IF NOT EXISTS {product_table_name}(
                id INT AUTO_INCREMENT PRIMARY KEY,
                brand_name VARCHAR(150),
                login_page_link TEXT,
                address VARCHAR(500) ,
                region VARCHAR(150) ,
                delivery_time VARCHAR(150) ,
                cost VARCHAR(150) ,
                open_timing VARCHAR(150) ,
                good_for VARCHAR(150) ,
                phone_no VARCHAR(150) 
        ); """
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Table creation failed")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()




def product_data_insert(list_data : list):
    connection = get_connection()
    cursor = connection.cursor()
    dict_data = list_data[0]
    columns = ", ".join(list(dict_data.keys()))
    values = "".join([len(dict_data.keys()) * '%s,']).strip(',')
    parent_sql = f"""INSERT INTO {product_table_name} ({columns}) VALUES ({values})"""
    try:
        product_values = []
        for dict_data in list_data:
            product_values.append( (
                dict_data.get("brand_name"),
                dict_data.get("login_page_link"),
                dict_data.get("address"),
                dict_data.get("region"),
                dict_data.get("delivery_time"),
                dict_data.get("cost"),
                dict_data.get("open_timing"),
                dict_data.get("good_for"),
                dict_data.get("phone_no")
            ))

        try:
            batch_count = data_commit_batches_wise(connection, cursor, parent_sql, product_values)
            print(f"Parent batches executed count={batch_count}")
        except Exception as e:
            print(f"batch can not. Error : {e} ")

        cursor.close()
        connection.close()

    except Exception as e:
        ## this exception execute when error occur in try block and rollback until last save on database .
        connection.rollback()
        # print(f"Transaction failed, rolled back. Error: {e}")
        print("Transaction failed. Rolling back")
    except:
        print("except error raise ")
    finally:
        connection.close()


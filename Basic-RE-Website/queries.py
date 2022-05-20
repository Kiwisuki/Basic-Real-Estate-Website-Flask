from flask import Flask, redirect, url_for, render_template, request, session, flash
import pymysql
import string
import random
from datetime import datetime, timedelta

def filter_ad_keys(dictionary, keys):
    """Filters a dict by only including certain keys."""
    key_set = set(keys) & set(dictionary.keys())
    return {key: dictionary[key] for key in key_set}

def id_g(size=10, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def insert(info, table):
    '''
    Inserts values into the table
            Parameters:
                    info (dict): dictionary with col names as keys
                    table (string): specification to which database table to insert

            Returns:
                    exit_code (int): 1 if successful, 0 if failed insert
    '''
    try:
        cols = f'{tuple(info.keys())}'.replace("'","`")
        vals = f'{tuple(info.values())}'
        connection = pymysql.connect(host="localhost", user="root", passwd="", database="ktunt")
        cursor = connection.cursor()

        # queries for inserting values
        insert = f"INSERT INTO {table}{cols} VALUES{vals};"
        #executing the quires
        cursor.execute(insert)
        connection.commit()
        connection.close()
        return 1
    except Exception as e:
        print(e)
        return 0

def auth_password(email, password):
    '''
    Returns boolean if password matches password in database by email
    '''
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="ktunt")
    cursor = connection.cursor()

    # queries for inserting values
    insert = f"SELECT User_Password FROM users WHERE Email = '{email}'"
    #executing the quires
    cursor.execute(insert)
    row = cursor.fetchall()
    if len(row) == 0:
        return False
    password_db = row[0][0]
    connection.commit()
    connection.close()
    return password == password_db

def create_ad_request(request, object_type):
    info = dict(request.form)
    ad_info = {}
    ad_info['fk_User_Email'] = session['user']
    ad_info['Ad_id'] = id_g()
    info['fk_Advertisement_Ad_id'] = ad_info['Ad_id']
    ad_info['Ad_description'] = info['Ad_description']
    ad_info['Price'] = info['Price']
    ad_info['Ad_name'] = info['Ad_name']
    ad_info['Ad_type'] = info['Ad_type']
    ad_info['Upload_date'] = datetime.today().strftime('%Y-%m-%d')
    ad_info['Expire_date'] = (datetime.today() + timedelta(days=60)).strftime('%Y-%m-%d')
    info[f'{object_type}_id'] = id_g()
    for col in ['Ad_description', 'Price', 'Ad_name', 'Ad_type']: 
        info.pop(col, None)
    if not insert(ad_info, f'advertisements'):
        flash('Insert ad error')
    elif not insert(info, f'{object_type}s'):
        flash('Insert object error')
    else:
        flash(f'{object_type} ad created')

def get_ads_browse(object_type='', city=None, price_max=None, price_min=0, page=0):
    '''
    Gets list of  advertisement dictionaries from database
    '''
    
    offset = page*20
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="ktunt")
    cursor = connection.cursor()

    # query = f"SHOW COLUMNS FROM `advertisements`"
    cols = 'Name Price Type Link'.split()
    
    # queries for inserting values
    query = f"SELECT advertisements.Ad_name, advertisements.Price, advertisements.Ad_type, advertisements.Ad_id FROM `advertisements` LIMIT 1000 OFFSET {offset}"
    #executing the quires
    cursor.execute(query)
    rows = cursor.fetchall()
    ads = [dict(zip(cols, row)) for row in rows]
    for ad in ads:
        ad['Link'] = '/ads/' + ad['Link']
    
    connection.close()
    return ads

def user_ads(email):
    '''
    Gets list of  advertisement dictionaries from database
    '''
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="ktunt")
    cursor = connection.cursor()

    # query = f"SHOW COLUMNS FROM `advertisements`"
    cols = 'Name Price Type Ad_id'.split()
    
    # queries for inserting values
    query = f"SELECT advertisements.Ad_name, advertisements.Price, advertisements.Ad_type, advertisements.Ad_id FROM `advertisements` WHERE fk_User_Email='{email}'"

    #executing the quires
    cursor.execute(query)
    rows = cursor.fetchall()
    ads = [dict(zip(cols, row)) for row in rows]
    for ad in ads:
        ad['Link'] = '/ads/' + ad['Ad_id']
        ad['Edit'] = '/ads/edit/' + ad['Ad_id']
        ad['Delete'] = '/ads/delete/' + ad['Ad_id']
    
    connection.close()
    return ads

def get_ad_object(ad_id):

    '''
    Gets list of advertisement dictionaries from database that belong to a user(email)
    '''
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="ktunt")
    cursor = connection.cursor()

    # queries for inserting values
    query = f"SHOW COLUMNS FROM `advertisements`"
    cursor.execute(query)
    cols = cursor.fetchall()
    cols = [col[0] for col in cols]
    connection.commit()
    
    # queries for inserting values
    query = f"SELECT * FROM `advertisements` WHERE Ad_id='{ad_id}'"
    cursor.execute(query)
    row = cursor.fetchall()
    ad = dict(zip(cols, row[0]))
    
    
    
    for i in 'flats garages houses plots premises'.split():
        # queries for inserting values
        query = f"SHOW COLUMNS FROM `{i}`"
        cursor.execute(query)
        cols = cursor.fetchall()
        cols = [col[0] for col in cols]
        connection.commit()

        # queries for inserting values
        query = f"SELECT * FROM `{i}` WHERE fk_Advertisement_Ad_id='{ad_id}'"
        cursor.execute(query)
        row = cursor.fetchall()
        if len(row) != 0:
            ob = dict(zip(cols, row[0]))
            break
        
    res = ad | ob
    filtered = [k for k in res.keys() if 'id' not in k]
    result = []
    res = filter_ad_keys(res, filtered)
    connection.close()
    for k,v in res.items():
        result.append(f"{k}: {v}")

    return result

def get_ad(ad_id):
    '''
    Gets list of  advertisement dictionaries from database
    '''
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="ktunt")
    cursor = connection.cursor()

    # queries for inserting values
    query = f"SELECT advertisements.Ad_name, advertisements.Price, advertisements.Ad_description FROM `advertisements` WHERE Ad_id='{ad_id}'"
    #executing the quires
    cursor.execute(query)
    rows = cursor.fetchall()[0]
    connection.close()
    return rows

def delete_ad(ad_id):
    '''
    Deletes advertisement from database
    '''
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="ktunt")
    cursor = connection.cursor()

    # queries for inserting values
    query = f"DELETE FROM `advertisements` WHERE Ad_id='{ad_id}'"
    #executing the quires
    cursor.execute(query)
    connection.commit()
    connection.close()

def update_ad(ad_id, form):
    '''
    Updates advertisement in database
    '''
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="ktunt")
    cursor = connection.cursor()

    # queries for inserting values
    query = f"UPDATE `advertisements` SET Ad_name='{form['Ad_name']}', Price='{form['Price']}', Ad_description='{form['Ad_description']}' WHERE Ad_id='{ad_id}'"
    #executing the quires
    cursor.execute(query)
    connection.commit()
    connection.close()

def seen_ad(ad_id, email, table='viewed_ads' , g_id=None):
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="ktunt")
    cursor = connection.cursor()
    if not g_id:
        g_id = id_g()
    # queries for inserting values
    if table == 'viewed_ads':
        query = f"INSERT INTO `{table}` (`id_Viewed_ad`, `fk_User_Email`, `fk_Advertisement_Ad_id`) VALUES ('{g_id}', '{email}', '{ad_id}');"
    elif table == 'saved_ads':
        query = f"INSERT INTO `{table}` (`Saved_ad_id`, `fk_User_Email`, `fk_Advertisement_Ad_id`) VALUES ('{g_id}', '{email}', '{ad_id}');"
    #executing the quires
    cursor.execute(query)
    connection.commit()
    connection.close()

def get_seen_ads(email):
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="ktunt")
    cursor = connection.cursor()
    # queries for inserting values
    cols = 'Name Price Type Id Date view_id'.split()
    query = f"SELECT advertisements.Ad_name, advertisements.Price, advertisements.Ad_type, advertisements.Ad_id, viewed_ads.view_date, viewed_ads.id_Viewed_ad FROM `viewed_ads` INNER JOIN advertisements ON viewed_ads.fk_Advertisement_Ad_id = advertisements.Ad_id WHERE viewed_ads.fk_User_Email='{email}' ORDER BY viewed_ads.view_date DESC"
    #executing the quires
    cursor.execute(query)
    rows = cursor.fetchall()

    ads = [dict(zip(cols, row)) for row in rows]
    for ad in ads:
        ad['Link'] = '/ads/' + ad['Id']
        ad['Delete'] = '/delete-view/' + ad['view_id']

    connection.close()
    return ads

def delete_seen_ad(view_id):
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="ktunt")
    cursor = connection.cursor()
    # queries for inserting values
    query = f"DELETE FROM `viewed_ads` WHERE id_Viewed_ad='{view_id}'"
    #executing the quires
    cursor.execute(query)
    connection.commit()
    connection.close()

def get_saved_ads(email):
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="ktunt")
    cursor = connection.cursor()
    # queries for inserting values
    cols = 'Name Price Type Id saved_id'.split()
    query = f"SELECT advertisements.Ad_name, advertisements.Price, advertisements.Ad_type, advertisements.Ad_id, saved_ads.Saved_ad_id FROM `saved_ads` INNER JOIN advertisements ON saved_ads.fk_Advertisement_Ad_id = advertisements.Ad_id WHERE saved_ads.fk_User_Email='{email}'"
    #executing the quires
    cursor.execute(query)
    rows = cursor.fetchall()

    ads = [dict(zip(cols, row)) for row in rows]
    for ad in ads:
        ad['Link'] = '/ads/' + ad['Id']
        ad['Delete'] = '/delete-save/' + ad['saved_id']

    connection.close()
    return ads

def delete_saved_ad(saved_id):
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="ktunt")
    cursor = connection.cursor()
    # queries for inserting values
    query = f"DELETE FROM `saved_ads` WHERE Saved_ad_id='{saved_id}'"
    #executing the quires
    cursor.execute(query)
    connection.commit()
    connection.close()



def update_user(email, form):
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="ktunt")
    cursor = connection.cursor()

    # queries for inserting values
    query = f"UPDATE `users` SET User_password='{form['New_password']}', Phone_number{form['Phone_number']} WHERE Email='{email}'"
    #executing the quires
    cursor.execute(query)
    connection.commit()
    connection.close()



def update_user(email, form):
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="ktunt")
    cursor = connection.cursor()

    # queries for inserting values
    query = f"UPDATE `users` SET User_password='{form['New_password']}', Phone_number='{form['Phone_number']}', Email_notification={('email_not' in form)*1}, Phone_notification={('phone_not' in form)*1}  WHERE Email='{email}'"
    #executing the quires
    cursor.execute(query)
    connection.commit()
    connection.close()
    return 1

def get_user_number(email):
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="ktunt")
    cursor = connection.cursor()
    # queries for inserting values
    query = f"SELECT Phone_number FROM `users` WHERE Email='{email}'"
    #executing the quires
    cursor.execute(query)
    number = cursor.fetchone()
    connection.close()
    return number[0]


def get_ads_views(type_):
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="ktunt")
    cursor = connection.cursor()
    # queries for inserting values
    query = f"SELECT Ad_name, Ad_type, Ad_id, Price, COUNT(*) FROM advertisements LEFT JOIN viewed_ads ON advertisements.Ad_id = viewed_ads.fk_Advertisement_Ad_Id WHERE Ad_type='{type_}' GROUP BY fk_Advertisement_Ad_Id"
    #executing the quires
    cursor.execute(query)
    rows = cursor.fetchall()
    s = sum([v[4] for v in rows])
    connection.close()
    return rows, s

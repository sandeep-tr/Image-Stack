#Name: Sandeep Raveendran Thandassery
#Course Number: CSE 6331 Section 004
#Lab Number: 7
'''Copyright (c) 2015 HG,DL,UTA
   Database layer'''

# -*- coding: utf-8 -*-

import time
import MySQLdb
import MySQLdb.cursors

#DB connection params
_RDS_HOST_ADDR = ''
_RDS_PORT = 3306
_DATABASE = 'imagestack'

# Tables
_USER_TABLE = 'T_USER'
_IMAGE_TABLE = 'T_IMAGE'
_COMMENT_TABLE = 'T_COMMENT'


# Create a DB connection object and returns it.
def get_db():
    print 'Establishing db connection to - {}'.format(_DATABASE)
    db = MySQLdb.connect(host=_RDS_HOST_ADDR, port=_RDS_PORT, db=_DATABASE, user='', passwd='')
    return db

def autheticate_user(user_id, hash_pwd):
    valid = False
    connection = None
    cursor = None
    print 'here'
    query = 'SELECT COUNT(1) FROM {} WHERE USER_ID = %s AND PASSWORD = %s'.format(_USER_TABLE)
    try:
        print 'here'
        connection = get_db()
        print 'here'
        cursor = connection.cursor()
        cursor.execute(query, (user_id, hash_pwd))
        if cursor.fetchone()[0] > 0:
            valid = True
    except MySQLdb.Error, msqe:
        print msqe
        raise
    except Exception, e:
        print e
        raise
    finally:
        if cursor:
            cursor.close()
        if connection and connection.open:
            connection.close()
    return valid
            

def insert_image(user_id, content, image_name, mime_type):
    print('Entering insert_image function; params - user_id: {}, image_name: {}, mime_type: {}'.format(user_id, image_name, mime_type))
    status = False
    connection = cursor = None
    query = 'INSERT INTO {} (CONTENT, IMAGE_TITLE, MIME_TYPE, CREATED_BY) VALUES (%s, %s, %s, %s)'.format(_IMAGE_TABLE)
    try:
        connection = get_db()
        cursor = connection.cursor()
        params = (content.stream.read(), image_name, mime_type, user_id)
        count = cursor.execute(query, params)
        if count > 0:
            connection.commit()
            status = True
        
    except MySQLdb.Error, msqe:
        raise
    except Exception, e:
        raise
    finally:
        if cursor:
            cursor.close()
        if connection and connection.open:
            connection.close()
    print('Exiting insert_image function; status {}'.format(status))
    return status   

def delete_image(image_id):
    status = False
    connection = cursor = None
    query = 'UPDATE {} SET STATUS=%s, DELETED_ON=%s WHERE IMAGE_ID=%s'.format(_IMAGE_TABLE)
    try:
        connection = get_db()
        cursor = connection.cursor()
        count = cursor.execute(query, ('-1', time.strftime('%Y-%m-%d %H:%M:%S'), image_id))
        if count > 0:
            connection.commit()
            status = True
        
    except MySQLdb.Error, msqe:
        raise
    except Exception, e:
        raise
    finally:
        if cursor:
            cursor.close()
        if connection and connection.open:
            connection.close()
    return status

def add_comment(user_id, image_id, comment):
    status = False
    connection = cursor = None
    query = 'INSERT INTO {} (IMAGE_ID, COMMENT, COMMENTED_BY) VALUES (%s, %s, %s)'.format(_COMMENT_TABLE)
    try:
        connection = get_db()
        cursor = connection.cursor()
        count = cursor.execute(query, (image_id, comment, user_id))
        if count > 0:
            connection.commit()
            status = True
        
    except MySQLdb.Error, msqe:
        raise
    except Exception, e:
        raise
    finally:
        if cursor:
            cursor.close()
        if connection and connection.open:
            connection.close()
    return status

def fetch_image_list(user_id, own):
    print 'Entering fetch_image_list; params - user_id: {}'.format(user_id)
    data = []
    connection = cursor = None
    query = 'SELECT IMAGE_ID FROM {} WHERE STATUS = 1 AND'.format(_IMAGE_TABLE)
    try:
        if own:
            query = query + ' CREATED_BY=%s'
        else:
            query = query + ' NOT CREATED_BY=%s'
        connection = get_db()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, (user_id))
        for row in cursor.fetchall():
            data.append(dict([('image_id',row['IMAGE_ID'])]))
        
    except MySQLdb.Error, msqe:
        raise
    except Exception, e:
        raise
    finally:
        if cursor:
            cursor.close()
        if connection and connection.open:
            connection.close()
    return data

def fetch_image_details(image_id):
    data = connection = cursor = None
    query = 'SELECT IMAGE_TITLE, CREATED_BY, CREATED_ON FROM {} \
            WHERE IMAGE_ID=%s AND STATUS = 1'.format(_IMAGE_TABLE)
    
    try:            
        connection = get_db()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, (image_id))
        row = cursor.fetchone()
        if row:
            data = (dict([('image_id', image_id),
                          ('image_title', row['IMAGE_TITLE']),
                          ('created_by', row['CREATED_BY']),
                          ('created_on', row['CREATED_ON'])]))
        
    except MySQLdb.Error, msqe:
        raise
    except Exception, e:
        raise
    finally:
        if cursor:
            cursor.close()
        if connection and connection.open:
            connection.close()
    return data

def fetch_image_comments(image_id):
    comments = []
    connection = cursor = None
    query = 'SELECT COMMENT_ID, COMMENT, COMMENTED_BY, COMMENTED_ON \
            FROM {} WHERE IMAGE_ID=%s'.format(_COMMENT_TABLE)
    
    try:            
        connection = get_db()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, (image_id))
        for row in cursor.fetchall():
            comments.append(dict([('comment_id', row['COMMENT_ID']),
                                  ('comment', row['COMMENT']),
                                  ('commented_by', row['COMMENTED_BY']),
                                  ('commented_on', row['COMMENTED_ON'])]))
        
    except MySQLdb.Error, msqe:
        raise
    except Exception, e:
        raise
    finally:
        if cursor:
            cursor.close()
        if connection and connection.open:
            connection.close()
    return comments   

def fetch_image(image_id):
    print('Entering fetch_image; params - image_id: {}'.format(image_id))
    content = connection = cursor = None
    query = 'SELECT CONTENT FROM {} WHERE IMAGE_ID=%s AND STATUS = 1'.format(_IMAGE_TABLE)
    try:            
        connection = get_db()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, (image_id))
        content = cursor.fetchone()['CONTENT']
        
    except MySQLdb.Error, msqe:
        raise
    except Exception, e:
        raise
    finally:
        if cursor:
            cursor.close()
        if connection and connection.open:
            connection.close()
    return content
    

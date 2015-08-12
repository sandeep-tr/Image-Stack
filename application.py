#Name: Sandeep Raveendran Thandassery
#Course Number: CSE 6331 Section 004
#Lab Number: 7
'''Copyright (c) 2015 HG,DL,UTA
   Python program runs on AWS EC2. A service where
   images can be uploaded, deleted, view images uploaded
   by a User and others along with add comments feature'''

# -*- coding: utf-8 -*-

import time
from basic_auth import requires_auth
import database as app_data
from flask import Flask, request, render_template
from flask import send_file, session, redirect, url_for
from flask import make_response
from werkzeug import secure_filename

application = Flask(__name__)

# Displays index page
@application.route('/')
@requires_auth
def index():
    print 'Entering index function'
    own_images = app_data.fetch_image_list(session['user_id'], True)
    other_images = app_data.fetch_image_list(session['user_id'], False)
    return render_template('home.html',
                           own_images=own_images,
                           other_images=other_images)

# Used to upload an image
@application.route('/images',  methods=['POST'])
@requires_auth
def upload_image():
    print 'Entering upload_image function'
    status = False
    file = request.files['image']
    if file:
        file_name = secure_filename(file.filename)
        mime_type = file.mimetype
        status = app_data.insert_image(session['user_id'],
                                       file,
                                       file_name,
                                       mime_type)
        
    return redirect(url_for('index'))

# Used to get image content
@application.route('/images/<int:image_id>', methods=['GET'])
@requires_auth
def get_image(image_id):
    print 'Entering get_image function'
    content = app_data.fetch_image(image_id)
    if content:
        response = make_response(content)
        response.headers['Content-Type'] = 'image/jpeg'
        return response
    else:
        return send_file('error.gif', mimetype='image/gif')

# Used to delete an image
@application.route('/images/<int:image_id>', methods=['DELETE'])
@requires_auth
def delete_image(image_id):
    print 'Entering delete_image function'
    status = app_data.delete_image(image_id)
    return str(status)


# Used to get image details
@application.route('/images/<int:image_id>/details')
@requires_auth
def display_details(image_id):
    print 'Entering get_details function'
    details = app_data.fetch_image_details(image_id)
    comments = app_data.fetch_image_comments(image_id)
    if details:
        return render_template('details.html',
                               details=details,
                               comments=comments)

# Used to add comments on a photo
@application.route('/images/<int:image_id>/comments', methods=['POST'])
@requires_auth
def add_comment(image_id):
    print 'Entering send_image function'
    user_id = session['user_id']
    comment = request.form['comment']
    status = app_data.add_comment(user_id, image_id, comment)
    return redirect(url_for('display_details', image_id=image_id))

# Used by load balancer to check health of application
@application.route('/health')
def monitor():
    return render_template('health.html')

# Used to handle 404 errors
@application.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == '__main__':
    # Setting debug to True enables debug output.
    application.debug = True


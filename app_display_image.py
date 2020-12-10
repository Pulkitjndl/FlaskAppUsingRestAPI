'''------------------------------------------------------------------------
 Project Name: Demo app for Inspectlabs
 $Archive: app.py $
 $Author: PULKIT JINDAL $
 $Date: $ 10-12-2020
 (c) Copyright 2020, Pulkit Jindal
----------------------------------------------------------------------------
 $Revision: 1 $
----------------------------------------------------------------------------
 Target system: Windows/Linux/MAC
 Compiler:    Python3
----------------------------------------------------------------------------
               A U T H O R   I D E N T I T Y
----------------------------------------------------------------------------
             Initials       Name        
            ---------  -------------------
             PJINDAL     PULKIT JINDAL 
----------------------------------------------------------------------------'''
from functools import wraps
import datetime
import jwt
import os
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from flask import Flask, jsonify, request, make_response, render_template, send_from_directory
__author__ = 'Pulkit Jindal'
__version__ = '1.0'
__email__ = 'pulkitjndl@gmail.com'
'''----------------------------------------------------------------------------
               R E V I S I O N   H I S T O R Y
----------------------------------------------------------------------------
 $Log: $
----------------------------------------------------------------------------
 $Brief: This file works as the main server of the demo app for Inspectlabs.
--------------------------------------------------------------------------'''


app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)

app.config['SECRET_KEY'] = 'mysecretkey'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated


@app.route("/home")
@token_required
@limiter.limit('5 per minute')
def index():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    # target = os.path.join(APP_ROOT, 'static/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        if(len(upload.filename) < 1):
            return jsonify({'message': 'Image is missing!'}), 403
        filename = upload.filename
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)

    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("complete.html", filename=filename)


@app.route('/upload/<filename>')
@limiter.limit('5 per minute')
def send_image(filename):
    return send_from_directory("images", filename)
    # return redirect(url_for('static', filename='upload/' + filename), code=301)


@app.route('/')
def login():
    auth = request.authorization
    if auth and auth.password == 'password':
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(seconds=60)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


if __name__ == "__main__":
    #app.run(port=4555, debug=True)
    app.run(host='0.0.0.0', port=3000, debug=True,
            threaded=True, use_reloader=False)

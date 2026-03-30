"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

from flask import render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from . import app, db
from .forms import PropertyForm
from .models import Property
import os

def get_uploaded_images():
    lst = []
    rootdir = os.getcwd() 
    for subdir, dirs, files in os.walk(rootdir + '/uploads'): 
        for file in files:
            if file != ".gitkeep":
                lst.append(file)
            
    return lst
    
###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/properties/create', methods = ["GET","POST"]) 
def addProperty():
    form = PropertyForm()

    if form.validate_on_submit():
        title = form.title.data
        desc = form.desc.data
        numRooms = form.numRooms.data
        numBaths = form.numBaths.data
        price = form.price.data
        ptype = form.ptype.data
        location = form.location.data
        upload = form.photo.data
        
        filename = secure_filename(upload.filename)
        upload.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        prop = Property(title, desc, numBaths, numRooms, ptype, price, location, filename)
        
        db.session.add(prop)
        db.session.commit()
        
        flash('Property Saved', 'success')
        
        return redirect(url_for("home"))
    
    return render_template("create_property.html", form = form)

@app.route('/uploads/<filename>')
def get_image(filename):
    uploads = os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER'])
    if(os.path.exists(os.path.join(uploads, filename))):
        return send_from_directory(uploads, filename)
    
@app.route('/properties')
def showProperties():
    properties = Property.query.all()
    return render_template("properties.html", properties = properties)

@app.route('/properties/<propertyid>')
def viewProperty(propertyid):
    property = Property.query.get_or_404(propertyid)
    return render_template("view_property.html", property=property)


###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

import os

import urllib.request
from flask import Flask,g,abort, render_template,request,redirect,session,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename

from werkzeug.utils import redirect

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SECRET_KEY'] = 'sri'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
db = SQLAlchemy(app)


class BlogPost1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)



    def __repr__(self):
        return 'Blog Post1 ' + str(self.id)

contact_info = [
   { 
    'contact': '7595929511',
    'email': 'srijani19.sb@gmail.com'
   }
]


'''

@app.route('/home')
def home():
    
    return render_template("home.html")
'''

@app.route('/home', methods = ['GET','POST'])
def home():
    return render_template('home.html', info = contact_info)


@app.route('/feedback', methods = ['GET','POST'])
def feedback():
    '''
    return render_template("feedback.html", feedback = all_feedbacks)
    '''
    if request.method=="POST":
                     post_firstname = request.form['firstname']
                     post_lastname = request.form['lastname'] 
                     post_subject =  request.form['subject']
                                     
                     new_post = BlogPost1(firstname=post_firstname, lastname=post_lastname, subject=post_subject)
                     db.session.add(new_post)
                     db.session.commit()
                     return redirect('/feedback')
    else:
        all_posts = BlogPost1.query.order_by(BlogPost1.date_posted).all()
        return render_template('feedback.html', post = all_posts)

@app.route('/feedback/delete/<int:id>')
def delete(id):
    x = BlogPost1.query.get_or_404(id)
    db.session.delete(x)
    db.session.commit()
    return redirect('/feedback')

@app.route('/feedback/edit/<int:id>' ,  methods = ['GET', 'POST'])
def edit(id):
    x = BlogPost1.query.get_or_404(id)
    if request.method == "POST":
        x.firstname = request.form ['firstname']
        x.lastname = request.form ['lastname']
        x.subject = request.form ['subject']
        db.session.commit()
        flash('Your feedback Has been updated')
        return redirect('/feedback')
    else:
        return render_template('edit.html' , x = x)   



@app.route('/')
def index():
    return render_template("index.html")



@app.route('/portfolio',  methods = ['GET', 'POST'])
def portfolio():
        return render_template('upload.html')

'''
@app.route('/portfolio', methods=['POST'])
def upload_video():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	else:
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_video filename: ' + filename)
		flash('Video successfully uploaded and displayed below')
		return render_template('upload.html', filename=filename)


@app.route('/display/<filename>')
def display_video(filename):
	#print('display_video filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)
'''









if  __name__ == "__main__":
    app.run(debug=True)
    

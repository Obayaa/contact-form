from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Create the app
app = Flask(__name__)
# Configure SQL Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Defining Database Model
class ContactForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100), nullable = False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Creating the database
with app.app_context():
    db.create_all()

# Route to render frontend form
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods = ['POST'])
def submit():
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    message = request.form['message']

    if not lname or not fname or not email or not message:
        return jsonify({'message': 'All fields are required!'}), 400

    new_entry = ContactForm(fname=fname, lname=lname, email=email, message=message)
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({'message': 'Form Submitted Successfully'}), 200

@app.route('/messages', methods = ['GET'])
def get_messages():
    messages = ContactForm.query.all()
    return jsonify([{
        'id': msg.id, 'fname': msg.fname, 'lname':msg.lname, 'email':msg.email, 'message':msg.message
    }
    for msg in messages
    ])

if __name__ == '__main__':
    app.run(debug=True)
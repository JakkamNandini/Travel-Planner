
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
import os
app = Flask(__name__)
# Flask app secret key
app.secret_key = os.urandom(24)

# Sample list of destinations
destinations = [
    "Paris", "New York", "Tokyo", "London", "Rome",
    "Sydney", "Dubai", "Cape Town", "Singapore", "Barcelona"
]

@app.route('/', methods=['GET', 'POST'])
def home():
    search_query = ""
    results = []

    if request.method == 'POST':
        search_query = request.form.get('search', '')
        results = [destination for destination in destinations if search_query.lower() in destination.lower()]

    return render_template('index.html', results=results, search_query=search_query)

@app.route('/destinations')
def show_destinations():
    return render_template('destinations.html', destinations=destinations)

@app.route('/about')
def about():
    return render_template('about.html')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        # Here, you can save the message to a database or send an email
        return render_template('thankyou.html', name=name)
    return render_template('contact.html', form=form)

@app.route('/destination/<name>')
def destination_detail(name):
    # Example info for cities
    guides = {
        "Paris": "Known for Eiffel Tower, Louvre, and cafes.",
        "New York": "The city that never sleeps. Visit Times Square!",
        "Tokyo": "Tech and tradition blend in Tokyo.",
        "London": "Explore Buckingham Palace and British culture.",
        "Rome": "Ancient history, the Colosseum, and Vatican City.",
        "Sydney": "Beautiful beaches and the Sydney Opera House.",
        "Dubai": "Luxury shopping, ultramodern architecture, desert safaris.",
        "Cape Town": "Table Mountain and beautiful coastline.",
        "Singapore": "Marina Bay Sands and the Gardens by the Bay.",
        "Barcelona": "Gaudi’s architecture and Mediterranean beaches."
    }

    description = guides.get(name, "Travel guide coming soon...")
    return render_template('destination_detail.html', name=name, description=description)

if __name__ == "__main__":
    app.run(debug=True)

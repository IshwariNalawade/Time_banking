# app.py

from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session handling

# In-memory "database" (just Python dictionaries for now)
users = {}
services = []

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return "User already exists. Try logging in."
        users[username] = {
            'password': password,
            'hours': 5,  # Start with 5 hours
            'offers': [],
            'requests': []
        }
        return redirect(url_for('login'))
    return render_template('register.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials. Try again."
    return render_template('login.html')

# Dashboard Page
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = users[session['username']]
    return render_template('dashboard.html', username=session['username'], user=user)

# Offer a Service
@app.route('/offer', methods=['GET', 'POST'])
def offer():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
       service = request.form['service']
       category = request.form['category']
       user = users[session['username']]
       user['offers'].append({'service': service, 'category': category})
       return redirect(url_for('dashboard'))
    return render_template('offer.html')

# Request a Service
@app.route('/request_service', methods=['GET', 'POST'])
def request_service():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        service = request.form['service']
        users[session['username']]['requests'].append(service)
        services.append({'type': 'request', 'user': session['username'], 'service': service})
        return redirect(url_for('dashboard'))
    return render_template('request.html')

# View all Services
@app.route('/view_services')
def view_services():
    return render_template('view_services.html', services=services)

# Exchange Time
@app.route('/exchange', methods=['GET', 'POST'])
def exchange():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        receiver = request.form['receiver']
        hours = int(request.form['hours'])

        sender = session['username']

        if receiver not in users:
            return "Receiver not found."

        if users[sender]['hours'] < hours:
            return "You don't have enough hours!"

        users[sender]['hours'] -= hours
        users[receiver]['hours'] += hours

        return redirect(url_for('dashboard'))
    return render_template('exchange.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

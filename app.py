from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json

import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Load users from JSON file
def load_users():
    with open('users.json', 'r') as f:
        return json.load(f)

# Save users to JSON file
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

# Generate a random 5-digit connection ID
def generate_connection_id():
    return str(random.randint(10000, 99999))

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/services')
def services_page():
    return render_template('services.html')

@app.route('/verify_user', methods=['POST'])
def verify_user():
    connection_id = request.form['connectionID']
    password = request.form['password']
    users = load_users()['users']
    
    for user in users:
        if user['connectionID'] == connection_id and user['password'] == password:
            return redirect(url_for('main_page', username=user['username'], connectionID=user['connectionID']))
    
    flash("Wrong Connection ID or Password!", 'error')
    return redirect(url_for('login'))

@app.route('/main')
def main_page():
    username = request.args.get('username')
    connectionID = request.args.get('connectionID')
    return render_template('main.html', username=username, connectionID=connectionID)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    first_name = request.form['first_name']
    email = request.form['email']
    new_contact = {
        "first_name": first_name,
        "email": email
    }
    try:
        with open('emails.json', 'r+') as file:
            contacts = json.load(file)
            contacts.append(new_contact)
            file.seek(0)
            json.dump(contacts, file, indent=4)
        return redirect(url_for('main_page'))
    except Exception as e:
        return redirect(url_for('main_page'))

@app.route('/settings')
def settings():
    username = request.args.get('username')
    connectionID = request.args.get('connectionID')
    return render_template('settings.html', username=username, connectionID=connectionID)

@app.route('/add_user_page')
def add_user_page():
    return render_template('add_user.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    new_username = request.form['username']
    users = load_users()
    
    # Check for duplicate username
    for user in users['users']:
        if user['username'] == new_username:
            flash(f'Error: Username "{new_username}" already exists!', 'error')
            return redirect(url_for('login'))
    
    connection_id = generate_connection_id()
    new_user = {
        "connectionID": connection_id,
        "password": request.form['password'],
        "username": new_username
    }
    
    users['users'].append(new_user)
    save_users(users)
    flash(f'User added successfully! Connection ID: {connection_id}', 'success')
    return redirect(url_for('login'))

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.route('/delete_user', methods=['POST'])
def delete_user():
    connection_id = request.form['connectionID']
    users = load_users()
    updated_users = [user for user in users['users'] if user['connectionID'] != connection_id]
    
    # Check if user was found and deleted
    if len(updated_users) == len(users['users']):
        flash('Error: User not found', 'error')
    else:
        users['users'] = updated_users
        save_users(users)
        flash('User deleted successfully', 'success')
    
    return redirect(url_for('login'))

@app.route('/run_virtual_assistant', methods=['POST'])
def run_virtual_assistant():
    try:
        print('i ran')
        import main
        main.main()
        return jsonify({'status': 'success', 'message': 'The task has been completed.'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/submit_service_request', methods=['POST'])
def submit_service_request():
    email = request.form['email']
    name = request.form['name']
    connection_id = request.form['connectionID']
    description = request.form['description']
    # Here you can process the service request, e.g., save it to a database
    flash(f'Thank you {name}, your request has been submitted.', 'success')
    return redirect(url_for('services_page'))

@app.route('/submit_rating', methods=['POST'])
def submit_rating():
    rating = request.form['rating']
    # Process the rating as needed
    flash('Thank you for your rating!', 'success')
    return redirect(url_for('main_page'))

@app.route('/submit_service_card_request', methods=['POST'])
def submit_service_card_request():
    data = request.get_json()
    service = data['service']
    username = data['username']
    # Process the service card request as needed
    flash(f'Thank you {username}, your request for {service} has been submitted. A team member will contact you as soon as possible.', 'success')
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)

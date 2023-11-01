import csv, ast
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

users = []


# Load user data from the CSV file
with open('users.csv', mode='r', newline='') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        users.append(row)

def update_users_csv():
    # Write the updated user data back to the CSV file
    with open('users.csv', mode='w', newline='') as file:
        fieldnames = ['id', 'username', 'email', 'password', 'nid', 'location']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(users)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/profile')
def profile():
    if 'user_id' in session:
        user_id = session['user_id']
        user = users[user_id - 1]
        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('login'))

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' in session:
        user_id = session['user_id']
        user = users[user_id - 1]

        if request.method == 'POST':
            # Update the user's profile data based on the form submission
            user['username'] = request.form['username']
            user['email'] = request.form['email']

            # Write the updated user data back to the CSV file
            with open('users.csv', mode='w', newline='') as file:
                fieldnames = ['id', 'username', 'email', 'password']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(users)

            flash('Profile updated successfully')
            return redirect(url_for('profile'))

        return render_template('edit_profile.html', user=user)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        for user in users:
            if user['username'] == username and user['password'] == password:
                session['user_id'] = int(user['id'])
                return redirect(url_for('profile'))

        flash('Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the user session to log the user out
    session.pop('user_id', None)
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        nid = request.form['nid']
        location = request.form['location']

        # Check if the username is already in use
        for user in users:
            if user['username'] == username:
                flash('Username already exists')
                return render_template('register.html')

        # Generate a new user ID
        user_id = len(users) + 1

        # Add the new user to the users list
        new_user = {
            'id': user_id,
            'username': username,
            'email': email,
            'password': password,
            'nid': nid,
            'location': location,
        }
        users.append(new_user)
        update_users_csv()

        flash('Registration successful. Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')

def read_dorm_room_details():
    try:
        with open('dorm_room_details.txt', 'r') as file:
            data = file.read()
            dorm_rooms = ast.literal_eval(data)
        return dorm_rooms
    except (FileNotFoundError, SyntaxError, ValueError, IOError):
        return []

dorm_rooms = read_dorm_room_details()

@app.route('/dorm_room_details')
def dorm_room_details():
    return render_template('dorm_room_details.html', dorm_rooms=dorm_rooms)

@app.route('/room_detail/<int:room_id>')
def room_detail(room_id):
    if 1 <= room_id <= len(dorm_rooms):
        room = dorm_rooms[room_id - 1]
        return render_template('room_detail.html', room=room)
    else:
        return "Room not found", 404



app.run(debug=True)

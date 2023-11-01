from flask import Flask, render_template, request, redirect, url_for, session, flash
import ast
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

users = []

with open('users.csv', 'r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        users.append({
            'id': int(row['id']),
            'username': row['username'],
            'email': row['email'],
            'password': row['password']  # Add a 'password' field to your users.csv
        })

# Replace the code for loading dorm room details
with open("dorm_room_details.txt", "r") as file:
    dorm_room_details_data = file.read()

# Parse the dorm room details data as a Python list of dictionaries using eval
dorm_room_details = eval(dorm_room_details_data)

# Now you have the dorm room details in the `dorm_room_details` list.

# Rest of the code remains the same

def is_logged_in():
    return 'user_id' in session

def save_users():
    with open('users.csv', 'w', newline='') as file:
        fieldnames = ['id', 'username', 'email', 'password']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(users)

@app.route('/')
def home():
    return render_template('home.html', latest_dorm_rooms=dorm_room_details[-12:], popular_dorm_rooms=sorted(dorm_room_details, key=lambda x: x['popularity'], reverse=True)[:3])

# Replace the routes that deal with articles with dorm room details

@app.route('/dorm_room/<int:dorm_room_id>')
def dorm_room(dorm_room_id):
    dorm_room = next((room for room in dorm_room_details if room['id'] == dorm_room_id), None)
    if dorm_room:
        return render_template('dorm_room.html', dorm_room=dorm_room)
    return "Dorm room not found"

@app.route('/dorm_rooms/<dorm_room_type>')
def dorm_room_type(dorm_room_type):
    dorm_rooms_of_type = [room for room in dorm_room_details if room['type'] == dorm_room_type]
    return render_template('dorm_room_type.html', dorm_room_type=dorm_room_type, dorm_rooms=dorm_rooms_of_type)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = next((user for user in users if user['username'] == username and user['password'] == password), None)
        if user:
            session['user_id'] = user['id']  # Store the user's ID in the session
            return redirect(url_for('user_profile'))
        else:
            flash('Login failed. Please check your username and password or register if you are a new user.', 'error')
            return redirect(url_for('register'))

    return render_template('login.html')


@app.route('/user_profile')
def user_profile():
    if is_logged_in():
        user_id = session['user_id']
        user = next((user for user in users if user['id'] == user_id), None)
        if user:
            return render_template('user_profile.html', user=user)
    return redirect(url_for('login'))

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if not is_logged_in():
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = next((user for user in users if user['id'] == user_id), None)

    if request.method == 'POST':
        # Update user profile information here based on form data
        user['username'] = request.form.get('username')
        user['email'] = request.form.get('email')

        # Save the updated user list to the CSV file
        save_users()

        flash('Profile updated successfully.', 'success')
        return redirect(url_for('user_profile'))

    return render_template('edit_profile.html', user=user)


@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user_id from the session
    return redirect(url_for('login'))

@app.route('/admin_profile')
def admin_profile():
    if is_logged_in():
        user_id = session['user_id']
        user = next((user for users in users if user['id'] == user_id), None)
        if user:
            # Check if the user is an admin (you can add an 'is_admin' field to your users.csv)
            if user.get('is_admin', False):
                # Render the admin profile template
                return render_template('admin_profile.html', user=user)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the email is already registered
        if any(user['email'] == email for user in users):
            return "Email already registered. Please choose a different email or try logging in."

        # Find the max user ID and generate a new ID
        max_id = max(user['id'] for user in users) if users else 0
        new_user_id = max_id + 1

        # Create a new user
        new_user = {
            'id': new_user_id,
            'username': username,
            'email': email,
            'password': password  # In a real application, you should hash the password
        }

        # Append the new user to the list and save the list to the CSV file
        users.append(new_user)

        # Save the updated user list
        save_users()

        # Redirect to the login page
        return redirect(url_for('login'))

    return render_template('register.html')


app.run(debug=True)

from flask import Flask, render_template, request, redirect, session, flash  
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="V@nshu04",
    database="DesInk"
)
cursor = conn.cursor()
# Function to authenticate user
def authenticate_user(username_email):
    query = "SELECT * FROM Customer WHERE (email = %s OR custName = %s)"
    cursor.execute(query, (username_email, username_email))
    user = cursor.fetchone()
    return user
# Function to authenticate designer
def authenticate_designer(username_email, password):
    query = "SELECT * FROM Designer WHERE (email = %s OR desName = %s) AND password = %s"
    cursor.execute(query, (username_email, username_email, password))
    user = cursor.fetchone()
    return user
# Function to get available items for ordering
def get_available_items():
    cursor.execute("SELECT productID, title, price FROM Product WHERE availableUnits > 0")
    return cursor.fetchall()

# Function to get items in user's cart
def get_cart_items(customer_name):
    cursor.execute("SELECT productID, quantity FROM CartItem WHERE cartID IN (SELECT cartID FROM Cart WHERE custName = %s)", (customer_name,))
    return cursor.fetchall()

# Function to fetch all tables and their data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/customer/login', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'POST':
        username_email = request.form['username_email']
        password = request.form['password']

        # Authenticate user
        user = authenticate_user(username_email)
        if user:
            if user[-1]:
                flash("Your account has been blocked due to multiple login failures. Please contact support.", 'danger')
                return render_template('indexblocked.html')
            print(user)
            cursor.execute("INSERT INTO LoginAttempts (customer_id) VALUES (%s)", (user[0],))
            conn.commit()
            if user[2] == password:   # If the entered password matches the stored hash
                session['user_id'] = user[0]  # Set session variable with user ID
                cursor.execute("DELETE FROM LoginAttempts WHERE customer_id = %s", (user[0],))
                conn.commit()
                print(user)
                return redirect('/order')  # Redirect to order page
            else:
                return render_template('customer_login.html', message='Invalid password')
        else:
            return render_template('customer_login.html', message='Invalid username/email')

    return render_template('customer_login.html')

@app.route('/customer/signup', methods=['GET', 'POST'])
def customer_signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        custName = request.form['custName']

        # Insert customer data into the database
        try:
            cursor.execute("INSERT INTO Customer (custName,email, password, firstName, lastName) VALUES (%s,%s, %s, %s, %s)",
                           (custName,email, password, first_name, last_name))
            conn.commit()
            return redirect('/customer/login')  # Redirect to login page after successful signup
        except mysql.connector.Error as e:
            print("Error:", e)
            return render_template('error.html', message="Failed to sign up. Please try again.")

    return render_template('customer_signup.html')


@app.route('/designer/signup', methods=['GET', 'POST'])
def designer_signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        # Insert designer data into the database
        try:
            cursor.execute("INSERT INTO Designer (email, password, firstName, lastName) VALUES (%s, %s, %s, %s)",
                           (email, password, first_name, last_name))
            conn.commit()
            return redirect('/designer/login')  # Redirect to login page after successful signup
        except mysql.connector.Error as e:
            print("Error:", e)
            return render_template('error.html', message="Failed to sign up. Please try again.")

    return render_template('designer_signup.html')


@app.route('/designer/login', methods=['GET', 'POST'])
def designer_login():
    if request.method == 'POST':
        username_email = request.form['username_email']
        password = request.form['password']

        # Authenticate designer
        user = authenticate_designer(username_email, password)
        if user:
            session['user_id'] = user[0]  # Set session variable with user ID
            return redirect('/dashboard')  # Redirect to designer dashboard page
        else:
            return render_template('designer_login.html', message='Invalid username/email or password')

    return render_template('designer_login.html')


from flask import flash, session

@app.route('/order', methods=['GET', 'POST'])
def order():
    if 'user_id' not in session:
        return redirect('/')  # Redirect to login page if user is not authenticated

    customer_name = session['user_id']

    if request.method == 'POST':
        if 'place_order' in request.form:
            # Place order if the user has items in the cart
            cursor.execute("SELECT cartID FROM Cart WHERE custName = %s", (customer_name,))
            cart_info = cursor.fetchone()
            if cart_info:
                # Fetch cart details for placing order
                cursor.execute("SELECT ci.cartItemID, p.title, ci.quantity, ci.price FROM CartItem ci JOIN Product p ON ci.cartItemID = p.productID WHERE ci.cartID IN (SELECT cartID FROM Cart WHERE custName = %s)", (customer_name,))
                cart_details = cursor.fetchall()

                # Get total cart value
                cursor.execute("SELECT totalPrice FROM Cart WHERE custName = %s", (customer_name,))
                cart_value = cursor.fetchone()[0]

                return render_template('place_order.html', cart_details=cart_details, cart_value=cart_value)
            else:
                flash("Your cart is empty. Please add items before placing an order.", 'danger')
                return redirect('/order')
        else:
            # Add item to cart
            product_id = request.form['product_id']
            quantity = int(request.form['quantity'])

            # Check if the product exists and has enough available units
            cursor.execute("SELECT price, availableUnits, portfolioID FROM Product WHERE productID = %s", (product_id,))
            product_info = cursor.fetchone()
            if product_info:
                price = product_info[0]
                available_units = product_info[1]
                portfolio_id = product_info[2]

                if available_units >= quantity:
                    # Calculate the total price
                    total_price = price * quantity

                    # Create a new cart if it doesn't exist for the customer
                    cursor.execute("SELECT cartID FROM Cart WHERE custName = %s", (customer_name,))
                    cart_info = cursor.fetchone()
                    if not cart_info:
                        # If cart doesn't exist, create a new one and set total price to 0
                        cursor.execute("INSERT INTO Cart (cartID, custName, totalPrice) VALUES (UUID(), %s, 0)", (customer_name,))
                        conn.commit()

                    # Get the cart ID
                    cursor.execute("SELECT cartID FROM Cart WHERE custName = %s", (customer_name,))
                    cart_id = cursor.fetchone()[0]

                    # Insert the item into the cart
                    cursor.execute("INSERT INTO CartItem (cartItemID, cartID, price, quantity, dateAdded) VALUES (%s, %s, %s, %s, NOW())", (product_id, cart_id, price, quantity))
                    conn.commit()

                    # Update the total price in the cart
                    cursor.execute("UPDATE Cart SET totalPrice = totalPrice + %s WHERE cartID = %s", (total_price, cart_id))
                    conn.commit()

                    # Display success message
                    flash("Product added to cart successfully.", 'success')
                else:
                    flash("Insufficient available units for the product.", 'danger')
            else:
                flash("Product not found.", 'danger')

            return redirect('/order')

    # Get available items for ordering
    cursor.execute("SELECT productID, title, price, availableUnits FROM Product WHERE availableUnits > 0")
    available_items = cursor.fetchall()

    # Get items in user's cart
    cursor.execute("SELECT cartItemID, quantity FROM CartItem WHERE cartID IN (SELECT cartID FROM Cart WHERE custName = %s)", (customer_name,))
    cart_items = cursor.fetchall()

    # Get total cart value
    cursor.execute("SELECT totalPrice FROM Cart WHERE custName = %s", (customer_name,))
    cart_value = cursor.fetchone()[0]

    return render_template('order.html', available_items=available_items, cart_items=cart_items, cart_value=cart_value)
@app.route('/place_order', methods=['GET', 'POST'])
def place_order():
    if 'user_id' not in session:
        return redirect('/')  # Redirect to login page if user is not authenticated

    customer_name = session['user_id']

    if request.method == 'POST':
        if 'confirm_order' in request.form:
            # Code to confirm and place the order
            # This could involve applying the discount code, updating the order status, etc.
            # You can add this logic based on your requirements

            # Check if a discount code was provided
            discount_code = request.form.get('discount_code')
            if discount_code:
                # Verify if the discount code exists and is valid
                cursor.execute("SELECT discountPercent FROM Discount WHERE discountCode = %s AND expirationDate >= CURDATE()", (discount_code,))
                discount_info = cursor.fetchone()
                if discount_info:
                    discount_percent = discount_info[0]
                    # Apply the discount to the total price
                    cursor.execute("SELECT totalPrice FROM Cart WHERE custName = %s", (customer_name,))
                    total_price = cursor.fetchone()[0]
                    discounted_price = total_price * (1 - discount_percent / 100)

                    # Update the order with the applied discount
                    cursor.execute("UPDATE `Order` SET discountID = (SELECT discountID FROM Discount WHERE discountCode = %s) WHERE cartID IN (SELECT cartID FROM Cart WHERE custName = %s)", (discount_code, customer_name))
                    conn.commit()

                    flash(f"Order placed successfully with {discount_percent}% discount applied. Total price: ${discounted_price:.2f}", 'success')
                    return redirect('/')
                else:
                    flash("Invalid or expired discount code. Order placement failed.", 'danger')
                    return redirect('/place_order')
            else:
                flash("Please provide a discount code to proceed with the order.", 'danger')
                return redirect('/place_order')

    # Fetch cart details for placing order
    cursor.execute("SELECT ci.cartItemID, p.title, ci.quantity, ci.price FROM CartItem ci JOIN Product p ON ci.cartItemID = p.productID WHERE ci.cartID IN (SELECT cartID FROM Cart WHERE custName = %s)", (customer_name,))
    cart_details = cursor.fetchall()

    # Get total cart value
    cursor.execute("SELECT totalPrice FROM Cart WHERE custName = %s", (customer_name,))
    cart_value = cursor.fetchone()[0]

    return render_template('place_order.html', cart_details=cart_details, cart_value=cart_value)

# Route to render the admin HTML page
@app.route('/admin')
def admin():
    try:
        # Fetch data for each table separately
        cursor.execute("SELECT * FROM Product") 
        product_data = cursor.fetchall()

        cursor.execute("SELECT * FROM Designer")
        designer_data = cursor.fetchall()

        cursor.execute("SELECT * FROM Customer")
        customer_data = cursor.fetchall()

        return render_template('admin.html', product_data=product_data, designer_data=designer_data, customer_data=customer_data)
    except Exception as e:
        print("Error:", e)
        return "An error occurred while fetching data."


if __name__ == '__main__':
    app.run(debug=True)


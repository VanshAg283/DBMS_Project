from flask import Flask, render_template, request, redirect, session, flash  
import mysql.connector
import re

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
            cursor.execute("INSERT INTO LoginAttempts (customer_id) VALUES (%s)", (user[0],))
            conn.commit()
            if user[2] == password:   # If the entered password matches the stored hash
                session['user_id'] = user[0]  # Set session variable with user ID
                cursor.execute("DELETE FROM LoginAttempts WHERE customer_id = %s", (user[0],))
                conn.commit()
                
                return redirect('/product')  # Redirect to order page
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

        try:
            # Query the last cartID in the Cart table
            cursor.execute("SELECT cartID FROM Cart ORDER BY cartID DESC LIMIT 1")
            last_cart_id = cursor.fetchone()

            # Extract the numeric part from the last cartID and increment it
            if last_cart_id:
                last_cart_id_number = int(re.search(r'\d+', last_cart_id[0]).group())
                new_cart_id_number = last_cart_id_number + 1
                new_cart_id = f'C{new_cart_id_number:02d}'  # Format the new cartID

                # Insert customer data into the database
                cursor.execute("INSERT INTO Customer (custName, email, password, firstName, lastName) VALUES (%s, %s, %s, %s, %s)",
                               (custName, email, password, first_name, last_name))

                # Insert a new row into the Cart table with the generated cartID and customer's name
                cursor.execute("INSERT INTO Cart (cartID, custName) VALUES (%s, %s)", (new_cart_id, custName))

                conn.commit()
                return redirect('/customer/login')  # Redirect to login page after successful signup
            else:
                # No existing cartID found, handle this case
                print("Error: Unable to generate a new cart ID.")
                return render_template('error.html', message="Failed to sign up. Please try again.")

        except mysql.connector.Error as e:
            # Handle duplicate entry error
            if e.errno == 1062 :
                return render_template('customer_signup.html', message="An account with the same username already exists.")
            elif e.errno == 1644:
                return render_template('customer_signup.html', message="An account with the same email already exists.")
            print("Error:", e)
            return render_template('error.html', message="Failed to sign up. Please try again.")

    return render_template('customer_signup.html')

@app.route('/designer/signup', methods=['GET', 'POST'])
def designer_signup():
    if request.method == 'POST':
        desName = request.form['desName']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        portfolioID = request.form['portfolioID']
        error = 0

        # Insert designer data into the database
        try:
            cursor.execute("INSERT INTO Designer (desName, email, password, firstname, lastname) VALUES (%s, %s, %s, %s, %s)",
                           (desName, email, password, first_name, last_name))
            conn.commit()
            error = 1

            cursor.execute("INSERT INTO Portfolio (portfolioID, desName) VALUES (%s, %s)", (portfolioID, desName))
            conn.commit()
            error = 2

            cursor.execute("UPDATE Designer SET portfolioID = %s WHERE desName = %s", (portfolioID, desName))
            conn.commit()

            return redirect('/designer/login')  # Redirect to login page after successful signup
        
        except mysql.connector.Error as e:
            print("Error:", e)
            if error == 0:
                return render_template('designer_signup.html', message="Email/Username already exists. Please try again.")
            elif error == 1:
                cursor.execute("DELETE FROM Designer WHERE desName = %s", (desName,))
                conn.commit()
                return render_template('designer_signup.html', message="Portfolio Name already exists. Please try again.")
            else:
                return render_template('designer_signup.html', message="Failed to sign up. Please try again.")      

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


@app.route('/product', methods=['GET', 'POST'])
def product():
    if 'user_id' not in session:
        return redirect('/')
    
    customer_name = session['user_id']

    cursor.execute("SELECT * from Product where availableUnits > maxUnitsCap")
    available_items = cursor.fetchall()

    if request.method == 'POST':
        for key, value in request.form.items():
            if int(value) > 0:
                # Add item to cart
                product_id = key
                quantity = int(value)

                # Check if the product exists and has enough available units
                cursor.execute("SELECT price, availableUnits, maxUnitsCap FROM Product WHERE productID = %s", (product_id,))
                product_info = cursor.fetchone()
                if product_info:
                    price = product_info[0]
                    available_units = product_info[1]
                    max_units_cap = product_info[2]

                    if available_units >= quantity:
                        # Calculate the total price
                        total_price = price * quantity

                        # Get the cart ID
                        cursor.execute("SELECT cartID FROM Cart WHERE custName = %s", (customer_name,))
                        cart_id = cursor.fetchone()[0]

                        # Check if product already exists in the cart
                        cursor.execute("SELECT * FROM CartItem WHERE cartID = %s AND cartItemID = %s", (cart_id, product_id))
                        existing_item = cursor.fetchone()
                        if existing_item:
                            # Update the quantity of the existing item only if maxUnitsCap is not exceeded
                            if existing_item[3] + quantity > max_units_cap:
                                message = "Exceeded the maximum units cap for the product."
                                return render_template('product.html', message=message, available_items=available_items)
                            cursor.execute("UPDATE CartItem SET quantity = quantity + %s WHERE cartID = %s AND cartItemID = %s", (quantity, cart_id, product_id))
                            conn.commit()

                            # Update the total price in the cart
                            cursor.execute("UPDATE Cart SET totalPrice = totalPrice + %s WHERE cartID = %s", (total_price, cart_id))
                            conn.commit()
                        else:
                            # Insert the item into the cart
                            cursor.execute("INSERT INTO CartItem (cartItemID, cartID, price, quantity, dateAdded) VALUES (%s, %s, %s, %s, NOW())", (product_id, cart_id, price, quantity))
                            conn.commit()
                        # Display success message
                        flash("Product added to cart successfully.", 'success')
                    else:
                        flash("Insufficient available units for the product.", 'danger')
                else:
                    flash("Product not found.", 'danger')
        
        return redirect('/order')


    return render_template('product.html', available_items=available_items)


@app.route('/order', methods=['GET', 'POST'])
def order():
    if 'user_id' not in session:
        return redirect('/')  # Redirect to login page if user is not authenticated

    customer_name = session['user_id']

    if request.method == 'POST':
        if 'place_order' in request.form:
            # Place order if the user has items in the cart
            cursor.execute("SELECT cartID, totalPrice FROM Cart WHERE custName = %s", (customer_name,))
            cart_info = cursor.fetchone()
            if cart_info[1] > 0:
                # Fetch cart details for placing order
                cursor.execute("SELECT ci.cartItemID, p.title, ci.quantity, ci.price FROM CartItem ci JOIN Product p ON ci.cartItemID = p.productID WHERE ci.cartID IN (SELECT cartID FROM Cart WHERE custName = %s)", (customer_name,))
                cart_details = cursor.fetchall()

                
                cart_value = cart_info[1]

                # Check if same order details already in order table and delstatus is processing
                cursor.execute("SELECT * FROM `Order` WHERE cartID = %s AND delStatus = 'Processing'", (cart_info[0],))
                existing_order = cursor.fetchone()
                if existing_order:
                    return redirect('/choose_address')  # If yes, go directly to address page

                cursor.execute("INSERT INTO `Order` (orderDate, delStatus, custName, cartID) VALUES (NOW(), 'Processing', %s, %s)", (customer_name, cart_info[0]))
                conn.commit()

                return redirect('/choose_address')
            else:
                flash("Your cart is empty. Please add items before placing an order.", 'danger')
                return redirect('/order')
        
        elif 'cancel_order' in request.form:
            cancelled_order_id = request.form.get('order_id')
            cursor.execute("DELETE FROM Transaction WHERE orderID = %s", (cancelled_order_id,))
            conn.commit()
            cursor.execute("DELETE FROM `Order` WHERE orderID = %s", (cancelled_order_id,))
            conn.commit()
            return redirect('/order')
        
    # Get items in user's cart
    cursor.execute("SELECT cartItemID, quantity FROM CartItem WHERE cartID IN (SELECT cartID FROM Cart WHERE custName = %s)", (customer_name,))
    cart_items = cursor.fetchall()
    # Get product name from cartItemID
    for i in range(len(cart_items)):
        cursor.execute("SELECT title FROM Product WHERE productID = %s", (cart_items[i][0],))
        product_name = cursor.fetchone()
        cart_items[i] = cart_items[i] + product_name
    # Get total cart value
    cursor.execute("SELECT totalPrice FROM Cart WHERE custName = %s", (customer_name,))
    cart_value = cursor.fetchone()[0]

    # Check if there is an order not in processing state
    cursor.execute("SELECT * FROM `Order`  WHERE custName = %s AND delStatus != 'Processing'", (customer_name,))
    existing_order = cursor.fetchall()

    return render_template('order.html', cart_items=cart_items, cart_value=cart_value, existing_order=existing_order)

@app.route('/choose_address', methods=['GET', 'POST'])
def order_address():
    if 'user_id' not in session:
        return redirect('/')
    
    customer_name = session['user_id']

    cursor.execute("SELECT * FROM Address WHERE custName = %s", (customer_name,))
    addresses = cursor.fetchall()
    message = None

    if request.method == 'POST':
        if 'add_address' in request.form:
            return redirect('/add_address')
        
        elif 'place_order' in request.form:
            selected_address_id = request.form.get('selected_address')
            if selected_address_id:
                # Store the selected address ID in the session or wherever needed
                session['selected_address'] = selected_address_id

                # Store the addressID in customer order
                cursor.execute("SELECT orderID FROM `Order` WHERE cartID IN (SELECT cartID FROM Cart WHERE custName = %s) AND delStatus = 'Processing'", (customer_name,))
                order_id = cursor.fetchone()[0]
                cursor.execute("UPDATE `Order` SET addressID = %s WHERE orderID = %s", (selected_address_id, order_id))  # Fetches the last inserted id of the order
                conn.commit()
                return redirect('/place_order')
            else:
                message = "Please select an address to proceed."
    
    return render_template('order_address.html', addresses=addresses, message=message)

@app.route('/add_address', methods=['GET', 'POST'])
def add_address():
    if 'user_id' not in session:
        return redirect('/')
    
    if request.method == 'POST':
        houseNo = request.form['House_No']
        street = request.form['Street']
        city = request.form['City']
        state = request.form['State']
        zip_code = request.form['zip_code']

        # Add only if address is not already present for this user
        cursor.execute("SELECT * FROM Address WHERE houseNo = %s AND street = %s AND city = %s AND state = %s AND pincode = %s AND custName = %s", (houseNo, street, city, state, zip_code, session['user_id']))
        existing_address = cursor.fetchone()
        if existing_address:
            flash("Address already exists. Please select it from the list.", 'warning')
            return redirect('/choose_address')

        # Query last addressID in the Address table
        cursor.execute("SELECT addressID FROM Address ORDER BY addressID DESC LIMIT 1")
        last_address_id = cursor.fetchone()

        # Extract the numeric part from the last addressID and increment it
        if last_address_id:
            last_address_id_number = int(re.search(r'\d+', last_address_id[0]).group())
            new_address_id_number = last_address_id_number + 1
            new_address_id = f'A{new_address_id_number:03d}'
        
        customer_name = session['user_id']
        cursor.execute("INSERT INTO Address (addressID, houseNo, street, city, state, pincode, custName) VALUES (%s, %s, %s, %s, %s, %s, %s)", (new_address_id, houseNo, street, city, state, zip_code, customer_name))
        conn.commit()

        flash("Address added successfully.", 'success')

        return redirect('/choose_address')
    

    return render_template('add_address.html')


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
                cursor.execute("SELECT discountPercent, discountID FROM Discount WHERE discountCode = %s AND expirationDate >= CURDATE()", (discount_code,))
                discount_info = cursor.fetchone()
                if discount_info:
                    discount_percent = discount_info[0]
                    discountID = discount_info[1]
                    # Apply the discount to the total price
                    cursor.execute("SELECT totalPrice FROM Cart WHERE custName = %s", (customer_name,))
                    total_price = cursor.fetchone()[0]
                    discounted_price = total_price * (1 - discount_percent / 100)

                    # Update the order with the applied discount where delStatus is 'Processing'
                    cursor.execute("UPDATE `Order` SET discountID = %s WHERE cartID IN (SELECT cartID FROM Cart WHERE custName = %s) AND delStatus = 'Processing'", (discountID, customer_name))
                    conn.commit()


                    cursor.execute("SELECT orderID FROM `Order` WHERE cartID IN (SELECT cartID FROM Cart WHERE custName = %s) AND delStatus = 'Processing'", (customer_name,))
                    order_id = cursor.fetchone()[0]

                    cursor.execute("INSERT INTO transaction (discountID, custName, orderID) VALUES (%s, %s, %s)", (discountID, customer_name, order_id))
                    conn.commit()

                    update_query = """
                    UPDATE Transaction t
                    SET transactionPrice = (
                        SELECT (c.totalPrice - (c.totalPrice * d.discountPercent / 100))
                        FROM Cart c
                        JOIN Discount d ON t.discountID = d.discountID
                        JOIN `Order` o ON t.orderID = o.orderID
                        WHERE o.cartID = c.cartID
                    ) """
                    cursor.execute(update_query)
                    conn.commit()

                    # Update delStatus to 'Confirmed'
                    cursor.execute("UPDATE `Order` SET delStatus = 'Confirmed' WHERE cartID IN (SELECT cartID FROM Cart WHERE custName = %s) AND delStatus = 'Processing'", (customer_name,))
                    conn.commit()

                    cursor.execute("DELETE FROM CartItem WHERE cartID IN (SELECT cartID FROM Cart WHERE custName = %s)", (customer_name,))
                    conn.commit()

                    cursor.execute("UPDATE Cart SET totalPrice = %s WHERE custName = %s", (0, customer_name))
                    conn.commit()

                    flash(f"Order placed successfully with {discount_percent}% discount applied. Total price: ${discounted_price:.2f}", 'success')
                    return render_template('order_success.html', message=f"Order placed successfully with {discount_percent}% discount applied. Total price: ${discounted_price:.2f}")
                else:
                    flash("Invalid or expired discount code. Order placement failed.", 'danger')
                    return redirect('/place_order')
            else:
                # No need to apply discount
                cursor.execute("SELECT totalPrice FROM Cart WHERE custName = %s", (customer_name,))
                total_price = cursor.fetchone()[0]

                cursor.execute("SELECT orderID FROM `Order` WHERE cartID IN (SELECT cartID FROM Cart WHERE custName = %s) AND delStatus = 'Processing'", (customer_name,))
                order_id = cursor.fetchone()[0]
                

                cursor.execute("INSERT INTO transaction (custName, orderID, transactionPrice) VALUES (%s, %s, %s)", (customer_name, order_id, total_price))
                conn.commit()

                # Update delStatus to 'Confirmed'
                cursor.execute("UPDATE `Order` SET delStatus = 'Confirmed' WHERE cartID IN (SELECT cartID FROM Cart WHERE custName = %s) AND delStatus = 'Processing'", (customer_name,))
                conn.commit()

                cursor.execute("DELETE FROM CartItem WHERE cartID IN (SELECT cartID FROM Cart WHERE custName = %s)", (customer_name,))
                conn.commit()

                cursor.execute("UPDATE Cart SET totalPrice = %s WHERE custName = %s", (0, customer_name))
                conn.commit()

                flash(f"Order placed successfully. Total price: ${total_price:.2f}", 'success')
                return render_template('order_success.html', message=f"Order placed successfully. Total price: ${total_price:.2f}")



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
    if 'authenticated' in session and session['authenticated']:
        # Fetch data for each table separately
        cursor.execute("SELECT * FROM Product") 
        product_data = cursor.fetchall()

        cursor.execute("SELECT * FROM Designer")
        designer_data = cursor.fetchall()

        cursor.execute("SELECT * FROM Customer")
        customer_data = cursor.fetchall()

        return render_template('admin.html', product_data=product_data, designer_data=designer_data, customer_data=customer_data)
    else:
        return redirect('/')

# Predefined valid credentials
valid_credentials = {'username': 'root', 'password': 'root'}
# Route to render the login page
@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == valid_credentials['username'] and password == valid_credentials['password']:
            session['authenticated'] = True
            return redirect('/admin')
        else:
            return render_template('adminLogin.html', error=True)
    return render_template('adminLogin.html', error=False)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    
    desName = session['user_id']
    cursor.execute("SELECT portfolioID FROM Portfolio WHERE desName = %s", (desName,))
    portfolioID = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM Product WHERE portfolioID = %s", (portfolioID,))
    products = cursor.fetchall()

    if request.method == 'POST':
        return redirect('/add_product')

    return render_template('dashboard.html', products=products)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if 'user_id' not in session:
        return redirect('/')
    
    desName = session['user_id']
    cursor.execute("SELECT portfolioID FROM Portfolio WHERE desName = %s", (desName,))
    portfolioID = cursor.fetchone()[0]

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        price = request.form['price']
        available_units = request.form['available_units']
        max_units_cap = request.form['max_units']

        # Add only if product is not already present in the portfolio
        cursor.execute("SELECT * FROM Product WHERE title = %s AND portfolioID = %s", (title, portfolioID))
        existing_product = cursor.fetchone()
        if existing_product:
            flash("Product already exists in your portfolio. Please add a new product.", 'warning')
            return redirect('/dashboard')

        # Query last productID in the Product table
        cursor.execute("SELECT productID FROM Product ORDER BY productID DESC LIMIT 1")
        last_product_id = cursor.fetchone()

        # Extract the numeric part from the last productID and increment it
        if last_product_id:
            last_product_id_number = int(re.search(r'\d+', last_product_id[0]).group())
            new_product_id_number = last_product_id_number + 1
            new_product_id = f'P{new_product_id_number:03d}'
        else:
            new_product_id = 'P001'

        cursor.execute("INSERT INTO Product (productID, title, content, category, price, availableUnits, maxUnitsCap, portfolioID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (new_product_id, title, description, category, price, available_units, max_units_cap, portfolioID))
        conn.commit()

        flash("Product added successfully.", 'success')
        return redirect('/dashboard')

    return render_template('add_product.html')



if __name__ == '__main__':
    app.run(debug=True)



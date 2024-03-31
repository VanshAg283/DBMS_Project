import mysql.connector

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="DesInk"
)
print(f"Connnection Details : \n{conn}\n------------------------------------")
cursor = conn.cursor()

# Function to place an order
def place_order(customer_name, product_id, quantity, discount_code=None):
    try:
        # Check if product exists and has sufficient available units
        cursor.execute("SELECT availableUnits, price FROM Product WHERE productID = %s", (product_id,))
        product = cursor.fetchone()
        if product is None:
            print("Product not found.")
            return
        available_units, price = product
        if quantity > available_units:
            print("Not enough available units for this product.")
            return

        # Calculate total price
        total_price = price * quantity

        # Fetch discount percentage if discount code is provided
        if discount_code:
            cursor.execute("SELECT discountPercent FROM Discount WHERE discountCode = %s", (discount_code,))
            discount = cursor.fetchone()
            if discount:
                discount_percent = discount[0]
                total_price *= (1 - discount_percent / 100)

        # Create a new cart for the customer if not already existing
        cursor.execute("SELECT cartID FROM Cart WHERE custName = %s", (customer_name,))
        cart = cursor.fetchone()
        if cart is None:
            cursor.execute("INSERT INTO Cart (custName) VALUES (%s)", (customer_name,))
            conn.commit()
            cart_id = cursor.lastrowid
        else:
            cart_id = cart[0]

        # Add item to cart
        cursor.execute("INSERT INTO CartItem (cartID, price, quantity, dateAdded) VALUES (%s, %s, %s, NOW())",
                       (cart_id, price, quantity))
        conn.commit()

        # Update product available units
        updated_units = available_units - quantity
        cursor.execute("UPDATE Product SET availableUnits = %s WHERE productID = %s", (updated_units, product_id))
        conn.commit()

        # Create order
        cursor.execute("INSERT INTO `Order` (orderDate, delStatus, custName, cartID, totalPrice) VALUES (NOW(), 'Processing', %s, %s, %s)",
                       (customer_name, cart_id, total_price))
        conn.commit()

        print("Order placed successfully.")
    except mysql.connector.Error as e:
        print("Error placing order:", e)

# Example usage
place_order("John", "P001", 2, "D07")

# Close cursor and connection
cursor.close()
conn.close()

from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import mysql.connector

app = Flask(__name__, static_folder="static")
app = Flask(__name__, template_folder="templates")
app.secret_key = "123" 



# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ujjawal@@",
    database="Hotel_Management_System"
    
)
cursor = db.cursor(buffered=True)

@app.route("/")
def home():
    return render_template("login.html")

# Login check (POST)
@app.route("/login", methods=[ "GET","POST"])

def login():
    name = request.form["name"]
    password = request.form["password"]

    sql = "SELECT * FROM register WHERE FirstName=%s AND password=%s"
    cursor.execute(sql, (name, password))
    user = cursor.fetchone()

    if user:
        return "success"
    else:
        return "Invalid username or password"
    
    
    



# Forgot page
@app.route("/forgot", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        PhoneNumber = request.form["PhoneNumber"]
        Email = request.form["Email"]
        password = request.form["password"]

        sql = "UPDATE  register  set password=%s where Email=%s and   PhoneNumber=%s"
        cursor.execute(sql, (password, Email, PhoneNumber))
        db.commit()

        if cursor.rowcount > 0:
            return "Password updated successfully"
        else:
            return "User not found"

    return render_template("forgot.html")

   

# Register page
@app.route("/register", methods=["GET", "POST"])
def register():
    print(request.form)
    if request.method == "POST":
        firstName = request.form["FirstName"]
        lastName = request.form["LastName"]
        email = request.form["email"]
        mobileNumber = request.form["phone"]
        newPassword = request.form["newpassword"]
        confirmPassword = request.form["conformpassword"]

        if newPassword != confirmPassword:
            return "Passwords do not match"

        sql = """
        INSERT INTO register 
        (FirstName, LastName, Email, PhoneNumber, password)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (firstName, lastName, email, mobileNumber, newPassword))
        db.commit()

        return "Registration successful"

    return render_template("register.html")




# Dashboard page
@app.route("/drashboard")
def dashboard():
    return render_template("drashboard.html")


#customer page

@app.route("/customer")
def customer():
    cursor.execute("SELECT Room_no FROM Rooms" )
    rooms = cursor.fetchall()
    return render_template("customer.html", rooms=rooms)

@app.route("/add_customer", methods=["POST"])
def add_customer():
    data = request.json
    
    sql = """
    INSERT INTO customer_info
    (CustomerID, CustomerName, FatherName, MotherName, Gender, RoomNo, Mobile, Email, Nationality, IdProof, IdNumber, Address)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    
    values = (
        data["customerId"],
        data["name"],
        data["father"],
        data["mother"],
        data["gender"],
        data["room"],
        data["mobile"],
        data["email"],
        data["nation"],
        data["idproof"],
        data["idnumber"],
        data["address"]
    )
    
    try:
        cursor.execute(sql, values)
        db.commit()
        return jsonify({"message": "Customer added successfully"})
    except Exception as e:
        return jsonify({"message": "Error: " + str(e)})


@app.route("/get_customer")
def get_customer():
    cursor.execute("""
        SELECT referenceNo, CustomerID, CustomerName, FatherName, MotherName,
               Gender, RoomNo, Mobile, Email, Nationality, IdProof,
               IdNumber, Address
        FROM customer_info
    """)
    rows = cursor.fetchall()

    customers = []
    for r in rows:
        customers.append({
            "referenceNo": r[0],
            "customerId": r[1],
            "customerName": r[2],
            "FatherName": r[3],
            "MotherName": r[4],
            "Gender": r[5],
            "RoomNo": r[6],
            "Mobile": r[7],
            "Email": r[8],
            "Nationality": r[9],
            "IdProof": r[10],
            "IdNumber": r[11],
            "Address": r[12]
        })

    return jsonify(customers)

    

# update customer data
@app.route("/update_customer", methods=["PUT"])
def update_customer():
    try:
        data = request.get_json()

        SQL = """
        UPDATE customer_info SET
            CustomerId=%s,
            CustomerName=%s,
            FatherName=%s,
            MotherName=%s,
            Gender=%s,
            RoomNo=%s,
            Mobile=%s,
            Email=%s,
            Nationality=%s,
            IdProof=%s,
            IdNumber=%s,
            Address=%s
        WHERE referenceNo=%s
        """

        values = (
            data.get("customerId"),
            data.get("name"),
            data.get("father"),
            data.get("mother"),
            data.get("gender"),
            data.get("room"),
            data.get("mobile"),
            data.get("email"),
            data.get("nation"),
            data.get("idproof"),
            data.get("idnumber"),
            data.get("address"),
            data.get("referenceNo")
        )

        cursor.execute(SQL, values)
        db.commit()

        return jsonify({"message": "Customer updated successfully"})

    except Exception as e:
        print("UPDATE ERROR:", e)  
        return jsonify({"error": str(e)}),




#delete customer data
@app.route("/delete_customer/<int:referenceNo>", methods=["DELETE"])
def delete_customer(referenceNo):
    try:
        #
        sql = "DELETE FROM customer_info WHERE referenceNo = %s"
        cursor.execute(sql, (referenceNo,))  

        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Customer not found"}),

        return jsonify({"message": "Customer deleted successfully"}), 
    except Exception as e:
        print("DELETE ERROR:", e)
        return jsonify({"message": str(e)}), 

 # search customer data
@app.route("/searchCustomer", methods=["POST"])
def search_customer():
    data = request.json
    field = data.get("field")
    value = data.get("value")

    if field not in ["Mobile", "CustomerName"]:
        return jsonify([])  

    try:
        sql = f"SELECT * FROM customer_info WHERE {field} LIKE %s"
        cursor.execute(sql, ("%" + value + "%",))
        rows = cursor.fetchall()
        customers = []
        for row in rows:
            customers.append({
                "referenceNo": row[0],
                "customerId": row[1],
                "customerName": row[2],
                "FatherName": row[3],
                "MotherName": row[4],
                "Gender": row[5],
                "RoomNo": row[6],
                "Mobile": row[7],
                "Email": row[8],
                "Nationality": row[9],
                "IdProof": row[10],
                "IdNumber": row[11],
                "Address": row[12]
            })

        return jsonify(customers)

    except Exception as e:
        print("SEARCH ERROR:", e)
        return jsonify([])


# STAFF PAGE
@app.route("/staff")
def staff():
    return render_template("staff.html")

# ADD STAFF
@app.route("/add_staff", methods=["POST"])
def add_staff():
    data = request.json
    SQL = """ 
    INSERT INTO staff_info(
        FirstName, LastName, FatherName, MotherName, Role, Gender, Mobile,
        Email, Nationality, IdProof, IdNumber, Address
    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    VALUES = (
        data["FirstName"], data["LastName"], data["FatherName"], data["MotherName"],
        data["Role"], data["Gender"], data["Mobile"], data["Email"],
        data["Nationality"], data["IdProof"], data["IdNumber"], data["Address"]
    )
    try:
        cursor.execute(SQL, VALUES)
        db.commit()
        return jsonify({"message":"Staff added successfully"})
    except Exception as e:
        return jsonify({"message": "Error: " + str(e)}), 500

# GET STAFF
@app.route("/get_staff")
def get_staff():
    try:
        cursor.execute("SELECT * FROM staff_info")
        rows = cursor.fetchall()
        staff = []
        for s in rows:
            staff.append({
                "Id": s[0],
                "FirstName": s[1],
                "LastName": s[2],
                "FatherName": s[3],
                "MotherName": s[4],
                "Role": s[5],
                "Gender": s[6],
                "Mobile": s[7],
                "Email": s[8],
                "Nationality": s[9],
                "IdProof": s[10],
                "IdNumber": s[11],
                "Address": s[12]
            })
        return jsonify(staff)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# UPDATE STAFF
@app.route("/update_staff", methods=["PUT"])
def update_staff():
    try:
        data = request.get_json()
        SQL = """UPDATE staff_info SET
            FirstName=%s, LastName=%s, FatherName=%s, MotherName=%s,
            Role=%s, Gender=%s, Mobile=%s, Email=%s, Nationality=%s,
            IdProof=%s, IdNumber=%s, Address=%s
            WHERE Id=%s
        """
        values = (
            data["FirstName"], data["LastName"], data["FatherName"], data["MotherName"],
            data["Role"], data["Gender"], data["Mobile"], data["Email"],
            data["Nationality"], data["IdProof"], data["IdNumber"], data["Address"],
            data["Id"]
        )
        cursor.execute(SQL, values)
        db.commit()
        return jsonify({"message": "Staff updated successfully"})
    except Exception as e:
        print("UPDATE ERROR:", e)
        return jsonify({"error": str(e)}), 500

# DELETE STAFF
@app.route("/delete_staff/<int:Id>", methods=["DELETE"])
def delete_staff(Id):
    try:
        cursor.execute("DELETE FROM staff_info WHERE Id=%s", (Id,))
        db.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Staff member not found"}), 404
        return jsonify({"message": "Staff member deleted successfully"})
    except Exception as e:
        print("DELETE ERROR:", e)
        return jsonify({"message": str(e)}), 500

# SEARCH STAFF
@app.route("/search_staff", methods=["POST"])
def search_staff():
    data = request.json
    Field = data.get("Field")
    Value = data.get("value", "") 

    allowed_fields = ["Mobile", "FirstName", "Role"]
    if Field not in allowed_fields:
        return jsonify([])

    try:
        sql = f"SELECT * FROM staff_info WHERE {Field} LIKE %s"
        cursor.execute(sql, ("%" + Value + "%",))
        rows = cursor.fetchall()
        staff = []
        for s in rows:
            staff.append({
                "Id": s[0],
                "FirstName": s[1],
                "LastName": s[2],
                "FatherName": s[3],
                "MotherName": s[4],
                "Role": s[5],
                "Gender": s[6],
                "Mobile": s[7],
                "Email": s[8],
                "Nationality": s[9],
                "IdProof": s[10],
                "IdNumber": s[11],
                "Address": s[12]
            })
        return jsonify(staff)
    except Exception as e:
        print("SEARCH ERROR:", e)
        return jsonify([]), 

# room page

@app.route("/roomss")
def rooms():
    cursor.execute("SELECT * FROM Rooms")
    rooms = cursor.fetchall()
    return render_template("roomss.html", rooms=rooms)


#booking page


# Booking page
@app.route("/booking")
def booking():
    cursor.execute("SELECT CustomerID FROM customer_info")
    customer_info = cursor.fetchall()
    return render_template("booking.html", customer_info=customer_info)

# Add booking
@app.route("/add_booking", methods=["POST"])
def add_booking():
    data = request.json
    try:
        sql = "INSERT INTO Booking (Customer_ID, Room_no, check_in) VALUES (%s,%s,%s)"
        val = (data["Customer_ID"], data["Room_no"], data["check_in"])
        cursor.execute(sql, val)
        db.commit()
        return jsonify({"message":"Booking added successfully"})
    except Exception as e:
        return jsonify({"message":"Error: " + str(e)}), 500

# Get all bookings
@app.route("/get_booking")
def get_booking():
    cursor.execute("SELECT BookingID, Customer_ID, Room_no, check_in FROM Booking")
    rows = cursor.fetchall()
    data = []
    for r in rows:
        data.append({
            "BookingID": r[0],
            "Customer_ID": r[1],
            "Room_no": r[2],
            "check_in": str(r[3])
        })
    return jsonify(data)

# Update booking
@app.route("/update_booking", methods=["POST"])
def update_booking():
    data = request.json
    try:
        sql = "UPDATE Booking SET Customer_ID=%s, Room_no=%s, check_in=%s WHERE BookingID=%s"
        val = (data["Customer_ID"], data["Room_no"], data["check_in"], data["BookingID"])
        cursor.execute(sql, val)
        db.commit()
        return jsonify({"message":"Booking updated successfully"})
    except Exception as e:
        return jsonify({"message":"Error: " + str(e)}), 500

# Delete booking
@app.route("/delete_booking/<int:BookingID>")
def delete_booking(BookingID):
    try:
        cursor.execute("DELETE FROM Booking WHERE BookingID=%s", (BookingID,))
        db.commit()
        return jsonify({"message":"Booking deleted successfully"})
    except Exception as e:
        return jsonify({"message":"Error: " + str(e)}), 500

# Get customer RoomNo for auto-fill
@app.route("/get_customer_room/<cid>")
def get_customer_room(cid):
    try:
        cursor.execute("SELECT RoomNo FROM customer_info WHERE CustomerID=%s", (cid,))
        row = cursor.fetchone()
        if row and row[0]:
            return jsonify({"Room_no": row[0]})
        else:
            return jsonify({"Room_no": ""})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


# Billing Page
# Billing page
@app.route("/billing")
def billing():
    cursor.execute("SELECT CustomerID FROM customer_info")
    customer_info = cursor.fetchall()
    return render_template("billing.html", customer_info=customer_info)


# Get customer room & price
@app.route("/get_customer_room_price/<cid>")
def get_customer_room_price(cid):
    try:
        cursor.execute("""
            SELECT customer_info.RoomNo, Rooms.RoomPrice
            FROM customer_info
            JOIN Rooms ON customer_info.RoomNo = Rooms.Room_no
            WHERE CustomerID = %s
        """, (cid,))
        row = cursor.fetchone()
        if row:
            return jsonify({"RoomNo": row[0], "price_per_night": row[1]})
        return jsonify({"RoomNo": "", "price_per_night": 0})
    except Exception as e:
        return jsonify({"error": str(e)})


# Add Billing
@app.route("/add_billing", methods=["POST"])
def add_billing():
    data = request.json
    sql = """
        INSERT INTO billing
        (Customer_ID, total_days, room_price, room_amount,
         tax_percent, tax_amount, extra_charges, discount, grand_total)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    values = (
        data["Customer_ID"],
        data["total_days"],
        data["room_price"],
        data["room_amount"],
        data["tax_percent"],
        data["tax_amount"],
        data["extra_charges"],
        data["discount"],
        data["grand_total"]
    )
    try:
        cursor.execute(sql, values)
        db.commit()
        return jsonify({"message": "Billing added successfully"})
    except Exception as e:
        return jsonify({"message": "Error: " + str(e)}), 500


# Get all Billing
@app.route("/get_billing")
def get_billing():
    try:
        cursor.execute("SELECT * FROM billing")
        rows = cursor.fetchall()
        billing = []
        for b in rows:
            billing.append({
                "bill_id": b[0],
                "Customer_ID": b[1],
                "total_days": b[2],
                "room_price": b[3],
                "room_amount": b[4],
                "tax_percent": b[5],
                "tax_amount": b[6],
                "extra_charges": b[7],
                "discount": b[8],
                "grand_total": b[9],
                "bill_date": str(b[10])
            })
        return jsonify(billing)
    except Exception as e:
        return jsonify({"error": str(e)})


# Delete Billing
@app.route("/delete_billing/<int:bill_id>")
def delete_billing(bill_id):
    try:
        cursor.execute("DELETE FROM billing WHERE bill_id=%s", (bill_id,))
        db.commit()
        return jsonify({"message": "Billing deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

# report page:

@app.route("/report")
def report():
    try:
        # Total rooms
        cursor.execute("SELECT COUNT(*) FROM Rooms")
        total_rooms = cursor.fetchone()[0]

        # Booked rooms (rooms present in Booking table)
        cursor.execute("SELECT COUNT(DISTINCT Room_no) FROM Booking")
        booked_rooms = cursor.fetchone()[0]

        # Available rooms
        available_rooms = total_rooms - booked_rooms

        # Room-wise details
        cursor.execute("""
            SELECT  r.Room_no, r.Room_type, r.price_per_night,
                   CASE WHEN b.Room_no IS NOT NULL THEN 'Booked' ELSE 'Available' END AS Status
            FROM Rooms r
            LEFT JOIN Booking b ON r.Room_no = b.Room_no
        """)
        rooms_details = cursor.fetchall()

        return render_template("report.html",
                               total_rooms=total_rooms,
                               booked_rooms=booked_rooms,
                               available_rooms=available_rooms,
                               rooms_details=rooms_details)
    except Exception as e:
        print("REPORT ERROR:", e)
        return f"Error generating report: {str(e)}"


# log out page:
@app.route("/logout")
def logout():
    return redirect(url_for("home"))





if __name__ == "__main__":
    app.run(debug=True)

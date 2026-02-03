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
        phone = request.form["phone"]
        newPassword = request.form["password"]

        sql = "UPDATE users SET password=%s WHERE phone=%s"
        cursor.execute(sql, (newPassword, phone))
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
    (CustomerName, FatherName, MotherName, Gender, RoomNo, Mobile, Email, Nationality, IdProof, IdNumber, Address)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    
    values = (
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
    try:
        cursor.execute("select * from customer_info")
        rows= cursor.fetchall()
        customer=[]
        for row in rows:
            customer.append({
                "referenceNo":row[0],
                "customerName":row[1],
                "FatherName":row[2],
                "MotherName":row[3],
                "Gender":row[4],
                "RoomNo":row[5],
                "Mobile":row[6],
                "Email":row[7],
                "Nationality":row[8],
                "IdProof":row[9],
                "IdNumber":row[10],
                "Address":row[11],
            })


        return jsonify(customer)

           
    except Exception as e:
       
        return jsonify({"error" : str(e)})
    


        
        
    
#staff page:

@app.route("/staff")
def staff():
    return render_template("staff.html")

@app.route("/add_staff",methods=["POST"])
def add_staff():
    data= request.json
    SQL=""" 
    INSERT INTO staff_info(Id,FirstName,Lastname, FatherName,MotherName, Role,Gender,Mobile,Email,Nationality,IdProof,IdNumber,Address)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

    """
    VALUES=(
        data["Id"],
        data["FirstName"],
        data["LastName"],
        data["FatherName"],
        data["MotherName"],
        data["Role"],
        data["Gender"],
        data["Mobile"],
        data["Email"],
        data["Nationality"],
        data["IdProof"],
        data["IdNumber"],
        data["Address"]
        
    )
    try:
        cursor.execute(SQL,VALUES)
        db.commit()
        return jsonify({"message":"staff added succcessfully"})
    except Exception as e:
        return jsonify({"message" : "error :"  + str(e)})



@app.route("/get_staff")
def get_staff():
    try:
        cursor.execute("SELECT * FROM   staff_info")
        rows=cursor.fetchall()
        staff=[]
        for s in rows:
            staff.append({
                "Id":s[0],
                "FirstName":s[1],
                "LastName":s[2],
                "FatherName":s[3],
                "MotherName":s[4],
                "Role":s[5],
                "Gender":s[6],
                "Mobile":s[7],
                "Email":s[7],
                "Nationality":s[8],
                "IdProof":s[9],
                "IdNumber":s[10],
                "Address":s[10]
            })

            
        return jsonify(staff)

           
    except Exception as e:
       
        return jsonify({"error" : str(e)})

# room page

@app.route("/roomss")
def rooms():
    cursor.execute("SELECT * FROM Rooms")
    rooms = cursor.fetchall()
    return render_template("roomss.html", rooms=rooms)


#booking page

@app.route("/booking")
def booking():
    return render_template("booking.html")

@app.route("/add_booking", methods=["POST"])
def add_booking():
    data=request.json

    SQL=""" INSERT INTO Booking (ReferenceNO, Room_no,check_in, check_out) 
    VALUES(%s,%s,%s,%s)
     """
    
    VALUES=(
        data["ReferenceNO"],
        data["Room_no"],
        data["check_in"],
        data["check_out"]
    )

    
    try:
        cursor.execute(SQL,VALUES)
        db.commit()
        return jsonify({"message":"Booking added successfully"})
    except Exception as e:
        return jsonify({"message" : "error :"  + str(e)})
    
@app.route("/get_booking")
def get_booking():

    try:
        cursor.execute("SELECT * from Booking")
        rows=cursor.fetchall()
        booking=[]
        for b in rows:
            booking.append({
                "BookingID":b[0],
                "ReferenceNO":b[1],
                "Room_no":b[2],
                "check_in": str(b[3]),
                "check_out":str(b[4])
            })

        return jsonify(booking)
              
    except Exception as e:
       
        return jsonify({"error" : str(e)})
    


@app.route("/billing")
def billing():
    return render_template("billing.html")


@app.route("/add_billing", methods=["POST"])
def add_billing():
    data = request.json

    sql = """
    INSERT INTO billing
    (booking_id, total_days, room_price, room_amount,
     tax_percent, tax_amount, extra_charges, discount, grand_total)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        data["booking_id"],
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
        return jsonify({"message": "error: " + str(e)}), 500

@app.route("/get_billing")

def get_billing():
    try:
        cursor.execute("SELECT * FROM billing")
        rows = cursor.fetchall()
        billing = []
        for b in rows:
            billing.append({
                "bill_id": b[0],
                "booking_id": b[1],
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

# report page:

@app.route("/report")
def report():
    return render_template("report.html")


# log out page:
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)

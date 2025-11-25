import os
from datetime import datetime, timedelta,timezone
import sqlite3
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
from flask_migrate import Migrate
import traceback

# ---------------------- CONFIGURATION ----------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'kkmcars.db')
SECRET_KEY = os.environ.get("SECRET_KEY", "change_this_secret_in_prod")
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DB_PATH
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

CORS(app, resources={r"/api/*": {"origins": "*"}})

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ---------------------- MODELS ----------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # NEW: Admin flag
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "username": self.username,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    brand = db.Column(db.String(100))
    year = db.Column(db.Integer)
    price = db.Column(db.Float)
    fuel_type = db.Column(db.String(50))
    transmission = db.Column(db.String(50))
    mileage = db.Column(db.String(50))
    location = db.Column(db.String(150))
    description = db.Column(db.Text)
    image1 = db.Column(db.String(300))
    image2 = db.Column(db.String(300))
    image3 = db.Column(db.String(300))
    image4 = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        images = []
        for img in [self.image1, self.image2, self.image3, self.image4]:
            if img:
                url = request.host_url.rstrip('/') + '/' + img.replace("\\", "/")
                images.append(url)
        return {
            "id": self.id,
            "name": self.name,
            "brand": self.brand,
            "year": self.year,
            "price": self.price,
            "fuel_type": self.fuel_type,
            "transmission": self.transmission,
            "mileage": self.mileage,
            "location": self.location,
            "description": self.description,
            "images": images,
            "image_url": images[0] if images else None,
        }

class SellRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    contact_number = db.Column(db.String(20))
    email = db.Column(db.String(150))
    car_brand = db.Column(db.String(100))
    car_model = db.Column(db.String(100))
    year = db.Column(db.Integer)
    price = db.Column(db.Float)
    mileage = db.Column(db.Float)
    fuel_type = db.Column(db.String(50))
    description = db.Column(db.Text)
    image = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        img_url = request.host_url.rstrip('/') + '/' + self.image.replace("\\", "/") if self.image else None
        return {
            "id": self.id,
            "user_name": self.user_name,
            "contact_number": self.contact_number,
            "email": self.email,
            "car_brand": self.car_brand,
            "car_model": self.car_model,
            "year": self.year,
            "price": self.price,
            "mileage": self.mileage,
            "fuel_type": self.fuel_type,
            "description": self.description,
            "image": img_url,
            "created_at": self.created_at.isoformat(),
        }

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "message": self.message,
            "created_at": self.created_at.isoformat(),
        }

# ---------- JWT Helpers ----------
def create_access_token(user_id, expires_minutes=60):
    now_utc = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),  # must be string
        "iat": now_utc,
        "exp": now_utc + timedelta(minutes=expires_minutes)
    }
    secret = app.config["SECRET_KEY"]
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token if isinstance(token, str) else token.decode("utf-8")


def decode_access_token(token):
    secret = app.config.get("SECRET_KEY")
    if not secret:
        raise RuntimeError("SECRET_KEY not set in app config")
    try:
        return jwt.decode(str(token), secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        print("Token expired")
        return None
    except jwt.InvalidTokenError as e:
        print("Token invalid:", e)
        return None


# ---------- Decorator ----------
def require_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"ok": False, "msg": "Missing token"}), 401
        token = auth.split(" ", 1)[1]
        payload = decode_access_token(token)
        if not payload:
            return jsonify({"ok": False, "msg": "Invalid or expired token"}), 401
        request.user_id = int(payload["sub"])  # convert back to int
        return func(*args, **kwargs)
    return wrapper

# NEW: Admin decorator
def require_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"ok": False, "msg": "Missing token"}), 401
        token = auth.split(" ", 1)[1]
        payload = decode_access_token(token)
        if not payload:
            return jsonify({"ok": False, "msg": "Invalid or expired token"}), 401
        
        user = User.query.get(int(payload["sub"]))
        if not user or not user.is_admin:
            return jsonify({"ok": False, "msg": "Admin access required"}), 403
        
        request.user_id = user.id
        return func(*args, **kwargs)
    return wrapper

# ---------------------- ROUTES ----------------------

@app.route("/api/ping")
def ping():
    return jsonify({"ok": True, "msg": "pong"})

# ---- ADMIN LOGIN (NEW) ----
@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    try:
        data = request.get_json() or {}
        username_or_email = (data.get("username") or data.get("email") or "").strip().lower()
        password = data.get("password", "")

        if not username_or_email or not password:
            return jsonify({"ok": False, "msg": "Username/email and password required"}), 400

        user = User.query.filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()

        print(f" Admin login attempt: {username_or_email}")
        
        if not user:
            print(" User not found")
            return jsonify({"ok": False, "msg": "Invalid credentials"}), 401
        
        if not check_password_hash(user.password_hash, password):
            print(" Invalid password")
            return jsonify({"ok": False, "msg": "Invalid credentials"}), 401
        
        if not user.is_admin:
            print(" User is not admin")
            return jsonify({"ok": False, "msg": "Admin access required"}), 403

        # Update last login
        user.last_login = datetime.now(timezone.utc)
        db.session.commit()

        token = create_access_token(user.id, expires_minutes=60*24)  # 24 hours
        
        print(f" Admin login successful: {user.username}")
        return jsonify({
            "ok": True, 
            "msg": "Login successful", 
            "user": user.to_dict(), 
            "token": token
        })
    
    except Exception as e:
        print(f" Admin login error: {str(e)}")
        traceback.print_exc()
        return jsonify({"ok": False, "msg": "Server error"}), 500

# ---- VERIFY ADMIN TOKEN (NEW) ----
@app.route("/api/admin/verify", methods=["GET"])
@require_admin
def verify_admin():
    user = User.query.get(request.user_id)
    return jsonify({"ok": True, "user": user.to_dict()})

# ---- CREATE ADMIN USER (NEW - For initial setup) ----
@app.route("/api/admin/create", methods=["POST"])
def create_admin():
    """
    Initial admin creation endpoint. 
    In production, you should secure or remove this after creating your admin user.
    """
    data = request.get_json() or {}
    username = (data.get("username") or "").strip().lower()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password", "")
    full_name = (data.get("full_name") or "").strip()

    if not username or not email or not password:
        return jsonify({"ok": False, "msg": "Username, email, and password are required"}), 400

    # Check if admin already exists
    existing_admin = User.query.filter_by(is_admin=True).first()
    if existing_admin:
        return jsonify({"ok": False, "msg": "Admin user already exists"}), 400

    # Check if username/email already exists
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"ok": False, "msg": "Username or email already exists"}), 400

    user = User(
        full_name=full_name,
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        is_admin=True
    )
    db.session.add(user)
    db.session.commit()

    print(f" Admin user created: {username}")
    return jsonify({"ok": True, "msg": "Admin user created successfully", "user": user.to_dict()}), 201

# ---- SIGNUP ----
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    full_name = (data.get("full_name") or "").strip()
    username = (data.get("username") or "").strip().lower()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password", "")

    if not username or not email or not password:
        return jsonify({"ok": False, "msg": "Username, email, and password are required"}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"ok": False, "msg": "Username or email already exists"}), 400

    user = User(
        full_name=full_name,
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        is_admin=False  # Regular users are not admin
    )
    db.session.add(user)
    db.session.commit()

    token = create_access_token(user.id, expires_minutes=60*24)  # 24h token
    return jsonify({"ok": True, "msg": "User created", "user": user.to_dict(), "token": token}), 201

# ---- LOGIN ----
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username_or_email = (data.get("username") or data.get("email") or "").strip().lower()
    password = data.get("password", "")

    if not username_or_email or not password:
        return jsonify({"ok": False, "msg": "Username/email and password required"}), 400

    user = User.query.filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()
    
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"ok": False, "msg": "Invalid credentials"}), 401

    # Only update last_login for this user
    user.last_login = datetime.now(timezone.utc)
    db.session.commit()

    token = create_access_token(user.id, expires_minutes=60*24)
    return jsonify({"ok": True, "msg": "Login successful", "user": user.to_dict(), "token": token})

# ---- GET CURRENT USER ----
@app.route("/api/me", methods=["GET"])
@require_token
def get_current_user():
    user = User.query.get(request.user_id)
    if not user:
        return jsonify({"ok": False, "msg": "User not found"}), 404
    return jsonify({"ok": True, "user": user.to_dict()})

# ---- USER ACTIVITY ----
@app.route("/api/user-activity", methods=["GET"])
def user_activity():
    threshold = datetime.utcnow() - timedelta(minutes=10)
    users = User.query.all()
    online_users = [u for u in users if u.last_login and u.last_login >= threshold]
    recent_signups = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_logins = User.query.order_by(User.last_login.desc()).limit(5).all()
    return jsonify({
        "ok": True,
        "total_users": len(users),
        "online_users": len(online_users),
        "recent_signups": [u.to_dict() for u in recent_signups],
        "recent_logins": [u.to_dict() for u in recent_logins]
    })

# ---- CAR MANAGEMENT (All your existing code remains unchanged) ----

@app.route("/api/add_car", methods=["POST"])
def add_car():
    try:
        print(" Adding new car...")
        form = request.form
        
        # Get car details
        name = form.get('name', '').strip()
        brand = form.get('brand', '').strip()
        year = form.get('year')
        price = form.get('price')
        fuel_type = form.get('fuel_type', '').strip()
        transmission = form.get('transmission', '').strip()
        mileage = form.get('mileage', '').strip()
        location = form.get('location', '').strip()
        description = form.get('description', '').strip()
        
        if not name:
            return jsonify({"ok": False, "msg": "Car name is required"}), 400
        
        print(f" Car details: {name}, {brand}, {year}, {price}")
        
        # Handle 4 separate image uploads
        image_paths = []
        
        for i in range(1, 5):
            image_key = f'image{i}'
            if image_key in request.files:
                file = request.files[image_key]
                if file and file.filename:
                    try:
                        filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}_{secure_filename(file.filename)}"
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(filepath)
                        rel_path = f"static/uploads/{filename}"
                        image_paths.append(rel_path)
                        print(f" {image_key} saved: {rel_path}")
                    except Exception as e:
                        print(f" Error saving {image_key}: {str(e)}")
                        image_paths.append(None)
                else:
                    image_paths.append(None)
            else:
                image_paths.append(None)
        
        # Ensure we have exactly 4 image slots
        while len(image_paths) < 4:
            image_paths.append(None)
        
        print(f" Total images: {len(image_paths)}", image_paths)
        
        # Create car object with all 4 images
        car = Car(
            name=name,
            brand=brand if brand else None,
            year=int(year) if year else None,
            price=float(price) if price else None,
            fuel_type=fuel_type if fuel_type else None,
            transmission=transmission if transmission else None,
            mileage=mileage if mileage else None,
            location=location if location else None,
            description=description if description else None,
            image1=image_paths[0],
            image2=image_paths[1],
            image3=image_paths[2],
            image4=image_paths[3],
        )
        
        db.session.add(car)
        db.session.commit()
        
        print(f" Car added successfully with ID: {car.id}")
        return jsonify({"ok": True, "msg": "Car added successfully", "car": car.to_dict()}), 201
        
    except Exception as e:
        traceback.print_exc()
        print(f" Error adding car: {str(e)}")
        db.session.rollback()
        return jsonify({"ok": False, "msg": f"Error adding car: {str(e)}"}), 500


@app.route('/api/cars', methods=['GET'])
def get_cars():
    try:
        print("Fetching all cars...")
        cars = Car.query.order_by(Car.created_at.desc()).all()
        result = [c.to_dict() for c in cars]
        print(f"Retrieved {len(result)} cars")
        return jsonify(result), 200
    except Exception as e:
        traceback.print_exc()
        print(f"Error fetching cars: {str(e)}")
        return jsonify({"ok": False, "msg": f"Error: {str(e)}"}), 500


@app.route("/api/cars/<int:car_id>", methods=["GET"])
def get_car_detail(car_id):
    try:
        print(f" Fetching car ID: {car_id}")
        car = Car.query.get(car_id)
        
        if not car:
            print(f"Car {car_id} not found")
            return jsonify({"ok": False, "msg": "Car not found"}), 404
        
        result = car.to_dict()
        print(f"Car {car_id} retrieved")
        print(f" Images: {result.get('images')}")
        return jsonify(result), 200
        
    except Exception as e:
        traceback.print_exc()
        print(f" Error fetching car: {str(e)}")
        return jsonify({"ok": False, "msg": f"Error: {str(e)}"}), 500

@app.route("/api/update_car/<int:car_id>", methods=["PUT"])
def update_car(car_id):
    try:
        print(f"Updating car {car_id}...")
        car = Car.query.get(car_id)
        
        if not car:
            print(f" Car {car_id} not found")
            return jsonify({"ok": False, "msg": "Car not found"}), 404
        
        form = request.form
        
        # Update basic fields
        if form.get('name'):
            car.name = form.get('name').strip()
        if form.get('brand'):
            car.brand = form.get('brand').strip()
        if form.get('year'):
            car.year = int(form.get('year'))
        if form.get('price'):
            car.price = float(form.get('price'))
        if form.get('fuel_type'):
            car.fuel_type = form.get('fuel_type').strip()
        if form.get('transmission'):
            car.transmission = form.get('transmission').strip()
        if form.get('mileage'):
            car.mileage = form.get('mileage').strip()
        if form.get('location'):
            car.location = form.get('location').strip()
        if form.get('description'):
            car.description = form.get('description').strip()
        
        # Handle image updates (replace if new image provided)
        for i in range(1, 5):
            image_key = f'image{i}'
            if image_key in request.files:
                file = request.files[image_key]
                if file and file.filename:
                    try:
                        # Delete old image if exists
                        old_image = getattr(car, image_key, None)
                        if old_image:
                            try:
                                full_path = os.path.join(BASE_DIR, old_image)
                                if os.path.exists(full_path):
                                    os.remove(full_path)
                                    print(f" Deleted old image: {old_image}")
                            except Exception as e:
                                print(f" Could not delete old image: {str(e)}")
                        
                        # Save new image
                        filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}_{secure_filename(file.filename)}"
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(filepath)
                        rel_path = f"static/uploads/{filename}"
                        setattr(car, image_key, rel_path)
                        print(f" {image_key} updated: {rel_path}")
                    except Exception as e:
                        print(f" Error updating {image_key}: {str(e)}")
        
        db.session.commit()
        print(f" Car {car_id} updated successfully")
        return jsonify({"ok": True, "msg": "Car updated successfully", "car": car.to_dict()}), 200
        
    except Exception as e:
        traceback.print_exc()
        print(f" Error updating car: {str(e)}")
        db.session.rollback()
        return jsonify({"ok": False, "msg": f"Error: {str(e)}"}), 500

@app.route("/api/delete_car/<int:car_id>", methods=["DELETE"])
def delete_car(car_id):
    try:
        print(f" Deleting car {car_id}...")
        car = Car.query.get(car_id)
        
        if not car:
            print(f" Car {car_id} not found")
            return jsonify({"ok": False, "msg": "Car not found"}), 404

        for img_field in [car.image1, car.image2, car.image3, car.image4]:
            if img_field:
                try:
                    full_path = os.path.join(BASE_DIR, img_field)
                    if os.path.exists(full_path):
                        os.remove(full_path)
                        print(f" Deleted image: {img_field}")
                except Exception as e:
                    print(f" Could not delete {img_field}: {str(e)}")

        db.session.delete(car)
        db.session.commit()
        print(f" Car {car_id} deleted successfully")
        return jsonify({"ok": True, "msg": "Car deleted"}), 200
        
    except Exception as e:
        traceback.print_exc()
        print(f" Error deleting car: {str(e)}")
        db.session.rollback()
        return jsonify({"ok": False, "msg": f"Error: {str(e)}"}), 500

@app.route("/api/messages", methods=["GET"])
def get_messages():
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return jsonify({"ok": True, "messages": [m.to_dict() for m in messages]})

@app.route("/api/sell_request", methods=["POST"])
def sell_request():
    try:
        name = request.form.get("name")
        contact = request.form.get("num")
        email = request.form.get("mail")
        car_brand = request.form.get("brand")
        car_model = request.form.get("model")
        year = request.form.get("year", type=int)
        price = request.form.get("price", type=float)
        mileage = request.form.get("mileage", type=float)
        fuel = request.form.get("fuel")
        description = request.form.get("desc")
        image_file = request.files.get("image")

        # Save uploaded image
        image_path = None
        if image_file and image_file.filename:
            filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}_{secure_filename(image_file.filename)}"
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image_file.save(file_path)
            image_path = f"static/uploads/{filename}"

        req = SellRequest(
            user_name=name,
            contact_number=contact,
            email=email,
            car_brand=car_brand,
            car_model=car_model,
            year=year,
            price=price,
            mileage=mileage,
            fuel_type=fuel,
            description=description,
            image=image_path,
        )

        db.session.add(req)
        db.session.commit()
        return jsonify({"ok": True, "msg": "Sell request submitted successfully"})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"ok": False, "msg": f"Error: {str(e)}"}), 500

@app.route("/api/delete_sell_request/<int:request_id>", methods=["DELETE"])
def delete_sell_request(request_id):
    try:
        print(f" Deleting sell request {request_id}...")
        sell_req = SellRequest.query.get(request_id)
        
        if not sell_req:
            print(f"Sell request {request_id} not found")
            return jsonify({"ok": False, "msg": "Sell request not found"}), 404
        
        # Delete image file if exists
        if sell_req.image:
            try:
                full_path = os.path.join(BASE_DIR, sell_req.image)
                if os.path.exists(full_path):
                    os.remove(full_path)
                    print(f" Deleted image: {sell_req.image}")
            except Exception as e:
                print(f" Could not delete image: {str(e)}")
        
        db.session.delete(sell_req)
        db.session.commit()
        print(f" Sell request {request_id} deleted successfully")
        return jsonify({"ok": True, "msg": "Sell request deleted"}), 200
        
    except Exception as e:
        traceback.print_exc()
        print(f" Error deleting sell request: {str(e)}")
        db.session.rollback()
        return jsonify({"ok": False, "msg": f"Error: {str(e)}"}), 500

# ---------------- Search Cars API ----------------
@app.route('/api/search_cars', methods=['GET'])
def search_cars():
    try:
        brand = request.args.get('brand', '').strip()
        model = request.args.get('model', '').strip()
        year = request.args.get('year', '').strip()
        price = request.args.get('price', '').strip()

        # Base query
        query = Car.query

        # Filter by brand
        if brand and brand != "All Brands":
            query = query.filter_by(brand=brand)

        # Filter by model/name
        if model and model != "Any Models":
            query = query.filter_by(name=model)

        # Filter by year
        if year and year != "All Years":
            try:
                year_int = int(year)
                query = query.filter_by(year=year_int)
            except ValueError:
                pass

        # Filter by price
        if price and price != "All Prices":
            try:
                price_float = float(price)
                query = query.filter(Car.price <= price_float)
            except ValueError:
                pass

        cars = query.order_by(Car.created_at.desc()).all()
        car_list = [c.to_dict() for c in cars]

        print(f" Search results: {len(car_list)} cars found")
        return jsonify({"ok": True, "cars": car_list}), 200

    except Exception as e:
        print(" Error in search_cars:", e)
        traceback.print_exc()
        return jsonify({"ok": False, "msg": "Server error"}), 500

# ---------- GET ALL SELL REQUESTS ----------
@app.route("/api/sell_requests", methods=["GET"])
def get_sell_requests():
    requests = SellRequest.query.order_by(SellRequest.created_at.desc()).all()
    return jsonify({"ok": True, "requests": [r.to_dict() for r in requests]})

@app.route("/api/send_message", methods=["POST"])
def send_message():
    data = request.get_json() or {}
    username = data.get("username")
    email = data.get("email")
    message_text = data.get("message")
    if not all([username, email, message_text]):
        return jsonify({"ok": False, "msg": "All fields required"}), 400
    msg = Message(username=username, email=email, message=message_text)
    db.session.add(msg)
    db.session.commit()
    return jsonify({"ok": True, "msg": "Message sent successfully"}), 201

# -------- CONTACT FORM MESSAGE --------
@app.route("/api/contact", methods=["POST"])
def contact_message():
    try:
        data = request.get_json() or {}
        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip()
        phone = (data.get("phone") or "").strip()
        message = (data.get("message") or "").strip()
        
        # Validation
        if not name or not email or not message:
            return jsonify({"ok": False, "msg": "Name, email, and message are required"}), 400
        
        # Create message record
        msg = Message(
            username=name,
            email=email,
            message=message
        )
        
        db.session.add(msg)
        db.session.commit()
        
        print(f" Contact message received from {name} ({email})")
        return jsonify({
            "ok": True, 
            "msg": "Message sent successfully! We'll contact you soon.",
            "data": {
                "name": name,
                "email": email,
                "phone": phone
            }
        }), 201
        
    except Exception as e:
        traceback.print_exc()
        print(f" Error in contact form: {str(e)}")
        db.session.rollback()
        return jsonify({"ok": False, "msg": f"Error: {str(e)}"}), 500

# -------- DELETE CONTACT MESSAGE --------
@app.route("/api/messages/<int:message_id>", methods=["DELETE"])
def delete_contact_message(message_id):
    try:
        print(f" Deleting contact message {message_id}...")
        msg = Message.query.get(message_id)
        
        if not msg:
            print(f" Message {message_id} not found")
            return jsonify({"ok": False, "msg": "Message not found"}), 404
        
        db.session.delete(msg)
        db.session.commit()
        print(f"Message {message_id} deleted successfully")
        return jsonify({"ok": True, "msg": "Message deleted"}), 200
        
    except Exception as e:
        traceback.print_exc()
        print(f" Error deleting message: {str(e)}")
        db.session.rollback()
        return jsonify({"ok": False, "msg": f"Error: {str(e)}"}), 500

# ---------------------- INIT ----------------------
def init_db():
    with app.app_context():
        try:
            db.create_all()
            print("[INIT]  DB created / verified")
            
            # Check if admin exists, if not create default admin
            admin = User.query.filter_by(is_admin=True).first()
            if not admin:
                print("[INIT] No admin user found. Creating default admin...")
                print("[INIT]  Username: admin | Password: admin")
                print("[INIT]   Please change the password after first login!")
                
                # ADMIN CREDENTIALS - Change these values if needed
                default_admin = User(
                    username="admin",
                    email="admin@kkmcars.com",
                    full_name="Administrator",
                    password_hash=generate_password_hash("admin"),
                    is_admin=True
                )
                db.session.add(default_admin)
                db.session.commit()
                print("[INIT] Default admin created successfully")
            else:
                print(f"[INIT]  Admin user exists: {admin.username}")
                
        except Exception as e:
            print("[INIT]   DB init warning:", e)

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    print("=" * 50)
    print(" KKMCars Server Starting...")
    print("=" * 50)
    app.run(host="0.0.0.0", port=port, debug=True)
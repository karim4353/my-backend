# from flask import Flask, request, jsonify

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return {"message": "Backend is running"}

# @app.route('/check_app', methods=['POST'])
# def check_app():
#     data = request.get_json()

#     # Extract information
#     kernel = data.get("kernel_version")
#     android_version = data.get("android_version")
#     sdk_version = data.get("sdk_version")
#     model = data.get("model")
#     manufacturer = data.get("manufacturer")
#     cpu_abi = data.get("cpu_abi")
#     build_fingerprint = data.get("build_fingerprint")
#     facebook_installed = data.get("facebook_installed")

#     # Log the data
#     print(f"Device Info Received:")
#     print(f"Kernel: {kernel}")
#     print(f"Android Version: {android_version} (SDK {sdk_version})")
#     print(f"Model: {model}")
#     print(f"Manufacturer: {manufacturer}")
#     print(f"CPU ABI: {cpu_abi}")
#     print(f"Build Fingerprint: {build_fingerprint}")
#     print(f"Facebook Installed: {facebook_installed}")

#     # Optional: store in database later

#     return jsonify({"status": "ok", "message": "Device info received"})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devices.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Device model
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kernel_version = db.Column(db.String(100))
    android_version = db.Column(db.String(50))
    sdk_version = db.Column(db.String(10))
    model = db.Column(db.String(100))
    manufacturer = db.Column(db.String(100))
    cpu_abi = db.Column(db.String(50))
    build_fingerprint = db.Column(db.String(200))
    facebook_installed = db.Column(db.Boolean)

# Create the database tables if not exist
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return {"message": "Hello from Flask on Render!"}
@app.route('/devices')
def list_devices():
    devices = Device.query.all()
    return jsonify([{
        "id": d.id,
        "model": d.model,
        "android_version": d.android_version,
        "facebook_installed": d.facebook_installed
    } for d in devices])


@app.route('/check_app', methods=['POST'])
def check_app():
    data = request.get_json()
    
    # Save to database
    device = Device(
        kernel_version=data.get("kernel_version"),
        android_version=data.get("android_version"),
        sdk_version=data.get("sdk_version"),
        model=data.get("model"),
        manufacturer=data.get("manufacturer"),
        cpu_abi=data.get("cpu_abi"),
        build_fingerprint=data.get("build_fingerprint"),
        facebook_installed=data.get("facebook_installed", False)
    )
    db.session.add(device)
    db.session.commit()
    
    # Print to console for debugging
    print("Device Info Received:")
    print(f"Kernel: {device.kernel_version}")
    print(f"Android Version: {device.android_version} (SDK {device.sdk_version})")
    print(f"Model: {device.model}")
    print(f"Manufacturer: {device.manufacturer}")
    print(f"CPU ABI: {device.cpu_abi}")
    print(f"Build Fingerprint: {device.build_fingerprint}")
    print(f"Facebook Installed: {device.facebook_installed}")

    return jsonify({"message": "Device info received", "status": "ok"})



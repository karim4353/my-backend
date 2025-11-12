from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return {"message": "Backend is running"}

@app.route('/check_app', methods=['POST'])
def check_app():
    data = request.get_json()

    # Extract information
    kernel = data.get("kernel_version")
    android_version = data.get("android_version")
    sdk_version = data.get("sdk_version")
    model = data.get("model")
    manufacturer = data.get("manufacturer")
    cpu_abi = data.get("cpu_abi")
    build_fingerprint = data.get("build_fingerprint")
    facebook_installed = data.get("facebook_installed")

    # Log the data
    print(f"Device Info Received:")
    print(f"Kernel: {kernel}")
    print(f"Android Version: {android_version} (SDK {sdk_version})")
    print(f"Model: {model}")
    print(f"Manufacturer: {manufacturer}")
    print(f"CPU ABI: {cpu_abi}")
    print(f"Build Fingerprint: {build_fingerprint}")
    print(f"Facebook Installed: {facebook_installed}")

    # Optional: store in database later

    return jsonify({"status": "ok", "message": "Device info received"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


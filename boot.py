import network


def load_wifi_config(env_path=".env"):
    """Load WiFi credentials from .env file"""
    wifi_config = {}
    try:
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    if key in ["WIFI_SSID", "WIFI_PASSWORD"]:
                        wifi_config[key] = value.strip('"').strip("'")

        if not all(k in wifi_config for k in ["WIFI_SSID", "WIFI_PASSWORD"]):
            raise ValueError("WIFI_SSID and WIFI_PASSWORD must be set in .env")

        return wifi_config["WIFI_SSID"], wifi_config["WIFI_PASSWORD"]
    except FileNotFoundError:
        raise RuntimeError(
            "WiFi credentials not found! Please create .env file."
        )


def connect_wifi(timeout=20):
    """Connect to WiFi network using credentials from config

    Args:
        timeout (int): Maximum time to wait for connection in seconds

    Returns:
        str: IP address if connected, None if failed
    """
    import time

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(dhcp_hostname="esp8266-irrigation")

    if not wlan.isconnected():
        print(f"Connecting to WiFi: {WIFI_SSID}...")
        try:
            wlan.connect(WIFI_SSID, WIFI_PASSWORD)
            start_time = time.time()

            while not wlan.isconnected():
                if time.time() - start_time > timeout:
                    print("WiFi connection timeout")
                    return None
                time.sleep(0.1)

        except Exception as e:
            print(f"WiFi connection failed: {e}")
            return None

    ip = wlan.ifconfig()[0]
    print(f"Connected to WiFi. IP: {ip}")
    return ip


# Load WiFi credentials from .env file
WIFI_SSID, WIFI_PASSWORD = load_wifi_config()

# Connect to WiFi on boot
IP_ADDRESS = connect_wifi()

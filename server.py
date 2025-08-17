import gc
from climate_sensor import AHT20
from machine import Pin, I2C
from lib.microdot import Microdot
from relay import Relay
from soil_sensor import SoilMoisture


app = Microdot()


@app.route("/")
async def index(request):
    gc.collect()
    return {"status": "ok"}, 200, {"Content-Type": "application/json"}


@app.route("/irrigate")
async def relay_on(request):
    """
    Route to turn the relay ON.
    """
    gc.collect()
    relay_instance = Relay(pin_number=14)
    relay_instance.on()
    del relay_instance
    gc.collect()
    return (
        {"status": "success", "message": "Irrigation started"},
        200,
        {"Content-Type": "application/json"},
    )


@app.route("/climate")
async def climate_route(request):
    """
    Route to get air temperature, humidity (from AHT20).
    """
    gc.collect()
    response_data = {"status": "success"}

    # Initialize I2C bus for sensors
    try:
        i2c_bus = I2C(sda=Pin(4), scl=Pin(5), freq=100000)
        print(f"I2C bus initialized. Devices found: {[hex(d) for d in i2c_bus.scan()]}")
    except Exception as e:
        print(f"Error initializing I2C bus: {e}. Sensor functionality may be limited.")
        i2c_bus = None  # Mark I2C as unavailable if it fails

    aht20_sensor = None

    if i2c_bus:
        try:
            aht20_sensor = AHT20(i2c_bus)
        except Exception as e:
            print(
                f"Could not initialize AHT20 sensor: {e}. AHT20 data will not be available."
            )
    else:
        print("I2C bus not available, skipping sensor initialization.")

    # Read from AHT20
    if aht20_sensor:
        temp_aht, hum_aht = aht20_sensor.read_values()
        if temp_aht is not None and hum_aht is not None:
            response_data["aht20_temperature_celsius"] = f"{temp_aht:.2f}"
            response_data["aht20_humidity_percent"] = f"{hum_aht:.2f}"
            response_data["aht20_status"] = "AHT20 functional"
        else:
            response_data["aht20_status"] = "Failed to read AHT20 data"
    else:
        response_data["aht20_status"] = "AHT20 sensor not initialized"

    del aht20_sensor
    del i2c_bus
    gc.collect()

    # Determine overall HTTP status
    if "aht20_status" not in response_data:
        http_status = 500  # Partial or full failure
    else:
        http_status = 200

    return response_data, http_status, {"Content-Type": "application/json"}


@app.route("/soil_moisture")
async def soil_moisture_route(request):
    gc.collect()
    response_data = {"status": "success"}
    http_status = 200

    # Handle Soil Moisture sensor
    soil_sensor = SoilMoisture()
    if soil_sensor and soil_sensor.ready:
        moisture_percent = soil_sensor.read_percent()
        if moisture_percent is not None:
            response_data["soil_moisture_p"] = f"{moisture_percent:.2f}"
            response_data["soil_moisture_raw"] = f"{soil_sensor.read_raw()}"
        else:
            response_data["soil_moisture_status"] = "Failed soil moisture read"
            http_status = 500
    else:
        response_data["soil_moisture_status"] = "Soil moisture sensor not available"
        http_status = 500

    del soil_sensor
    gc.collect()

    return response_data, http_status, {"Content-Type": "application/json"}


@app.errorhandler(404)
async def not_found(request):
    return (
        {"status": "error", "message": "404"},
        404,
        {"Content-Type": "application/json"},
    )

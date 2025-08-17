import gc
from server import app
import config


def main():
    gc.collect()
    if not IP_ADDRESS:
        print("Failed to connect to WiFi. Cannot start server.")
        return

    print(f"Server started at http://{IP_ADDRESS}")
    app.run(host=IP_ADDRESS, port=config.PORT, debug=False)


if __name__ == "__main__":
    main()

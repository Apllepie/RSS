import time
from monitoring import Monitoring
from sensor import Humidity, Temperature


def main():
    temp1 = Temperature("temp1")
    temp2 = Temperature("temp2")

    humi1 = Humidity("humi1")
    humi2 = Humidity("humi2")

    monitoring = Monitoring()

    try:
        while True:
            temp1.send("temp")
            temp2.send("temp")
            humi1.send("humidity")
            humi2.send("humidity")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nPublisher stopped.")

        temp1.disconnect()
        temp2.disconnect()
        humi1.disconnect()
        humi2.disconnect()
        monitoring.disconnect()


if __name__ == "__main__":
    main()
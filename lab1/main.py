
from monitoring_unit import monitoring
import time
from monitoring_unit.monitoring import monitoring
from sensors.temperature import temperature
from sensors.humidity import humidity




def main():
    temp1 = temperature("temp1")
    temp2 = temperature("temp2")

    humi1 = humidity("humi1")
    humi2 = humidity("humi2")

    monitoring = monitoring()
    try:
        while True:
            temp1.send("temp")
            temp2.send("temp")
            humi1.send("humidity")
            humi2.send("humidity")
            time.sleep(1)

    except KeyboardInterrupt:
        print("Publisher stopped.")

        temp1.disconect()
        humi1.disconect()
        temp2.disconect()
        humi2.disconect()
        monitoring.disconect()
        
    time.sleep(1)





if __name__ == "__main__" :
    main()
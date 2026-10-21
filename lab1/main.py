import multiprocessing
import time
from sensor import Humidity, Temperature


def worker(sensor_instance, topic: str, interval: float):
    sensor_instance.run(topic=topic, interval=interval)


def main():
    sensors = [
        (Temperature("temp1"), "sensors/temperature", 1.5),
        (Temperature("temp2"), "sensors/temperature", 2.0),
        (Humidity("humi1"), "sensors/humidity", 3.0),
        (Humidity("humi2"), "sensors/humidity", 2.5),
    ]

    processes = []

    for sensor_obj, topic, interval in sensors:
        p = multiprocessing.Process(
            target=worker,
            args=(sensor_obj, topic, interval),
            daemon=True
        )
        processes.append(p)
        p.start()

    print(f"[Main] Started {len(processes)} sensor processes. Press Ctrl+C to stop.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[Main] Stopping all sensor processes...")
        for p in processes:
            p.terminate()
            p.join()
        print("[Main] All processes terminated cleanly.")


if __name__ == "__main__":
    main()
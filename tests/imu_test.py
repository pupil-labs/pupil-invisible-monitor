import time

from pi_monitor.models import Host_Controller


HC = Host_Controller()
HC.poll_events()


def mydevice():
    yield from (h for h in HC.hosts() if "GM1913" in h.name)


print("Waiting for hosts")
while not any(mydevice()):
    time.sleep(0.5)
    HC.poll_events()

try:
    H = next(mydevice())
    HC.link(H)
    imu = H.sensors["imu"]
    print(imu)
    while True:
        print("Waiting for data")
        for header, content in imu.fetch_data():
            print(header, content)
        time.sleep(1.0)

finally:
    HC.cleanup()

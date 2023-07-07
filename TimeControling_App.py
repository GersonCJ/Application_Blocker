import wmi
from csv import writer, reader, DictWriter, DictReader
from ApplicationBlocker.Application_Blocker import constants
import timeit
import os

# Initializing the wmi constructor
app_file = 'applications.csv'
headers = ['App Name', 'Time']
c = wmi.WMI()
first_time_running = 1
recognition_flag = 0
counter_start = 0
counter_end = 0
counter_flag = 0
time = 0

# Re-initialize file

to_restart = open(app_file, mode='w')
first_write = DictWriter(to_restart, fieldnames=headers)
first_write.writeheader()
for app in constants.applications:
    first_write.writerow({'App Name': app, 'Time': time})
to_restart.close()

# Iterating through all the running processess

try:
    while True:
        for process in c.Win32_Process():
            # print(f"{process.ProcessId:<10} {process.Name}")
            if process.Name == "Discord.exe" and not recognition_flag:
                recognition_flag += 1
                if recognition_flag == 1 and not counter_flag:
                    counter_start = timeit.default_timer()
                    counter_flag += 1
            else:
                pass

        if not recognition_flag and counter_flag:
            counter_end = timeit.default_timer()
            to_read = open(app_file, mode='r')
            csv_reader = DictReader(to_read)
            for line in csv_reader:
                if len(line) > 0:
                    time = f"{float(line['Time']) + (counter_end - counter_start)}"
                else:
                    pass
            to_read.close()

            to_write = open(app_file, mode='w')
            csv_writer = DictWriter(to_write, fieldnames=headers)
            csv_writer.writeheader()
            csv_writer.writerow({'App Name': 'Discord.exe', 'Time': time})
            to_write.close()

        recognition_flag = 0

except KeyboardInterrupt:
    pass

from math import radians, cos, sin, asin, sqrt
import matplotlib.pyplot as plot
import datetime
from datetime import timedelta
import pandas as pd


class Data_Lookup:

    def __init__(self):
        self.data_table = {}
        self.list_of_csvs = ["person1.csv", "person2.csv", "person3.csv"]

    def distance(self,lat1, lat2, lon1, lon2):

        # The math module contains a function named
        # radians which converts from degrees to radians.
        lon1 = radians(lon1)
        lon2 = radians(lon2)
        lat1 = radians(lat1)
        lat2 = radians(lat2)

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

        c = 2 * asin(sqrt(a))

        # Radius of earth in kilometers. Use 3956 for miles
        r = 6371

        # calculate the result
        return (c * r)

    def wrangle_time(self, time, duration):
        year = int(time[0:4])
        month = int(time[4:6])
        day = int(time[6:8])
        hour = int(time[8:10])
        minute = int(time[10:12])
        duration = int(duration)
        time_delta = timedelta(milliseconds=duration)
        full_date = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=0)
        end_date = full_date + time_delta
        day_of_week = full_date.weekday()
        return year,month,day,hour,minute,duration,time_delta,full_date,end_date,day_of_week

    def location_attributes_update(self, user, location, day_of_week, hour, duration):
        if (hour < 6 or hour > 21):
            self.data_table[user][location][0] += duration/60000

        if (day_of_week == 5 or day_of_week == 6):
            self.data_table[user][location][1] += duration/60000

        elif (hour >= 9 and hour < 17 and day_of_week != 5 and day_of_week != 6):
            self.data_table[user][location][2] += duration/60000

        self.data_table[user][location][3] += 1

    def insert_locations(self, csv):
        user = csv[:-4]
        df = pd.read_csv(csv, sep=';')
        self.data_table[user] = {}
        for index, row in df.iterrows():
            unique = True
            latitude = row['latitude']
            longitude = row['longitude']
            proposed_lat, proposed_lon = latitude, longitude
            time = row['start_time(YYYYMMddHHmmZ)']
            duration = row['duration(ms)']
            year, month, day, hour, minute, duration, time_delta, full_date, end_date, day_of_week = self.wrangle_time(time,
                                                                                                                  duration)
            for key in self.data_table[user]:
                existing_lat, existing_lon = key[0], key[1]
                dist = self.distance(existing_lat, proposed_lat, existing_lon, proposed_lon)
                if (dist < 1.0):
                    unique = False
                    self.location_attributes_update(user, key, day_of_week, hour, duration)
                    break
            if (unique):
                self.data_table[user][(latitude, longitude)] = [0, 0, 0 , 0]
                location = (latitude, longitude)
                self.location_attributes_update(user, location, day_of_week, hour, duration)

    def fill_data_table(self):
        for file in self.list_of_csvs:
            self.insert_locations(file)

    def lookup(self,location,user):
        if location in self.data_table[user]:
            return True
        proposed_lat, proposed_lon = location[0], location[1]
        for key in self.data_table[user]:
            existing_lat, existing_lon = key[0], key[1]
            dist = self.distance(existing_lat, proposed_lat, existing_lon, proposed_lon)
            if (dist < 1.0):
                return True
        return False






lookup_table = Data_Lookup()
lookup_table.fill_data_table()
print(lookup_table.data_table["person2"])



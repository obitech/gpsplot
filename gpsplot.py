#!/usr/bin/python3
# Requires Python 3.6 (for f-string)

import sys
import datetime

def dms_to_dd(arg):
    """
    Input: string with DMS coordinates: <degrees> <minutes> <seconds> (e.g. 45 51 53.3)
    Out: string of DD coordinates: e.g. 32.123456
    """
    #split string
    temp = [float(x) for x in arg.split(" ")]

    # degrees + (minutes + seconds / 60) / 60
    return temp[0] + (temp[1] + temp[2] / 60) / 60

def diff_dist(lon1, lat1, lon2, lat2):
    """
    * This function was provided by TU Chemnitz staff as part of the exercise *
    Input: two points (lon1, lat1, lon2, lat2) as gps coordinates in DMS form
    Output: Rturns distance between two points (lat1, lon1, lon2, lat2)
    """

    from numpy import deg2rad
    from math import sin, cos, asin, sqrt

    lon1 = deg2rad(lon1)
    lat1 = deg2rad(lat1)
    lon2 = deg2rad(lon2)
    lat2 = deg2rad(lat2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = sin(dlat/2.0)**2 + cos(lat1) * cos(lat2) * sin(dlon/2.0)**2
    c = 2.0 * asin(min(1,sqrt(a)))
    d = 6396.0 * c

    return d

def diff_time(t1, t2):
    """
    * For now this only works with times on the same day (pre 24:00:00) *
    Input: two strings as time (HH:MM:SS)
    Output: string of time difference (HH:MM:SS)
    """

    fmt = "%H:%M:%S"
    out = str(datetime.datetime.strptime(t2, fmt) - datetime.datetime.strptime(t1, fmt))
   
    return out

def add_time(t0, t):
    """
    * For now this only works with times on the same day (pre 24:00:00) *
    Input: two strings as time (HH:MM:SS)
    Output: string with sum of times
    """

    fmt = "%H:%M:%S"

    t1 = datetime.datetime.strptime(t0, fmt)
    dt1 = datetime.timedelta(hours = t1.hour, minutes = t1.minute, seconds = t1.second)

    t2 = datetime.datetime.strptime(t, fmt)
    dt2 = datetime.timedelta(hours = t2.hour, minutes = t2.minute, seconds = t2.second)

    out = str(dt1 + dt2)

    return out

def format_time(t):
    """
    Use this if you really need to change 0:00:00 to 00:00:00 for some reason

    Input: string as time (H:MM:SS)
    Output: string as time (HH:MM:SS)
    """
    return ":".join(['0' + x if len(x) < 2 else x for x in t.split(":")])

def to_seconds(t):
    arr = t.split(":")

    h = int(arr[0]) * 3600
    m = int(arr[1]) * 60

    return h + m + int(arr[2])

def parse_log(fname):
    """
    Input: file name of gps file
    Output: [time(str), lat(dms/str), long(dms/str), height(int)]
    """

    try:
        arr = []
        with open(fname, "r") as file:
            for line in file:
                if line[0] != "!" and (not len(line) <= 1):
                    temp = [x for x in line.strip().split("\t")]
                    
                    # Removing date stamp
                    if "-" in temp[0]:
                        temp[0] = temp[0].split(" ")[1]

                    # Cast int on height
                    temp[3] = int(temp[3])

                    arr.append(temp)

        return arr

    except:
        print("Unable to work with file " + fname + ": " + str(sys.exc_info()[0]))

def format_arr(arr):
    """
    Converts an array of strings in a format for GNUplot

    Input: [time(str), lat(dms/str), long(dms/str), height(float)]
    Output: [iterator, section length, total length, time diff, total time, heigth, latitude(dms), longitude(dms)]
    """

    i = 0;
    sec_len, tot_len = 0.0, 0.0
    t_diff = '0:00:00'
    t_tot = t_diff[:]
    v = 0.0

    out = []

    for x in arr:
        lat = arr[i][1]
        lon = arr[i][2]
        h  = arr[i][3]

        if i > 0:
            sec_len = diff_dist(dms_to_dd(arr[i - 1][2]), dms_to_dd(arr[i - 1][1]), dms_to_dd(lon), dms_to_dd(lat))
            tot_len += sec_len

            t = arr[i][0]
            t_diff = diff_time(arr[i - 1][0], t)
            t_tot = add_time(t_tot, t_diff)

            v = (sec_len * 1000) / to_seconds(t_diff)

        string = f"{i}.\t{sec_len:.6f}\t{tot_len:.6f}\t{t_diff}\t{t_tot}\t{v:.6f}\t{h}\t{lat}\t{lon}"
        out.append(string)
        i += 1

    return out

def create_plot_file(arr, fname):
    """
    Saves an array to file

    Input: format_arr()-type array, file name
    """

    try:
        with open(fname, "w") as file:
            for line in arr:
                file.write(line + "\n")

    except:
        print("Unable to work with file " + fname + ": " + str(sys.exc_info()[0]))

if __name__ == "__main__":
    data = format_arr(parse_log("data.track"))
    create_plot_file(data, "gpsplot.gp")

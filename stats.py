#!/usr/bin/env python
import json
import datetime
import subprocess
import csv
import os
import argparse

def system_call(command):
    p = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    return p.stdout.read()

parser = argparse.ArgumentParser(description='creates statistics for the release file in the "results" dir')
parser.add_argument("-f", "--release-file", dest="file", help="path to release file", default="release_6.0.2.json")
parser.add_argument("-d", "--directory", dest="directory", help="results directory", default="results")

args = parser.parse_args()
release_file = args.file

#Create months list
months = []
#2017-2018
for year in range(2017, 2019):
        for month in range(1, 12):
            months.append(datetime.date.today().replace(year=year, month=month, day=1))
#2019:
for month in range (1,3):
    months.append(datetime.date.today().replace(year=2019, month=month, day=1))
#today:
months.append(datetime.date.today())

with open(release_file, "r") as data_file:
    data = json.load(data_file)

directory = args.directory
if not os.path.exists(directory):
    os.makedirs(directory)

for i in data:
    o = open(directory + "/" + i["name"] + ".csv", "w")
    print (i["name"])
    o.write('''Month,Commiters,Commits\n''')
    #clone
    if not os.path.exists(i["name"]):
        system_call("git clone --branch %s %s %s" % (i["branch"], i["source"], i["name"]))
    #gather stats
    for m in range(0, (len(months)-1)):
        o.write("%s - %s," % (months[m], months[m+1]))
        committers = system_call('cd %s && git shortlog --after="%s" --before="%s" -sn | wc -l | tr -d " |\n"' % (i["name"], months[m], months[m+1]))
        o.write("%s," % committers)
        commits = system_call('cd %s && git rev-list --count HEAD --after="%s" --before="%s"'% (i["name"], months[m], months[m+1]))
        o.write("%s" % commits)
    o.close()
    #cloc
    with open(directory + "/" + "%s_cloc.txt" % i["name"], "w") as c:
        cloc = system_call("cloc %s --quiet" % i["name"])
        c.write(cloc)


# for i in data["dependencies"]:
#     if "skip" not in i.keys():
#         print (i["name"])
#         o = open(directory + "/" + i["name"] + ".csv", "w")
#         o.write('''Month,Commiters,Commits\n''')
#         #clone
#         if not os.path.exists(i["name"]):
#             system_call("git clone --branch %s %s %s" % (i["branch"], i["source"], i["name"]))
#         #gather stats
#         for m in range(0, (len(months)-1)):
#             o.write("%s - %s," % (months[m], months[m+1]))
#             committers = system_call('cd %s && git shortlog --after="%s" --before="%s" -sn | wc -l | tr -d " |\n"' % (i["name"], months[m], months[m+1]))
#             o.write("%s," % committers)
#             commits = system_call('cd %s && git rev-list --count HEAD --after="%s" --before="%s"'% (i["name"], months[m], months[m+1]))
#             o.write("%s" % commits)
#         o.close()
#         #cloc
#         with open(directory + "/" + "%s_cloc.txt" % i["name"], "w") as c:
#             cloc = system_call("cloc %s --quiet" % i["name"])
#             c.write(cloc)

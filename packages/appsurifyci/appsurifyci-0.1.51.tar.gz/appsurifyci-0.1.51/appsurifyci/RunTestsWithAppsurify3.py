#!/usr/bin/env python3
# requires python>3.6
# Requires - pip install pyyaml
# Proxy issue - pip install urllib3==1.25.11

# upload - https://www.youtube.com/watch?v=zhpI6Yhz9_4&ab_channel=MakerBytes
# python setup.py sdist
# twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

# github actions - https://docs.github.com/en/actions/reference/workflow-commands-for-github-actions#setting-an-environment-variable
# https://stackoverflow.com/questions/66642705/why-requests-raise-this-exception-check-hostname-requires-server-hostname

from urllib.parse import quote
from junitparser import JUnitXml
import os
import sys
import subprocess
import shutil
import json
import requests
import re
import pathlib
from requests.auth import HTTPProxyAuth
import csv
import datetime
from shutil import copyfile
from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as ET
import time
from requests.adapters import HTTPAdapter, Retry
import socket
from urllib3.connection import HTTPConnection
import pathlib
from testbrain.contrib.report.mergers.junit import JUnitReportMerger
from testbrain.contrib.report.utils import xml_string_to_fileobject
import datetime as dt  

try:
    import yaml
except ImportError:
    print("Error, yaml is required, please run pip install pyyaml")

tests = ""
testsrun = ""
run_id = ""
proxy = ""
username = ""
password = ""
url = ""
apikey = ""
project = ""
testsuite = ""
report = ""
maxtests = 1000000  # default 10000000
fail = "newdefects, reopeneddefects"  # default new defects and reopened defects  #options newdefects, reopeneddefects, flakybrokentests, newflaky, reopenedflaky, failedtests, brokentests
additionalargs = ""  # default ''
testseparator = ""  # default ' '
postfixtest = ""  # default ''
prefixtest = ""  # default ''
fullnameseparator = ""  # default ''
fullname = "false"  # default false
failfast = "false"  # defult false
maxrerun = 3  # default 3
rerun = "false"  # default false
importtype = "junit"  # default junit
reporttype = "directory"  # default directory other option file, when directory needs to end with /
teststorun = "all"  # options include - high, medium, low, unassigned, ready, open, none
deletereports = "false"  # options true or false, BE CAREFUL THIS WILL DELETE THE SPECIFIC FILE OR ALL XML FILES IN THE DIRECTORY
startrunall = ""  # startrun needs to end with a space sometimes
endrunall = ""  # endrun needs to start with a space sometimes
startrunspecific = ""  # startrun needs to end with a space sometimes
endrunspecific = ""  # endrun needs to start with a space sometimes
commit = ""
scriptlocation = "./"
branch = ""
# runfrequency="single" #options single for single commits, lastrun for all commits since the last run, betweeninclusive or betweenexclusive for all commits between two commits either inclusive or exclusive
runfrequency = "multiple"  # options single for ['Single', 'LastRun', 'BetweenInclusive', 'BetweenExclusive']
fromcommit = ""
repository = "git"
scriptlocation = "./"
generatefile = "false"
template = "none"
addtestsuitename = "false"
addclassname = "false"
runtemplate = ""
testsuitesnameseparator = ""
testtemplate = ""
classnameseparator = ""
testseparatorend = ""
testtemplatearg1 = ""
testtemplatearg2 = ""
testtemplatearg3 = ""
testtemplatearg4 = ""
startrunpostfix = ""
endrunprefix = ""
endrunpostfix = ""
executetests = "true"
encodetests = "false"
escapetests = "false"
trainer = "false"
azure_variable = "appsurifytests"
pipeoutput = "false"
bitrise = "false"
recursive = "false"
executioncommand = ""
githubactionsvariable = ""
circlecivariable = ""
circlecivariablenobash = ""
printcommand = ""
testsuiteencoded = ""
projectencoded = ""
azurefilter = ""
azurefilteronall = "true"
replaceretry = "false"
webdriverio = "false"
percentage = ""
endspecificrun = ""
runnewtests = "false"
weekendrunall = "false"
daysrunall = ""
newdays = 14
azurevariablenum = 0
commandset = ""
alwaysrun = ""
alwaysrunset = []
azurealwaysrun = ""
azurealwaysrunset = []
upload = "true"
createfile = "false"
createpropertiesfile = "false"
spliton = "false"
nopush = "false"
repo_name = ""
screenplay = False
endcommand = ""
createfiles = ""
createfilesdirectory = ""
maxretrytime = 60
testsetnum = ""
numtestsets = ""
filenames = ""
printout = "false"
includefailing = "false"
convertcucumber = "false"
mergereports = "False"
mergefiles = "False"
fullreportdir = ""
azureTest = False
dll = ""
dlllocation = ""
vstestlocation = ""
#https://stackoverflow.com/questions/10048249/how-do-i-determine-if-current-time-is-within-a-specified-range-using-pythons-da
startTimeRunAll = ""

def isNowAfter(startTime): 
    nowTime = dt.datetime.now().time()
    #Over midnight: 
    return nowTime >= startTime 


def find(name):
    currentdir = (
        os.getcwd()
    )  # using current dir, could change this to work with full computer search
    for root, dirs, files in os.walk(currentdir):
        if name in files:
            return os.path.join(
                os.path.relpath(root, currentdir), name
            )  # for relative path
            # return os.path.join(root, name) # for full path - could also change the main search to search all folders


# inputs
# link to template used as the template
# will create copy of testsuite with all tests called temp.yaml
# list of tests with format testname,
# i.e. #teststorun = "path/testname,, path/testname"
def generate_opentest(teststocreate):
    # Copy xml file with all tests
    # Source path
    source = testtemplatearg2

    full_path = os.path.realpath(source)

    # Destination path
    destination = os.path.join(os.path.dirname(full_path), "temp.yaml")

    copyfile(source, destination)

    # remove tests not in test list
    teststorunopen = teststocreate
    testlist = teststorunopen.split(",,")
    data = ""

    with open(source) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    # data =
    tests = []
    k = 0
    teststring = ""
    for test in testlist:
        # if k != 0:
        #    teststring = teststring + ","
        head_tail = os.path.split(test)
        test_path = head_tail[0]
        test_name = head_tail[1]
        if test_path == "":
            test_path = "."
        # print("test_path = " + test_path)
        # print("test_name = " + test_name)
        testdic = {"name": test_name, "path": test_path}
        tests.append(testdic)

    # print(tests)
    testsdic = {"tests": tests}
    # print(testsdic)
    data.update(testsdic)
    # print(data)

    with open(destination, "w") as f:
        newdata = yaml.dump(data, f)


# Script to run Katalon tests with Appsurify


# inputs
# link to test suite with all tests
# will create copy of testsuite with all tests called temp.ts
# list of tests with format testname,
# i.e. #teststorun = "Test Cases/New Test Case 2, Test Cases/New Test Case"
def generate_katalon(teststocreate):
    # Copy xml file with all tests
    # Source path
    source = os.path.join(testtemplatearg2, testtemplatearg3)

    full_path = os.path.realpath(source)

    # Destination path
    destination = os.path.join(os.path.dirname(full_path), "temp.ts")

    print(destination)
    copyfile(source, destination)

    # remove tests not in test list
    teststorunkat = teststocreate
    testlist = teststorunkat.split(",,")

    tree = ElementTree()
    tree.parse(destination)

    root = tree.getroot()
    for test in root.findall("testCaseLink"):
        testids = test.findall("testCaseId")
        for testid in testids:
            print((testid.text))
            if testid.text not in testlist:
                root.remove(test)

    tree.write(destination)


# Function to run Sahi tests with Appsurify

# Will generate two files one called temp.dd.csv and anotehr called temp.suite.
# To run the tests execute testrunner.bat|.sh temp.dd.csv %additionalargs%

# inputs
# list of tests with format testsuitename#testname,
# i.e. #sahiteststorun = "ddcsv_dd_csv#test9.sah,ddcsv_dd_csv#test10.sah,sahi_demo_sah#sahi_demo.sah,demo_suite#getwin_popupWithParam.sah"

# Questions/TODO's
# should we get the first line comment?

# query to get which tests to run
# Can get - <testsuite name="ddcsv_dd_csv" tests="3" failures="3" errors="0" time="24.051">
# <testcase classname="ddcsv_dd_csv.test9" name="test9.sah" time="17.982">
# normal suite <?xml version="1.0" encoding="UTF-8"?><testsuite name="demo_suite" tests="138" failures="23" errors="0" time="2322.014">
# <testcase classname="demo_suite.204" name="204.sah" time="4.615"></testcase>
# single test
# <?xml version="1.0" encoding="UTF-8"?><testsuite name="sahi_demo_sah" tests="1" failures="0" errors="0" time="14.008">
# 	<testcase classname="sahi_demo_sah.sahi_demo" name="sahi_demo.sah" time="9.967"></testcase></testsuite>
# find file before the . in classname
# open that file and find the row with test9.sah
# copy that row to new file


def generate_sahi(teststocreate):
    sahiteststorun = teststocreate
    datarows = []
    sahitests = sahiteststorun.split(",,")
    print(sahitests)
    standalonetests = []
    suitetests = []
    datatests = []
    rows = []
    standalonerows = []

    if os.path.exists("temp.dd.csv"):
        os.remove("temp.dd.csv")
    if os.path.exists("temp.suite"):
        os.remove("temp.suite")

    for test in sahitests:
        testsuitename = test[0 : (test.find("#"))]
        testsuitename = testsuitename.replace("_", ".")
        testname = test[(test.find("#")) + 1 :]
        if testsuitename[-4:] == ".sah":
            standalonetests.append(testname)
        if testsuitename[-4:] == ".csv":
            datatests.append(test)
        if testsuitename[-6:] == ".suite":
            suitetests.append(test)

    print("printing standalone then data then suite")
    print(standalonetests)
    print(datatests)
    print(suitetests)
    print("printed sets")

    for test in suitetests:
        print(test)

        testsuitename = test[0 : (test.find("#"))]
        testsuitename = testsuitename.replace("_", ".")
        testname = test[(test.find("#")) + 1 :]
        print(testname)
        print(testsuitename)

        f = open(testsuitename, "r")
        fl = f.readlines()
        for line in fl:
            # print(line)
            if testname in line:
                values = line.split()
                for i, value in enumerate(values):
                    if testname in value:
                        values[i] = find(testname)

                print(values)
                row = " ".join(values)
                print(row)
                standalonerows.append(row)
                print(("Found {}".format(row)))

    print(standalonerows)

    f = open("temp.suite", "w+")
    for row in standalonerows:
        f.write(row + "\n")

    print(standalonetests)
    for test in standalonetests:
        f.write(find(test) + "\n")

    f.close()

    for test in datatests:
        print(test)
        testsuitename = test[0 : (test.find("#"))]
        testsuitename = testsuitename.replace("_", ".")
        testname = test[(test.find("#")) + 1 :]
        print(testname)
        print(testsuitename)

        with open(testsuitename, "r") as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                # print(row)
                if testname in row:
                    print(("Found: {}".format(row)))
                    for i, column in enumerate(row):
                        if testname in column:
                            row[i] = find(testname)
                    rows.append(row)

    with open("temp.dd.csv", "w") as outf:
        writer = csv.writer(outf)
        for row in rows:
            writer.writerow(row)
        tempsuite = ["temp.suite"]
        writer.writerow(tempsuite)


###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
# Main Script


def strip_non_ascii(string):
    """Returns the string without non ASCII characters"""
    stripped = (c for c in string if 0 < ord(c) < 127)
    return "".join(stripped)


def replace_non_ascii(string):
    """Returns the string without non ASCII characters"""
    newstring = ""
    addedAsciiSpace = False
    for c in string:
        if 0 < ord(c) < 127:
            if c == " ":
                if addedAsciiSpace == False:
                    newstring = newstring + c
            else:
                newstring = newstring + c
            addedAsciiSpace = False
        else:
            if newstring[-1] != " ":
                newstring = newstring + " "
                addedAsciiSpace = True
    return newstring


# created at 3/3 from below should be kept up to date.  Refactor to use the same method for both
# https://youtrack.jetbrains.com/issue/TW-70205
# potential option for long filters
def setVariables():
    if "azure" in testtemplate:
        max_length = 28000
        variable_num = 1
        # moved new test section to else statement as if we are running all tests then no need to check for new
        if len(testsrun) == 0 or testsrun == "all":
            print("no tests to set for azure")
            if azurefilteronall == "false":
                azurefilter = ""
            if azurefilter != "":
                # print (f'##vso[task.setvariable variable={azure_variable}{variable_num}]{azurefilter}{testsrun}')
                print(
                    f"##vso[task.setvariable variable={azure_variable}{variable_num}]{azurefilter}"
                )
                print(f"##vso[task.setvariable variable={azure_variable}]{azurefilter}")
            if azurefilter == "":
                # print (f'##vso[task.setvariable variable={azure_variable}{variable_num}]{testsrun}')
                print(f"##vso[task.setvariable variable={azure_variable}]")
                print(
                    f"##vso[task.setvariable variable={azure_variable}{variable_num}]"
                )
            # print (f'##vso[task.setvariable variable={azurefilter}{azure_variable}{variable_num}]{testsrun}')
        else:
            if runnewtests != "false" and runnewtests != "true":
                old_percentage = percentage
                percentage = "100"
                testset = get_tests(9)
                count = 0
                alltests = runcommand(runnewtests)
                i = 0
                newtestset = ""
                for line in alltests.splitlines():
                    line = line.strip()
                    if i != 0:
                        newtest = True
                        count = 0
                        for element in testset:
                            count = count + 1
                            testName = element["name"]
                            if testName == line:
                                newtest = False
                        if newtest == True:
                            testtoadd = line
                            if encodetests == "true":
                                testtoadd = testtoadd.encode("unicode_escape").decode()
                                testtoadd = testtoadd.replace("\\", "\\\\")
                                testtoadd = strip_non_ascii(testtoadd)
                                # testtoadd = testtoadd.replace("\\u00F6", "")
                                testtoadd = testtoadd.replace("\n", "\\n")
                                testtoadd = testtoadd.replace("(", "\(")
                                testtoadd = testtoadd.replace(")", "\)")
                                testtoadd = testtoadd.replace("&", "\&")
                                testtoadd = testtoadd.replace("|", "\|")
                                testtoadd = testtoadd.replace("=", "\=")
                                testtoadd = testtoadd.replace("!", "\!")
                                testtoadd = testtoadd.replace("~", "\~")
                            testsrun = (
                                testsrun
                                + testseparator
                                + prefixtest
                                + testtoadd
                                + postfixtest
                            )
                            newtestset = (
                                newtestset
                                + testseparator
                                + prefixtest
                                + testtoadd
                                + postfixtest
                            )
                    if line == "The following Tests are available:":
                        i = i + 1
                percentage = old_percentage
                execute_tests(newtestset, 11)
            print(
                f"##vso[task.setvariable variable={azure_variable}]{azurefilter}{testsrun}"
            )
            while len(testsrun) > max_length:
                stringtosplit = "|" + prefixtest
                split_string = testsrun.find(stringtosplit, max_length)
                setval = testsrun[:split_string]
                testsrun = testsrun[split_string:]
                print(
                    f"##vso[task.setvariable variable={azure_variable}{variable_num}]{azurefilter}{setval}"
                )
                variable_num = variable_num + 1
            print(
                f"##vso[task.setvariable variable={azure_variable}{variable_num}]{azurefilter}{testsrun}"
            )
    # print("##vso[task.setvariable variable=BuildVersion;]998")

    # print("Execution command = " + executioncommand)

    if executioncommand != "" and executioncommand is not None:
        # max_length = 28000
        # variable_num = 1
        # while len(testsrun) > max_length:
        #    split_string = testsrun.find("|Name=",max_length)
        #    setval = testsrun[:split_string]
        #    testsrun = testsrun[split_string:]
        #    print (f'##vso[task.setvariable variable={azure_variable}{variable_num}]{setval}')
        #    variable_num = variable_num + 1
        # print (f'##vso[task.setvariable variable={azure_variable}{variable_num}]{testsrun}')
        executioncommand = executioncommand.replace("[[teststorun]]", testsrun)
        print("Execution command is " + executioncommand)
        runcommand(executioncommand, True)

    if printcommand != "" and printcommand is not None:
        # max_length = 28000
        # variable_num = 1
        # while len(testsrun) > max_length:
        #    split_string = testsrun.find("|Name=",max_length)
        #    setval = testsrun[:split_string]
        #    testsrun = testsrun[split_string:]
        #    print (f'##vso[task.setvariable variable={azure_variable}{variable_num}]{setval}')
        #    variable_num = variable_num + 1
        # print (f'##vso[task.setvariable variable={azure_variable}{variable_num}]{testsrun}')
        printcommand = printcommand.replace("[[teststorun]]", testsrun)
        print(printcommand)

    # if githubactionsvariable != "" and githubactionsvariable is not None:
    #    executioncommand = "echo \"\{githubactionsvariable\}={[[teststorun]]}\" >> $GITHUB_ENV"

    if bitrise == "true":
        print(f'envman add --key TESTS_TO_RUN --value "{testsrun}"')
    # envman add --key MY_RELEASE_NOTE --value "This is the release note"
    if failfast == "false" and rerun == "true" and teststorun != "none":
        rerun_tests()


def urlencode(name):
    return quote(name, safe="")


def echo(stringtoprint):
    print(stringtoprint)


def runcommand(command, stream="false"):
    print("Running command " + command)
    print("platform = " + sys.platform)
    try:
        if stream == "true":
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                encoding="utf-8",
            )
            output = ""
            while True:
                # returns None while subprocess is running
                retcode = process.poll()
                line = process.stdout.readline()
                output = output + line
                print(line, end="")
                # yield line
                if retcode is not None:
                    break
            return output
        if stream == "false":
            result = subprocess.run(command, shell=True, capture_output=True)
            # subprocess.run(['ls', '-l'])stdout=subprocess.PIPE,
            print((result.stdout.decode("utf-8")))
            print((result.stderr.decode("utf-8")))
            return result.stdout.decode("utf-8")
    except Exception as ex:
        print(ex)


def delete_reports():
    try:
        if reporttype == "directory":
            folder = report
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(("Failed to delete %s. Reason: %s" % (file_path, e)))
        if reporttype == "file":
            os.remove(report)
    except Exception as exp:
        print(("Failed to delete. Reason: %s" % (exp)))


def execute_tests(testlist, testset):
    if executetests == "false":
        return
    if deletereports == "true":
        delete_reports()
    command = ""

    # endrunpostfix
    if generatefile == "false":
        if testset == 0:
            command = (
                startrunall
                + startrunpostfix
                + testlist
                + endrunprefix
                + endrunall
                + endrunpostfix
            )
        else:
            command = (
                startrunspecific
                + startrunpostfix
                + testlist
                + endrunprefix
                + endrunspecific
                + endrunpostfix
            )

    if generatefile == "sahi":
        generate_sahi(testlist)
        if testset == 0:
            command = (
                startrunall + startrunpostfix + endrunprefix + endrunall + endrunpostfix
            )
        else:
            command = (
                startrunspecific
                + startrunpostfix
                + endrunprefix
                + endrunspecific
                + endrunpostfix
            )

    if generatefile == "katalon":
        generate_katalon(testlist)
        if testset == 0:
            command = (
                startrunall + startrunpostfix + endrunprefix + endrunall + endrunpostfix
            )
        else:
            command = (
                startrunspecific
                + startrunpostfix
                + endrunprefix
                + endrunspecific
                + endrunpostfix
            )

    if generatefile == "opentest":
        generate_opentest(testlist)
        if testset == 0:
            command = (
                startrunall + startrunpostfix + endrunprefix + endrunall + endrunpostfix
            )
        else:
            command = (
                startrunspecific
                + startrunpostfix
                + endrunprefix
                + endrunspecific
                + endrunpostfix
            )

    # echo("run command = " + command)
    runcommand(command, pipeoutput)
    echo(os.getcwd())
    if nopush == "false":
        push_results()


def get_always_tests_azure():
    count = 0
    tests = ""
    for testName in azurealwaysrunset:
        count = count + 1
        if encodetests == "true":
            testName = testName.encode("unicode_escape").decode()
            testName = testName.replace("\\", "\\\\")
            testName = strip_non_ascii(testName)
            # testtoadd = testtoadd.replace("\\u00F6", "")
            testName = testName.replace("\n", "\\n")
            testName = testName.replace("(", "\(")
            testName = testName.replace(")", "\)")
            testName = testName.replace("&", "\&")
            testName = testName.replace("|", "\|")
            testName = testName.replace("=", "\=")
            testName = testName.replace("!", "\!")
            testName = testName.replace("~", "\~")
        tests = tests + testseparator + prefixtest + testName + postfixtest
    return tests


def get_tests(testpriority, retryGetTests=True):
    origtestpriority = testpriority
    # echo("getting test set " + str(testpriority))
    tests = ""
    valuetests = ""
    finalTestNames = ""
    # echo("runfrequency = " + runfrequency)
    # echo("apikey = " + apikey)
    # echo("importtype = " + importtype)
    # echo("commit = "+ commit)
    # echo("projectencoded = "+ projectencoded)
    # echo("testsuiteencoded = "+ testsuiteencoded)
    # echo("testpriority = "+ str(testpriority))
    # echo("addclassname = "+ addclassname)
    # echo("addtestsuitename = "+ addtestsuitename)
    # echo("testsuitesnameseparator = "+ testsuitesnameseparator)
    # echo("classnameseparator = "+ classnameseparator)
    # echo("repository = "+ repository)
    # echo("url = "+ url)
    # echo("branch = "+ branch)

    # apiendpoint=f"{url}/api/external/prioritized-tests/?project_name={projectencoded}&priority={testpriority}&testsuitename_separator={testsuitesnameseparator}&testsuitename={addtestsuitename}&classname={addclassname}&classname_separator={classnameseparator}&test_suite_name={testsuiteencoded}&first_commit={commit}"
    # headers={'token': apikey}
    headers = {
        "token": apikey,
    }

    params = {
        "name_type": importtype,
        "commit": commit,
        "project_name": projectencoded,
        "test_suite_name": testsuiteencoded,
        "priority": testpriority,
        "classname": addclassname,
        "testsuitename": addtestsuitename,
        "testsuitename_separator": testsuitesnameseparator,
        "classname_separator": classnameseparator,
        "repo": repository,
    }

    if runfrequency == "single":
        params["commit_type"] = "Single"
        params["target_branch"] = branch
    if runfrequency == "multiple":
        params["commit_type"] = "LastRun"
        params["target_branch"] = branch
    if runfrequency == "betweenexclusive":
        params["commit_type"] = "BetweenExclisuve"
        params["target_branch"] = branch
        params["from_commit"] = fromcommit
    if runfrequency == "betweeninclusive":
        params["commit_type"] = "BetweenInclusive"
        params["target_branch"] = branch
        params["from_commit"] = fromcommit

    if includefailing == "true":
        params["include_failing"] = "True"

    if percentage.isnumeric() and testpriority != 11 and testpriority != 10:
        params["percent"] = percentage

    if testpriority == 11:
        params["day"] = newdays

    if repo_name != "":
        params["repo_name"] = repo_name

    if filenames == "True":
        params["filename"] = "True"
        params["filename_separator"] = "#"

    print(params)
    api_url = url + "/api/external/prioritized-tests/"

    # s = requests.Session()

    # retries = Retry(total=3,
    #                backoff_factor=5,
    #                status_forcelist=[ 400, 500, 502, 503, 504 ])

    # s.mount(url, HTTPAdapter(max_retries=retries))
    retryCount = 6
    # HTTPConnection.default_socket_options = (
    #    HTTPConnection.default_socket_options + [
    #        (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),
    #        (socket.SOL_TCP, socket.TCP_KEEPIDLE, 45),
    #        (socket.SOL_TCP, socket.TCP_KEEPINTVL, 10),
    #        (socket.SOL_TCP, socket.TCP_KEEPCNT, 6)
    #    ]
    # )
    response_returned = True
    if proxy == "":
        try:
            # response = s.get(url + "/api/external/prioritized-tests/", headers=headers, params=params, timeout=600)
            try:
                response = requests.get(
                    url + "/api/external/prioritized-tests/",
                    headers=headers,
                    params=params,
                    timeout=600,
                )
                response_returned = True
            except:
                response_returned = False
            for x in range(retryCount):
                timetowait = (
                    maxretrytime * 1.5 / retryCount
                    + maxretrytime * 1.5 / retryCount * x
                )
                if response_returned:
                    if response.status_code == 200:
                        break
                print("Processing commits")
                time.sleep(timetowait)
                try:
                    response = requests.get(
                        url + "/api/external/prioritized-tests/",
                        headers=headers,
                        params=params,
                        timeout=600,
                    )
                    response_returned = True
                except:
                    response_returned = False
        except Exception as e:
            print(e)

    else:
        try:
            httpproxy = "http://" + proxy
            httpsproxy = "https://" + proxy
            proxies = {"http": httpproxy, "https": httpsproxy}
            if username == "":
                # response = s.get(url + "/api/external/prioritized-tests/", headers=headers,params=params,proxies=proxies,timeout=600)
                response = requests.get(
                    url + "/api/external/prioritized-tests/",
                    headers=headers,
                    params=params,
                    proxies=proxies,
                    timeout=600,
                )
                for x in range(retryCount):
                    timetowait = (
                        maxretrytime / retryCount + maxretrytime / retryCount * x
                    )
                    if response.status_code == 200:
                        break
                    time.sleep(timetowait)
                    response = requests.get(
                        url + "/api/external/prioritized-tests/",
                        headers=headers,
                        params=params,
                        proxies=proxies,
                        timeout=600,
                    )
            else:
                auth = HTTPProxyAuth(username, password)
                # response = s.get(url + "/api/external/prioritized-tests/",headers=headers,params=params,proxies=proxies,auth=auth,timeout=600)
                response = requests.get(
                    url + "/api/external/prioritized-tests/",
                    headers=headers,
                    params=params,
                    proxies=proxies,
                    auth=auth,
                    timeout=600,
                )
                for x in range(retryCount):
                    timetowait = (
                        maxretrytime / retryCount + maxretrytime / retryCount * x
                    )
                    if response.status_code == 200:
                        break
                    time.sleep(timetowait)
                    response = requests.get(
                        url + "/api/external/prioritized-tests/",
                        headers=headers,
                        params=params,
                        proxies=proxies,
                        auth=auth,
                        timeout=600,
                    )
        except:
            httpproxy = proxy
            httpsproxy = proxy
            proxies = {"http": httpproxy, "https": httpsproxy}
            if username == "":
                # response = s.get(url + "/api/external/prioritized-tests/",headers=headers,params=params,proxies=proxies,timeout=600)
                response = requests.get(
                    url + "/api/external/prioritized-tests/",
                    headers=headers,
                    params=params,
                    proxies=proxies,
                    timeout=600,
                )
                for x in range(retryCount):
                    timetowait = (
                        maxretrytime / retryCount + maxretrytime / retryCount * x
                    )
                    if response.status_code == 200:
                        break
                    time.sleep(timetowait)
                    response = requests.get(
                        url + "/api/external/prioritized-tests/",
                        headers=headers,
                        params=params,
                        proxies=proxies,
                        timeout=600,
                    )
            else:
                auth = HTTPProxyAuth(username, password)
                # response = s.get(url + "/api/external/prioritized-tests/",headers=headers,params=params,proxies=proxies,auth=auth,timeout=600)
                response = requests.get(
                    url + "/api/external/prioritized-tests/",
                    headers=headers,
                    params=params,
                    proxies=proxies,
                    auth=auth,
                    timeout=600,
                )
                for x in range(retryCount):
                    timetowait = (
                        maxretrytime / retryCount + maxretrytime / retryCount * x
                    )
                    if response.status_code == 200:
                        break
                    time.sleep(timetowait)
                    response = requests.get(
                        url + "/api/external/prioritized-tests/",
                        headers=headers,
                        params=params,
                        proxies=proxies,
                        auth=auth,
                        timeout=600,
                    )
    print("request sent to get tests")
    print((response.status_code))

    if response.status_code >= 500:
        print(
            (
                "[!] [{0}] Server Error {1}".format(
                    response.status_code, response.content.decode("utf-8")
                )
            )
        )
        return None
    elif response.status_code == 404:
        print(("[!] [{0}] URL not found: [{1}]".format(response.status_code, api_url)))
        return None
    elif response.status_code == 401:
        print(("[!] [{0}] Authentication Failed".format(response.status_code)))
        return None
    elif response.status_code == 400:
        print(
            (
                "[!] [{0}] Bad Request: Content: {1}".format(
                    response.status_code, response.content
                )
            )
        )
        return None
    elif response.status_code >= 300:
        print(("[!] [{0}] Unexpected Redirect".format(response.status_code)))
        return None
    elif response.status_code == 200:
        testset = json.loads(response.content.decode("utf-8"))
        return testset
    else:
        print(
            (
                "[?] Unexpected Error: [HTTP {0}]: Content: {1}".format(
                    response.status_code, response.content
                )
            )
        )

    # if retryGetTests == True:
    #    if response.status_code != 200:
    #        print("retrying getting prioritized tests")
    #        get_tests(origtestpriority, retryGetTests=False)

    return None


def get_and_run_tests(type):
    global maxtests, vstestlocation, dll, dlllocation
    count = 0
    tests = ""
    testset = ""
    try:
        oldmaxtests = maxtests
    except Exception as e:
        print(e)
    runcount = 1
    numplusone = 0
    try:
        testset = get_tests(type)
        count = 0
        tests = ""
        # print(maxtests)
        # print("max tests")
        # print(type(maxtests))
        # print("type")
        testrunset = []
        for element in testset:
            testName = element["name"]
            testrunset.append(testName)
        if type == 9:
            testrunset = list(set(testrunset + alwaysrunset))
        if createfiles.isnumeric():
            numoftests = len(testrunset)
            maxtests = numoftests // int(createfiles) + (
                numoftests % int(createfiles) > 0
            )
            maxtests = numoftests // int(createfiles)
            numplusone = numoftests % int(createfiles)
            # this below might not be a good idea :/
            if maxtests > oldmaxtests:
                maxtests = oldmaxtests
                numplusone = 0
        # if testtemplate == "mvn":
        #    testrunset = sorted(testrunset)
        # if screenplay and project == "Campspot":
        #    print("Setting screenplay")
        #    count = 1
        #    tests = "e2e.tests.EditWorkflowTest#datesChange"
        addedtests = []
        for testName in testrunset:
            count = count + 1
            if testtemplate == "cypress circleci":
                circlecisplitstring = '"'
                if testName.endswith(circlecisplitstring):
                    testName = testName[0 : -len(circlecisplitstring)]
                if circlecisplitstring in testName:
                    testName = testName.split(circlecisplitstring)[-1]

                circlecisplitstring = "&quot;"
                if testName.endswith(circlecisplitstring):
                    testName = testName[0 : -len(circlecisplitstring)]
                if circlecisplitstring in testName:
                    testName = testName.split(circlecisplitstring)[-1]

                testName = testName.strip()

            if testtemplate == "cypress update":
                suitename = testName.split(";")[0]
                testName = testName.replace(suitename, "")
                testName = testName.replace(";", "", 1)
                testName = testName.strip()
                if "(example #" in testName:
                    testName = testName.split("(example #")[0]
                    testName = testName.strip()

            if testtemplate == "cypress inquirer":
                suitename = testName.split(";")[0]
                testName = testName.replace(suitename, "")
                testName = testName.replace(";", "", 1)
                testName = testName.strip()
                if "(example #" in testName:
                    testName = testName.split("(example #")[0]
                    testName = testName.strip()
                if "C" in testName:
                    testName = "C" + testName.split("C")[1]
                    newTestName = testName[0:7].strip()
                    testName = newTestName
                else:
                    testName = ""
                    # to do fix this

                if testName in addedtests:
                    testName = ""

            if testtemplate == "cypress update no env":
                suitename = testName.split(";")[0]
                testName = testName.replace(suitename, "")
                testName = testName.replace(";", "", 1)
                testName = testName.strip()
                if "(example #" in testName:
                    testName = testName.split("(example #")[0]
                    testName = testName.strip()

            if "cypress" in testtemplate:
                testName = max(testName.split(","), key=len).strip()

            if escapetests == "true":
                testName = testName.replace('"', '\\"')

            if encodetests == "true":
                testName = testName.encode("unicode_escape").decode()
                testName = testName.replace("\\", "\\\\")
                testName = strip_non_ascii(testName)
                # testtoadd = testtoadd.replace("\\u00F6", "")
                testName = testName.replace("\n", "\\n")
                testName = testName.replace("(", "\(")
                testName = testName.replace(")", "\)")
                testName = testName.replace("&", "\&")
                testName = testName.replace("|", "\|")
                testName = testName.replace("=", "\=")
                testName = testName.replace("!", "\!")
                testName = testName.replace("~", "\~")
            if screenplay:
                testName = testName.split("(Actor)")[0]
            if spliton != "false" and spliton != "":
                testName = testName.split(spliton)[0]
            if filenames == "True":
                try:
                    if "#" in testName:
                        testName = testName.split("#")[0]
                        if testName in tests:
                            testName = ""
                        if "." not in testName:
                            testName = ""
                    else:
                        testName = ""
                except:
                    testName = ""
            if count == 1:
                if testName != "":
                    tests = prefixtest + testName + postfixtest
                    addedtests.append(testName)
                else:
                    count = 0
            else:
                # if testtemplate == "mvn":
                # if tests.split(testseparator)[-1].split(testsuitesnameseparator)[0] == testName.split(testsuitesnameseparator)[0]:
                # tests = tests + "+" + testName.split(testsuitesnameseparator)[1]
                # else:
                # tests = tests + testseparator + prefixtest + testName + postfixtest
                if testName != "":
                    tests = tests + testseparator + prefixtest + testName + postfixtest
                    addedtests.append(testName)
            maxtofind = maxtests
            if runcount <= numplusone:
                maxtofind = maxtofind + 1
            if count == maxtofind:
                # print("reached max tests")
                if createfiles.isnumeric():
                    filetosave = "appsurifytests" + str(runcount) + ".txt"
                    # filedirectories doesn't work yet
                    if createfilesdirectory != "":
                        # use this so it is relative?
                        # pathtocreate = os.path.join(getcwd(),createfilesdirectory)
                        os.makedirs(
                            os.path.dirname(createfilesdirectory), exist_ok=True
                        )
                        filetosave = os.path.join(createfilesdirectory, filetosave)
                    f = open(filetosave, "w+")
                    f.write(tests)
                    f.close()
                execute_tests(tests, type)
                count = 0
                tests = ""
                # print("restarting test count")
                failfast_tests()
                runcount = runcount + 1
        #####shouuld change this to add to test set at the start and be part of the standard loop
        if azureTest:
            try:
                os.chdir(dlllocation)
                # vstestlocation = "c:\\test\\this"
                print("vs test location = ")
                print(vstestlocation)
                if vstestlocation.endswith('"'):
                    vstestlocation = vstestlocation[:-1]
                if vstestlocation.endswith("vstest.console.exe"):
                    vstestlocation = vstestlocation.split("vstest.console.exe")[0]
                if not vstestlocation.endswith("\\"):
                    if vstestlocation != "":
                        vstestlocation = vstestlocation + "\\"
                vstestlocation = '"' + vstestlocation + 'vstest.console"'
                if vstestlocation == '"vstest.console"':
                    vstestlocation = "vstest.console"
                #vstestlocation = "\"" + vstestlocation + "\""
                commandToRun = (
                    vstestlocation
                    + " "
                    + dll
                    + " /ListFullyQualifiedTests /ListTestsTargetPath:testlist.txt"
                )
                runcommand(commandToRun)
                old_tests = get_tests_file()
                call_upload()
                if old_tests != '{"message":"No file found"}':
                    print("No old tests")
                    new_tests = compare_file_to_string("testlist.txt", old_tests)
                    print("Checking for new tests")
                    for testName in new_tests:
                        print(testName)
                        tests = (
                            tests + testseparator + prefixtest + testName + postfixtest
                        )
                        addedtests.append(testName)
            except Exception as error:
                # handle the exception
                print(
                    "No tests to add", error
                )  # An exception occurred: division by zero
        if createfiles.isnumeric():
            if count != 0:
                filetosave = "appsurifytests" + str(runcount) + ".txt"
                if createfilesdirectory != "":
                    os.makedirs(os.path.dirname(createfilesdirectory), exist_ok=True)
                    filetosave = os.path.join(createfilesdirectory, filetosave)
                f = open(filetosave, "w+")
                f.write(tests)
                f.close()
    except Exception as e:
        print("No tests to run")

    if tests != "":
        execute_tests(tests, type)
        failfast_tests()

    if createfiles.isnumeric():
        maxtests = oldmaxtests

    return tests

    # doesn't work as it will run on high, medium and low then if there are none for any it will run all
    # if type != 5 and tests == "":
    #        print("executing all tests")
    #        execute_tests("", 0)


def get_tests_file(retryImport=True):
    payload = {
        "project_name": project,
        "testsuite_name": testsuite,
    }

    headers = {
        "Token": apikey,
    }
    apiurl = url + "/fileimport/download"

    print(headers)
    print(payload)
    print(apiurl)
    print("=======================================")

    retryCount = 3
    timetowait = (maxretrytime / 2) / retryCount

    if proxy == "":
        response = requests.get(
            apiurl,
            headers=headers,
            params=payload,
            timeout=600,
        )

        for x in range(retryCount):
            if response.status_code == 200 or response.status_code == 201:
                break
            print(("Status code : [{0}] Retrying".format(response.status_code)))
            time.sleep(timetowait)
            # files = {
            #     "file": open(filepath, "rb"),
            # }
            response = requests.get(
                apiurl,
                headers=headers,
                params=payload,
                timeout=600,
            )
    else:
        try:
            httpproxy = "http://" + proxy
            httpsproxy = "https://" + proxy
            proxies = {"http": httpproxy, "https": httpsproxy}
            if username == "":
                # files = {
                #    "file": open(filepath, "rb"),
                # }
                response = requests.get(
                    apiurl,
                    headers=headers,
                    params=payload,
                    timeout=600,
                    proxies=proxies,
                )
                for x in range(retryCount):
                    if response.status_code == 200 or response.status_code == 201:
                        break
                    time.sleep(timetowait)
                    # files = {
                    #    "file": open(filepath, "rb"),
                    # }

                    response = requests.get(
                        apiurl,
                        headers=headers,
                        params=payload,
                        timeout=600,
                        proxies=proxies,
                    )
            else:
                auth = HTTPProxyAuth(username, password)
                # files = {
                #    "file": open(filepath, "rb"),
                # }
                response = requests.get(
                    apiurl,
                    headers=headers,
                    params=payload,
                    timeout=600,
                    proxies=proxies,
                    auth=auth,
                )
                for x in range(retryCount):
                    if response.status_code == 200 or response.status_code == 201:
                        break
                    time.sleep(timetowait)
                    # files = {
                    #     "file": open(filepath, "rb"),
                    # }
                    response = requests.get(
                        apiurl,
                        headers=headers,
                        params=payload,
                        timeout=600,
                        proxies=proxies,
                        auth=auth,
                    )
        except:
            print("Exception importing, retrying")
            httpproxy = proxy
            httpsproxy = proxy
            proxies = {"http": httpproxy, "https": httpsproxy}
            if username == "":
                # files = {
                #    "file": open(filepath, "rb"),
                # }
                # files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                response = requests.get(
                    apiurl,
                    headers=headers,
                    params=payload,
                    timeout=600,
                    proxies=proxies,
                )
                for x in range(retryCount):
                    if response.status_code == 200 or response.status_code == 201:
                        break
                    time.sleep(timetowait)
                    # files = {
                    #     "file": open(filepath, "rb"),
                    # }
                    response = requests.get(
                        apiurl,
                        headers=headers,
                        params=payload,
                        timeout=600,
                        proxies=proxies,
                    )
            else:
                auth = HTTPProxyAuth(username, password)
                # files = {
                #     "file": open(filepath, "rb"),
                # }
                response = requests.get(
                    apiurl,
                    headers=headers,
                    params=payload,
                    timeout=600,
                    proxies=proxies,
                    auth=auth,
                )
                for x in range(retryCount):
                    if response.status_code == 200 or response.status_code == 201:
                        break
                    time.sleep(timetowait)
                    # files = {
                    #     "file": open(filepath, "rb"),
                    # }
                    # files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                    response = requests.get(
                        apiurl,
                        headers=headers,
                        params=payload,
                        timeout=600,
                        proxies=proxies,
                        auth=auth,
                    )

    print("file sent")
    if response.status_code >= 500:
        if retryImport == True and "Parse error" in response.content.decode("utf-8"):
            print("retrying import after parsing errors")
            get_tests_file(retryImport=False)
            return
        else:
            print(
                (
                    "[!] [{0}] Server Error {1}".format(
                        response.status_code, response.content.decode("utf-8")
                    )
                )
            )
    elif response.status_code == 404:
        print(("[!] [{0}] URL not found: []".format(response.status_code)))
    elif response.status_code == 401:
        print(("[!] [{0}] Authentication Failed".format(response.status_code)))
    elif response.status_code == 400:
        print(
            (
                "[!] [{0}] Bad Request: Content: {1}".format(
                    response.status_code, response.content
                )
            )
        )
    elif response.status_code >= 300:
        print(("[!] [{0}] Unexpected Redirect".format(response.status_code)))
    elif response.status_code == 200 or response.status_code == 201:
        # resultset = json.loads(response.content.decode("utf-8"))
        # print(response.content)
        return response.content.decode("utf-8")
    else:
        print(
            (
                "[?] Unexpected Error: [HTTP {0}]: Content: {1}".format(
                    response.status_code, response.content
                )
            )
        )
    if retryImport == True:
        if response.status_code != 200 and response.status_code != 201:
            print("retrying import")
            time.sleep(5)
            get_tests_file(retryImport=False)


def compare_file_to_string(file_path, string):
    """
    Compares the contents of a file to a given string.
    Returns an array of lines from the file that were not found in the string.
    """
    lines_not_found = []

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            if line not in string:
                lines_not_found.append(line)

    return lines_not_found


# Example usage
# file_path = 'example.txt'
# string_to_compare = "This is a sample string to compare against the file."
#
# lines_missing = compare_file_to_string(file_path, string_to_compare)
# print("Lines from the file that were not found in the string:")
# for line in lines_missing:
#     print(line)


# def failfast_tests(tests):
def failfast_tests():
    if failfast == "true":
        print("failing fast")
        rerun_tests()
        try:
            getresults()
        except:
            print("unable to find results")


def rerun_tests_execute():
    get_and_run_tests(5)


def rerun_tests():
    if rerun == "true":
        numruns = 1
        while numruns <= maxrerun:
            echo("rerun " + str(numruns))
            rerun_tests_execute()
            numruns = numruns + 1


def getresults(retryResults=True):
    global run_id
    print(run_id)
    if run_id == "":
        print("no results")
        # os._exit(0)
        return
    echo("getting results")
    headers = {
        "token": apikey,
    }
    api_url = url + "/api/external/output/"
    params = (("test_run", run_id),)
    print(params)
    print(headers)

    # s = requests.Session()

    # retries = Retry(total=3,
    #                backoff_factor=5,
    #                status_forcelist=[ 400, 500, 502, 503, 504 ])

    # s.mount(url, HTTPAdapter(max_retries=retries))
    retryCount = 3
    if proxy == "":
        response = requests.get(
            url + "/api/external/output/", headers=headers, params=params, timeout=600
        )
        for x in range(retryCount):
            timetowait = maxretrytime / retryCount
            if response.status_code == 200:
                break
            time.sleep(timetowait)
            response = requests.get(
                url + "/api/external/output/",
                headers=headers,
                params=params,
                timeout=600,
            )
    else:
        try:
            httpproxy = "http://" + proxy
            httpsproxy = "https://" + proxy
            proxies = {"http": httpproxy, "https": httpsproxy}
            if username == "":
                response = requests.get(
                    url + "/api/external/output/",
                    headers=headers,
                    params=params,
                    proxies=proxies,
                    timeout=600,
                )
                for x in range(retryCount):
                    timetowait = maxretrytime / retryCount
                    if response.status_code == 200:
                        break
                    time.sleep(timetowait)
                    response = requests.get(
                        url + "/api/external/output/",
                        headers=headers,
                        params=params,
                        proxies=proxies,
                        timeout=600,
                    )
            else:
                auth = HTTPProxyAuth(username, password)
                response = requests.get(
                    url + "/api/external/output/",
                    headers=headers,
                    params=params,
                    proxies=proxies,
                    auth=auth,
                    timeout=600,
                )
                for x in range(retryCount):
                    timetowait = maxretrytime / retryCount
                    if response.status_code == 200:
                        break
                    time.sleep(timetowait)
                    response = requests.get(
                        url + "/api/external/output/",
                        headers=headers,
                        params=params,
                        proxies=proxies,
                        auth=auth,
                        timeout=600,
                    )
        except:
            httpproxy = proxy
            httpsproxy = proxy
            proxies = {"http": httpproxy, "https": httpsproxy}
            if username == "":
                response = requests.get(
                    url + "/api/external/output/",
                    headers=headers,
                    params=params,
                    proxies=proxies,
                    timeout=600,
                )
                for x in range(retryCount):
                    timetowait = maxretrytime / retryCount
                    if response.status_code == 200:
                        break
                    time.sleep(timetowait)
                    response = requests.get(
                        url + "/api/external/output/",
                        headers=headers,
                        params=params,
                        proxies=proxies,
                        timeout=600,
                    )
            else:
                auth = HTTPProxyAuth(username, password)
                response = requests.get(
                    url + "/api/external/output/",
                    headers=headers,
                    params=params,
                    proxies=proxies,
                    auth=auth,
                    timeout=600,
                )
                for x in range(retryCount):
                    timetowait = maxretrytime / retryCount
                    if response.status_code == 200:
                        break
                    time.sleep(timetowait)
                    response = requests.get(
                        url + "/api/external/output/",
                        headers=headers,
                        params=params,
                        proxies=proxies,
                        auth=auth,
                        timeout=600,
                    )
    print("result request sent")
    resultset = ""
    if response.status_code >= 500:
        print(
            (
                "[!] [{0}] Server Error {1}".format(
                    response.status_code, response.content.decode("utf-8")
                )
            )
        )
        return None
    elif response.status_code == 404:
        print(("[!] [{0}] URL not found: [{1}]".format(response.status_code, api_url)))
        return None
    elif response.status_code == 401:
        print(("[!] [{0}] Authentication Failed".format(response.status_code)))
        return None
    elif response.status_code == 400:
        print(
            (
                "[!] [{0}] Bad Request: Content: {1}".format(
                    response.status_code, response.content
                )
            )
        )
        return None
    elif response.status_code >= 300:
        print(("[!] [{0}] Unexpected Redirect".format(response.status_code)))
        return None
    elif response.status_code == 200:
        resultset = json.loads(response.content.decode("utf-8"))
        echo(resultset)
    else:
        print(
            (
                "[?] Unexpected Error: [HTTP {0}]: Content: {1}".format(
                    response.status_code, response.content
                )
            )
        )

    # if retryResults == True:
    #    if response.status_code != 200:
    #        print("retrying getting results")
    #        getresults(retryResults=False)
    #        return

    if resultset["new_defects"] and "newdefects" in fail:
        exit(1)
    if resultset["reopened_defects"] != 0 and "reopeneddefects" in fail:
        exit(1)
    if resultset["flaky_defects"] != 0 and "newflaky" in fail:
        exit(1)
    if resultset["reopened_flaky_defects"] != 0 and "reopenedflaky" in fail:
        exit(1)
    if resultset["flaky_failures_breaks"] != 0 and "flakybrokentests" in fail:
        exit(1)
    if resultset["failed_test"] != 0 and "failedtests" in fail:
        exit(1)
    if resultset["broken_test"] != 0 and "brokentests" in fail:
        exit(1)


def convertcucumberfile(cucumberfile, xmlfile):
    with open(cucumberfile, "r", encoding="utf8", errors="ignore") as json_file:
        print("Opening file " + cucumberfile + " in read-only")
        try:
            json_data = json.load(json_file)
        except Exception as error:
            # handle the exception
            print(
                "An exception occurred:", error
            )  # An exception occurred: division by zero

    test_cases = ""
    header = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'

    test_suite_time = 0.0
    failure_count = 0
    scenario_count = 0

    for feature in json_data:
        feature_name = sanitize(feature["name"])
        scenarios = feature["elements"]
        feature_time = 0.0

        for scenario in scenarios:
            scenario_count += 1

            scenario_name = sanitize(scenario["name"])
            steps_blob = "<![CDATA["
            err_blob = ""
            scenario_status = "passed"
            scenario_time = 0.0

            if scenario["type"] != "background":
                for tag in scenario["tags"]:
                    steps_blob += tag["name"] + " "
                steps_blob += "\n"
            for step in scenario["steps"]:
                try:
                    description = sanitize(step["name"])
                except:
                    description = ""
                results = step["result"]
                status = sanitize(results["status"])
                keyword = sanitize(step["keyword"])

                if status != "skipped":
                    try:
                        scenario_time += float(results["duration"]) / 1000000000
                    except:
                        do_nothing = ""

                num_dots = 83 - len(keyword) - len(description) - len(status)
                if num_dots <= 0:
                    num_dots = 1

                steps_blob += keyword + description
                for i in range(num_dots):
                    steps_blob += "."
                steps_blob += status + "\n"
                if status == "failed":
                    err_blob = sanitize(results["error_message"])
                    scenario_status = "failed"
                    failure_count += 1
            feature_time += scenario_time

            steps_blob += "]]>"

            test_case = "<testcase "
            test_case += 'classname="' + feature_name + '" '
            test_case += 'name="' + scenario_name + '" '
            test_case += 'time="' + str(scenario_time) + '">'
            if scenario_status == "passed":
                test_case += "<system-out>" + steps_blob + "</system-out>\n"
            else:
                test_case += '<failure message="' + err_blob + '">'
                test_case += steps_blob + "</failure>\n"
            test_case += "</testcase>\n"

            test_cases += test_case
            test_suite_time += feature_time
    test_suite = "<testsuite "
    test_suite += 'failures="' + str(failure_count) + '" '
    test_suite += 'name="Cucumber JSON to JUnit" '
    test_suite += 'skipped="0" '
    test_suite += 'tests="' + str(scenario_count) + '" '
    test_suite += 'time="' + str(test_suite_time) + '">\n'
    for test_case in test_cases:
        test_suite += test_case
    test_suite += "</testsuite>"
    with open(xmlfile, "w") as junit_file:
        print("Writing to file " + xmlfile + "...")
        junit_file.write(header)
        junit_file.write(test_suite)


def sanitize(input):
    try:
        input = input.replace("&", "&amp;").replace('"', "&quot;")
        input = input.replace("<", "&lt;").replace(">", "&gt;")
    except:
        input = ""
    return input


def convertcucumberfolderrecursive(directoryToPushFrom):
    for root, dirs, files in os.walk(directoryToPushFrom):
        for file in files:
            if file.lower().endswith(".json"):
                convertcucumberfile(
                    os.path.abspath(os.path.join(root, file)),
                    os.path.abspath(os.path.join(root, file)) + ".xml",
                )


def convertcucumberfolder(directoryToPushFrom):
    for file in os.listdir(directoryToPushFrom):
        if file.lower().endswith(".json"):
            convertcucumberfile(
                os.path.abspath(os.path.join(directoryToPushFrom, file)),
                os.path.abspath(os.path.join(directoryToPushFrom, file)) + ".xml",
            )


def push_results():
    global run_id, fullreportdir
    print("pushing results " + reporttype + " " + report)

    if trainer == "true":
        runcommand("trainer")

    if reporttype == "directory" and (mergefiles == "True" or mergereports == "True"):
        if fullreportdir != "":
            if os.path.isdir(fullreportdir):
                print("fullreportdir directory is correct")
            else:
                fullreportdir = os.path.join(
                    os.getcwd(), fullreportdir.strip("\\").strip("/")
                )
                if not os.path.isdir(fullreportdir):
                    if report.startswith(".") and not report.startswith(".."):
                        fullreportdir = os.path.join(
                            os.getcwd(), report[1:].strip("\\").strip("/")
                        )
                if os.path.isdir(fullreportdir):
                    print("using dir for fullreport" + fullreportdir)
                else:
                    print(
                        "ERROR - Path to report is incorrect, please use the full path"
                    )

    if reporttype == "directory" and mergefiles == "True":
        try:
            directoryToPushFrom = report
            if os.path.isdir(report):
                print("directory is correct")
            else:
                directoryToPushFrom = os.path.join(
                    os.getcwd(), directoryToPushFrom.strip("\\").strip("/")
                )
                if not os.path.isdir(directoryToPushFrom):
                    if report.startswith(".") and not report.startswith(".."):
                        directoryToPushFrom = os.path.join(
                            os.getcwd(), report[1:].strip("\\").strip("/")
                        )
            if os.path.isdir(directoryToPushFrom):
                print("using dir " + directoryToPushFrom)
                if fullreportdir == "":
                    fullreportdir = directoryToPushFrom

                # Ensure directory exists or created
                fullreportdir = pathlib.Path(fullreportdir)
                fullreportdir.mkdir(parents=True, exist_ok=True)

                path = pathlib.Path(directoryToPushFrom)
                print(directoryToPushFrom)
                print(path)
                try:
                    junit_merger = JUnitReportMerger.from_directory(directory=path)
                    junit_merger.merge()
                    junit_report = junit_merger.result  # internal format
                    full_report_file = fullreportdir.joinpath("full_report.xml")
                    full_report_file.write_text(junit_report.model_dump_xml())
                    print(f"Importing file: {full_report_file}")
                    call_import(str(full_report_file.resolve()))
                except Exception as e:
                    print(str(e))
            else:
                print("ERROR - Path to report is incorrect, please use the full path")

        except Exception as e:
            print(e)
            print("Import failed")

    if reporttype == "directory" and mergefiles != "True":
        directoryToPushFrom = report
        if os.path.isdir(report):
            print("directory is correct")
        else:
            directoryToPushFrom = os.path.join(
                os.getcwd(), directoryToPushFrom.strip("\\").strip("/")
            )
            if not os.path.isdir(directoryToPushFrom):
                if report.startswith(".") and not report.startswith(".."):
                    directoryToPushFrom = os.path.join(
                        os.getcwd(), report[1:].strip("\\").strip("/")
                    )
            if os.path.isdir(directoryToPushFrom):
                print("using dir " + directoryToPushFrom)
            else:
                print("ERROR - Path to report is incorrect, please use the full path")
        if fullreportdir == "":
            fullreportdir = directoryToPushFrom
        filetype = ".xml"
        full_report_file = os.path.abspath(
            os.path.join(fullreportdir, "full_report.xml")
        )
        print("Checking to merge reports")
        if mergereports == "True":
            print("Creating file full report")
            print(full_report_file)
            try:
                with open(full_report_file, "w") as text_file:
                    text_file.write("")
            except Exception as e:
                print(str(e))
            # with open(full_report_file, 'w') as fp:
            #    pass
            print("Full report file created")
        if recursive == "true":
            if importtype == "trx":
                filetype = ".trx"
            pushedfile = False
            if convertcucumber.lower() == "true":
                convertcucumberfolderrecursive(directoryToPushFrom)
            for root, dirs, files in os.walk(directoryToPushFrom):
                for file in files:
                    if file.endswith(filetype):
                        try:
                            if mergereports == "True":
                                if "full_report" not in file:
                                    if pushedfile:
                                        full_report = JUnitXml.fromfile(
                                            full_report_file
                                        )
                                        new_report = JUnitXml.fromfile(
                                            os.path.abspath(os.path.join(root, file))
                                        )
                                        # Merge in place and write back to same file
                                        full_report += new_report
                                        full_report.write()
                                        pushedfile = True
                                    else:
                                        shutil.copyfile(
                                            os.path.abspath(os.path.join(root, file)),
                                            full_report_file,
                                        )
                                        pushedfile = True
                            else:
                                call_import(os.path.abspath(os.path.join(root, file)))
                                pushedfile = True
                        except:
                            print("import failed")
            if mergereports == "True":
                call_import(full_report_file)
                pushedfile = True
            if pushedfile == False:
                print("No files pushed")
        if recursive == "false":
            print("Preparing to push files")
            if importtype == "trx":
                filetype = ".trx"
            pushedfile = False
            if convertcucumber.lower() == "true":
                convertcucumberfolder(directoryToPushFrom)
            for file in os.listdir(directoryToPushFrom):
                if file.endswith(filetype):
                    echo(file)
                    if mergereports == "True":
                        if "full_report" not in file:
                            if pushedfile:
                                print(full_report_file)
                                full_report = JUnitXml.fromfile(full_report_file)
                                print(os.path.join(directoryToPushFrom, file))
                                new_report = JUnitXml.fromfile(
                                    os.path.join(directoryToPushFrom, file)
                                )
                                # Merge in place and write back to same file
                                full_report += new_report
                                full_report.write()
                                pushedfile = True
                            else:
                                try:
                                    shutil.copyfile(
                                        os.path.join(directoryToPushFrom, file),
                                        full_report_file,
                                    )
                                    pushedfile = True
                                except Exception as e:
                                    print(str(e))
                    else:
                        try:
                            call_import(
                                os.path.abspath(os.path.join(directoryToPushFrom, file))
                            )
                            pushedfile = True
                        except:
                            print("import failed")
            if mergereports == "True":
                call_import(full_report_file)
            if pushedfile == False:
                print("No files pushed")

    if reporttype == "file":
        try:
            print("Importing file: " + report)
            call_import(report)
        except Exception as e:
            print(e)
            print("Import failed")


def call_import(filepath, retryImport=True, replaceAscii=False):
    global run_id
    origfilepath = filepath

    print("Current dir " + os.getcwd())
    print("importing results from " + filepath)

    # curr_dir = os.getcwd()
    # if not filepath.startswith(curr_dir):
    #     filepath = os.path.join(curr_dir, filepath)
    #
    # print("importing results 2 from " + filepath)

    if importtype == "trx" and replaceretry == "true":
        try:
            with open(filepath, "r", errors="ignore") as openfile:
                filedata = openfile.read()

                # Replace the target string
            filedata = re.sub(r" retry #\d\"", '"', filedata)

            # Write the file out again
            with open(filepath, "w") as openfile:
                openfile.write(filedata)
        except Exception as e:
            print(str(e))
            print("unable to strip retries from file")

    try:
        with open(filepath, "r", errors="ignore") as openfile:
            filedata = openfile.read()

            # Replace the target string
        if filedata.startswith(
            "This XML file does not appear to have any style information associated with it. The document tree is shown below."
        ):
            print("replacing invalid xml")
            filedata = filedata.replace(
                "This XML file does not appear to have any style information associated with it. The document tree is shown below.",
                "",
            )
            with open(filepath, "w") as openfile:
                openfile.write(filedata)

        # Write the file out again
    except:
        testpath = filepath
        # print("unable to remove text")
    if replaceAscii:
        try:
            with open(filepath, "r", errors="ignore") as openfile:
                filedata = openfile.read()

                # Replace the target string
            filedata = replace_non_ascii(filedata)

            # Write the file out again
            with open(filepath, "w") as openfile:
                openfile.write(filedata)
        except:
            print("unable to strip Ascii")
    try:
        sizeOfFile = os.path.getsize(filepath)
    except:
        print("Unable to get file size")
        sizeOfFile = 0
    # if importtype == "trx" and sizeOfFile > 1000000:
    #    ET.register_namespace("", "http://microsoft.com/schemas/VisualStudio/TeamTest/2010")
    #    tree = ET.ElementTree()
    #    tree.parse(filepath)
    #    root = tree.getroot()
    #    ns = re.match(r'{.*}', root.tag).group(0)
    #    for test in root.findall(f"{ns}Results"):
    #        for testresult in test.findall(f"{ns}UnitTestResult"):
    # testName = (testresult.get("testName"))
    # sep = ','
    # testName = testName.split(sep, 1)[0]
    # sep = ' '
    # testName = testName.split(sep, 1)[0]
    # testresult.set("testName", testName)
    #            for output in testresult.findall(f"{ns}Output"):
    #                for stderr in output.findall(f"{ns}StdOut"):
    #                    stderr.text = stderr.text[:500]
    #                for stderr in output.findall(f"{ns}StdErr"):
    #                    stderr.text = stderr.text[:500]
    #                for ErrorInfo in output.findall(f"{ns}ErrorInfo"):
    #                    for stacktrace in ErrorInfo.findall(f"{ns}StackTrace"):
    #                        stacktrace.text = stacktrace.text[:500]
    #    tree.write(filepath)
    if importtype == "trx" and sizeOfFile > 1000000:
        ET.register_namespace(
            "", "http://microsoft.com/schemas/VisualStudio/TeamTest/2010"
        )
        tree = ET.ElementTree()
        with open(filepath, "r", errors="replace", encoding="utf8") as f:
            root = ET.fromstring(f.read())
            tree = ET.ElementTree()
            ns = re.match(r"{.*}", root.tag).group(0)
            for test in root.findall(f"{ns}Results"):
                for testresult in test.findall(f"{ns}UnitTestResult"):
                    for output in testresult.findall(f"{ns}Output"):
                        for stderr in output.findall(f"{ns}StdOut"):
                            stderr.text = stderr.text[:500]
                        for stderr in output.findall(f"{ns}StdErr"):
                            stderr.text = stderr.text[:500]
                        for ErrorInfo in output.findall(f"{ns}ErrorInfo"):
                            for stacktrace in ErrorInfo.findall(f"{ns}StackTrace"):
                                stacktrace.text = stacktrace.text[:500]
            try:
                tree._setroot(root)
                tree.write(filepath)
            except:
                print("unable to write file")
    if importtype == "junit":
        try:
            with open(filepath, "r", errors="replace", encoding="utf8") as f:
                root = ET.fromstring(f.read())
                tree = ET.ElementTree()
                added_failure_type = False
                for test in root.findall("testcase"):
                    failure = test.find("failure")
                    if failure is None:
                        continue
                    else:
                        if "type" not in failure.attrib:
                            failure.set("type", "AssertionError")
                            added_failure_type = True
                if added_failure_type:
                    tree._setroot(root)
                    tree.write(filepath)
        except:
            print("unable to set failure type")
    if webdriverio == "true":
        tree = ElementTree()
        tree.parse(filepath)
        root = tree.getroot()

        for test in root.iter("testcase"):
            # print("found testcase")
            # for sysout in test.findall('system-out'):
            #    test.remove(sysout)
            # for syserror in test.findall('system-err'):
            #    test.remove(syserror)
            message = ""
            for error in test.findall("error"):
                message = error.get("message")

            for failure in test.findall("failure"):
                failure.set("message", message)

        tree.write(filepath)

    apiurl = url + "/api/external/import/"

    payload = {
        "type": importtype,
        "commit": commit,
        "project_name": projectencoded,
        "test_suite_name": testsuiteencoded,
        "repo": repository,
        "import_type": "prioritized",
    }

    if teststorun == "all":
        payload["import_type"] = "full_test_run"

    if repo_name != "":
        payload["repo_name"] = repo_name

    # files = {
    #     "file": open(filepath, "rb"),
    # }

    files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]

    headers = {
        "Token": apikey,
    }

    print(headers)
    print(payload)
    print(apiurl)
    print("=======================================")

    retryCount = 3
    timetowait = (maxretrytime / 2) / retryCount

    if proxy == "":
        response = requests.post(apiurl, headers=headers, data=payload, files=files)

        for x in range(retryCount):
            if response.status_code == 200 or response.status_code == 201:
                break
            print(("Status code : [{0}] Retrying".format(response.status_code)))
            time.sleep(timetowait)
            # files = {
            #     "file": open(filepath, "rb"),
            # }
            files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
            response = requests.post(apiurl, headers=headers, data=payload, files=files)
    else:
        try:
            httpproxy = "http://" + proxy
            httpsproxy = "https://" + proxy
            proxies = {"http": httpproxy, "https": httpsproxy}
            if username == "":
                # files = {
                #    "file": open(filepath, "rb"),
                # }
                files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                response = requests.post(
                    apiurl, headers=headers, data=payload, files=files, proxies=proxies
                )
                for x in range(retryCount):
                    if response.status_code == 200 or response.status_code == 201:
                        break
                    time.sleep(timetowait)
                    # files = {
                    #    "file": open(filepath, "rb"),
                    # }
                    files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                    response = requests.post(
                        apiurl,
                        headers=headers,
                        data=payload,
                        files=files,
                        proxies=proxies,
                    )
            else:
                auth = HTTPProxyAuth(username, password)
                # files = {
                #    "file": open(filepath, "rb"),
                # }
                files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                response = requests.post(
                    apiurl,
                    headers=headers,
                    data=payload,
                    files=files,
                    proxies=proxies,
                    auth=auth,
                )
                for x in range(retryCount):
                    if response.status_code == 200 or response.status_code == 201:
                        break
                    time.sleep(timetowait)
                    # files = {
                    #     "file": open(filepath, "rb"),
                    # }
                    files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                    response = requests.post(
                        apiurl,
                        headers=headers,
                        data=payload,
                        files=files,
                        proxies=proxies,
                        auth=auth,
                    )
        except:
            print("Exception importing, retrying")
            httpproxy = proxy
            httpsproxy = proxy
            proxies = {"http": httpproxy, "https": httpsproxy}
            if username == "":
                # files = {
                #    "file": open(filepath, "rb"),
                # }
                files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                response = requests.post(
                    apiurl, headers=headers, data=payload, files=files, proxies=proxies
                )
                for x in range(retryCount):
                    if response.status_code == 200 or response.status_code == 201:
                        break
                    time.sleep(timetowait)
                    # files = {
                    #     "file": open(filepath, "rb"),
                    # }
                    files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                    response = requests.post(
                        apiurl,
                        headers=headers,
                        data=payload,
                        files=files,
                        proxies=proxies,
                    )
            else:
                auth = HTTPProxyAuth(username, password)
                # files = {
                #     "file": open(filepath, "rb"),
                # }
                files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                response = requests.post(
                    apiurl,
                    headers=headers,
                    data=payload,
                    files=files,
                    proxies=proxies,
                    auth=auth,
                )
                for x in range(retryCount):
                    if response.status_code == 200 or response.status_code == 201:
                        break
                    time.sleep(timetowait)
                    # files = {
                    #     "file": open(filepath, "rb"),
                    # }
                    files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                    response = requests.post(
                        apiurl,
                        headers=headers,
                        data=payload,
                        files=files,
                        proxies=proxies,
                        auth=auth,
                    )

    print("file import sent")
    if response.status_code >= 500:
        if retryImport == True and "Parse error" in response.content.decode("utf-8"):
            print("retrying import after parsing errors")
            call_import(origfilepath, retryImport=False, replaceAscii=True)
            return
        else:
            print(
                (
                    "[!] [{0}] Server Error {1}".format(
                        response.status_code, response.content.decode("utf-8")
                    )
                )
            )
    elif response.status_code == 404:
        print(("[!] [{0}] URL not found: []".format(response.status_code)))
    elif response.status_code == 401:
        print(("[!] [{0}] Authentication Failed".format(response.status_code)))
    elif response.status_code == 400:
        print(
            (
                "[!] [{0}] Bad Request: Content: {1}".format(
                    response.status_code, response.content
                )
            )
        )
    elif response.status_code >= 300:
        print(("[!] [{0}] Unexpected Redirect".format(response.status_code)))
    elif response.status_code == 200 or response.status_code == 201:
        resultset = json.loads(response.content.decode("utf-8"))
        echo(resultset)
        echo("report url = " + resultset["report_url"])
        echo("run url = " + str(resultset["test_run_id"]))
        run_id = str(resultset["test_run_id"])
    else:
        print(
            (
                "[?] Unexpected Error: [HTTP {0}]: Content: {1}".format(
                    response.status_code, response.content
                )
            )
        )
    if retryImport == True:
        if response.status_code != 200 and response.status_code != 201:
            print("retrying import")
            time.sleep(5)
            call_import(origfilepath, retryImport=False)


def call_upload(retryImport=True):
    payload = {
        "project_name": project,
        "testsuite_name": testsuite,
    }
    filepath = "testlist.txt"

    files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]

    headers = {
        "Token": apikey,
    }
    apiurl = url + "/fileimport/upload"

    print(headers)
    print(payload)
    print(apiurl)
    print("=======================================")

    retryCount = 3
    timetowait = (maxretrytime / 2) / retryCount

    if proxy == "":
        response = requests.post(apiurl, headers=headers, data=payload, files=files)

        for x in range(retryCount):
            if response.status_code == 200 or response.status_code == 201:
                break
            print(("Status code : [{0}] Retrying".format(response.status_code)))
            time.sleep(timetowait)
            # files = {
            #     "file": open(filepath, "rb"),
            # }
            files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
            response = requests.post(apiurl, headers=headers, data=payload, files=files)
    else:
        try:
            httpproxy = "http://" + proxy
            httpsproxy = "https://" + proxy
            proxies = {"http": httpproxy, "https": httpsproxy}
            if username == "":
                # files = {
                #    "file": open(filepath, "rb"),
                # }
                files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                response = requests.post(
                    apiurl, headers=headers, data=payload, files=files, proxies=proxies
                )
                for x in range(retryCount):
                    if response.status_code == 200 or response.status_code == 201:
                        break
                    time.sleep(timetowait)
                    # files = {
                    #    "file": open(filepath, "rb"),
                    # }
                    files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                    response = requests.post(
                        apiurl,
                        headers=headers,
                        data=payload,
                        files=files,
                        proxies=proxies,
                    )
            else:
                auth = HTTPProxyAuth(username, password)
                # files = {
                #    "file": open(filepath, "rb"),
                # }
                files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                response = requests.post(
                    apiurl,
                    headers=headers,
                    data=payload,
                    files=files,
                    proxies=proxies,
                    auth=auth,
                )
                for x in range(retryCount):
                    if response.status_code == 200 or response.status_code == 201:
                        break
                    time.sleep(timetowait)
                    # files = {
                    #     "file": open(filepath, "rb"),
                    # }
                    files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                    response = requests.post(
                        apiurl,
                        headers=headers,
                        data=payload,
                        files=files,
                        proxies=proxies,
                        auth=auth,
                    )
        except:
            print("Exception importing, retrying")
            httpproxy = proxy
            httpsproxy = proxy
            proxies = {"http": httpproxy, "https": httpsproxy}
            if username == "":
                # files = {
                #    "file": open(filepath, "rb"),
                # }
                files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                response = requests.post(
                    apiurl, headers=headers, data=payload, files=files, proxies=proxies
                )
                for x in range(retryCount):
                    if response.status_code == 200 or response.status_code == 201:
                        break
                    time.sleep(timetowait)
                    # files = {
                    #     "file": open(filepath, "rb"),
                    # }
                    files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                    response = requests.post(
                        apiurl,
                        headers=headers,
                        data=payload,
                        files=files,
                        proxies=proxies,
                    )
            else:
                auth = HTTPProxyAuth(username, password)
                # files = {
                #     "file": open(filepath, "rb"),
                # }
                files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                response = requests.post(
                    apiurl,
                    headers=headers,
                    data=payload,
                    files=files,
                    proxies=proxies,
                    auth=auth,
                )
                for x in range(retryCount):
                    if response.status_code == 200 or response.status_code == 201:
                        break
                    time.sleep(timetowait)
                    # files = {
                    #     "file": open(filepath, "rb"),
                    # }
                    files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                    response = requests.post(
                        apiurl,
                        headers=headers,
                        data=payload,
                        files=files,
                        proxies=proxies,
                        auth=auth,
                    )

    print("file upload sent")
    if response.status_code >= 500:
        if retryImport == True and "Parse error" in response.content.decode("utf-8"):
            print("retrying import after parsing errors")
            call_upload(retryImport=False)
            return
        else:
            print(
                (
                    "[!] [{0}] Server Error {1}".format(
                        response.status_code, response.content.decode("utf-8")
                    )
                )
            )
    elif response.status_code == 404:
        print(("[!] [{0}] URL not found: []".format(response.status_code)))
    elif response.status_code == 401:
        print(("[!] [{0}] Authentication Failed".format(response.status_code)))
    elif response.status_code == 400:
        print(
            (
                "[!] [{0}] Bad Request: Content: {1}".format(
                    response.status_code, response.content
                )
            )
        )
    elif response.status_code >= 300:
        print(("[!] [{0}] Unexpected Redirect".format(response.status_code)))
    elif response.status_code == 200 or response.status_code == 201:
        resultset = json.loads(response.content.decode("utf-8"))
    else:
        print(
            (
                "[?] Unexpected Error: [HTTP {0}]: Content: {1}".format(
                    response.status_code, response.content
                )
            )
        )
    if retryImport == True:
        if response.status_code != 200 and response.status_code != 201:
            print("retrying import")
            time.sleep(5)
            call_upload(retryImport=False)


def runtestswithappsurify(*args):
    global tests, teststorun, run_id, proxy, username, password, url, apikey, project, testsuite, report, maxtests, fail, additionalargs, testseparator, postfixtest, prefixtest
    global fullnameseparator, fullname, failfast, maxrerun, rerun, importtype, reporttype, teststorun, deletereports, startrunall, endrunall, startrunspecific, endrunspecific
    global commit, scriptlocation, branch, runfrequency, fromcommit, repository, scriptlocation, generatefile, template, addtestsuitename, addclassname, runtemplate, testsuitesnameseparator
    global testtemplate, classnameseparator, testseparatorend, testtemplatearg1, testtemplatearg2, testtemplatearg3, testtemplatearg4, startrunpostfix, endrunprefix
    global endrunpostfix, executetests, encodetests, testsuiteencoded, projectencoded, testsrun, trainer, azure_variable, pipeoutput, recursive, bitrise, executioncommand, githubactionsvariable, printcommand
    global azurefilter, replaceretry, webdriverio, percentage, endspecificrun, runnewtests, weekendrunall, daysrunall, newdays, azurefilteronall, azurevariablenum, commandset, alwaysrun, alwaysrunset
    global azurealwaysrun, azurealwaysrunset, upload, createfile, createpropertiesfile, spliton, nopush, repo_name, screenplay, endcommand, createfiles, createfilesdirectory, maxretrytime, testsetnum
    global numtestsets, filenames, printout, includefailing, convertcucumber, escapetests, circlecivariable, circlecivariablenobash, mergereports, mergefiles, fullreportdir, azureTest, dll, dlllocation, vstestlocation, startTimeRunAll
    try:
        tests = ""
        testsrun = ""
        run_id = ""
        proxy = ""
        username = ""
        password = ""
        url = ""
        apikey = ""
        project = ""
        testsuite = ""
        report = ""
        maxtests = 1000000  # default 10000000
        fail = "newdefects, reopeneddefects"  # default new defects and reopened defects  #options newdefects, reopeneddefects, flakybrokentests, newflaky, reopenedflaky, failedtests, brokentests
        additionalargs = ""  # default ''
        testseparator = ""  # default ' '
        postfixtest = ""  # default ''
        prefixtest = ""  # default ''
        fullnameseparator = ""  # default ''
        fullname = "false"  # default false
        failfast = "false"  # defult false
        maxrerun = 3  # default 3
        rerun = "false"  # default false
        importtype = "junit"  # default junit
        reporttype = "directory"  # default directory other option file, when directory needs to end with /
        teststorun = (
            "all"  # options include - high, medium, low, unassigned, ready, open, none
        )
        deletereports = "false"  # options true or false, BE CAREFUL THIS WILL DELETE THE SPECIFIC FILE OR ALL XML FILES IN THE DIRECTORY
        startrunall = ""  # startrun needs to end with a space sometimes
        endrunall = ""  # endrun needs to start with a space sometimes
        startrunspecific = ""  # startrun needs to end with a space sometimes
        endrunspecific = ""  # endrun needs to start with a space sometimes
        commit = ""
        scriptlocation = "./"
        branch = ""
        # runfrequency="single" #options single for single commits, lastrun for all commits since the last run, betweeninclusive or betweenexclusive for all commits between two commits either inclusive or exclusive
        runfrequency = "multiple"  # options single for ['Single', 'LastRun', 'BetweenInclusive', 'BetweenExclusive']
        fromcommit = ""
        repository = "git"
        scriptlocation = "./"
        generatefile = "false"
        template = "none"
        addtestsuitename = "false"
        addclassname = "false"
        runtemplate = ""
        testsuitesnameseparator = ""
        testtemplate = ""
        classnameseparator = ""
        testseparatorend = ""
        testtemplatearg1 = ""
        testtemplatearg2 = ""
        testtemplatearg3 = ""
        testtemplatearg4 = ""
        startrunpostfix = ""
        endrunprefix = ""
        endrunpostfix = ""
        executetests = "true"
        encodetests = "false"
        escapetests = "false"
        trainer = "false"
        azure_variable = "appsurifytests"
        pipeoutput = "false"
        bitrise = "false"
        recursive = "false"
        executioncommand = ""
        githubactionsvariable = ""
        circlecivariable = ""
        circlecivariablenobash = ""
        printcommand = ""
        testsuiteencoded = ""
        projectencoded = ""
        azurefilter = ""
        azurefilteronall = "true"
        replaceretry = "false"
        webdriverio = "false"
        percentage = ""
        endspecificrun = ""
        runnewtests = "false"
        weekendrunall = "false"
        daysrunall = ""
        newdays = 14
        azurevariablenum = 0
        commandset = ""
        alwaysrun = ""
        alwaysrunset = []
        azurealwaysrun = ""
        azurealwaysrunset = []
        upload = "true"
        createfile = "false"
        createpropertiesfile = "false"
        spliton = "false"
        nopush = "false"
        repo_name = ""
        screenplay = False
        endcommand = ""
        createfiles = ""
        createfilesdirectory = ""
        maxretrytime = 60
        testset = ""
        numtestsets = ""
        testsetnum = ""
        filenames = ""
        printout = "false"
        includefailing = "false"
        convertcucumber = "false"
        mergereports = "false"
        mergefiles = "False"
        fullreportdir = ""
        azureTest = False
        dll = ""
        dlllocation = ""
        vstestlocation = ""
        startTimeRunAll = ""
        # --testsuitesnameseparator and classnameseparator need to be encoded i.e. # is %23

        # Templates
        # sys.argv = args
        # print(sys.argv)
        # print(type(sys.argv))
        try:
            sys.argv = args[0]
            if type(sys.argv) == tuple:
                sys.argv = sys.argv[0]
        except Exception as e:
            print("Starting script execution")
        c = 0
        print("================================================")
        if len(sys.argv) > 1:
            c = len(sys.argv)
            for k in range(1, c):
                if sys.argv[k] == "--runtemplate":
                    runtemplate = sys.argv[k + 1]
                if sys.argv[k] == "--testtemplate":
                    testtemplate = sys.argv[k + 1]
                if sys.argv[k] == "--testtemplatearg1":
                    testtemplatearg1 = sys.argv[k + 1]
                if sys.argv[k] == "--testtemplatearg2":
                    testtemplatearg2 = sys.argv[k + 1]
                if sys.argv[k] == "--testtemplatearg3":
                    testtemplatearg3 = sys.argv[k + 1]
                if sys.argv[k] == "--testtemplatearg4":
                    testtemplatearg4 = sys.argv[k + 1]
                if sys.argv[k] == "--filenames":
                    filenames = "True"

        #####Test Run Templates######

        if runtemplate == "prioritized tests with unassigned":
            teststorun = "high,medium,unassigned"

        if runtemplate == "prioritized tests":
            teststorun = "high,medium,unassigned"

        if runtemplate == "prioritized tests without unassigned":
            teststorun = "high,medium"

        if runtemplate == "prioritized tests with unassigned no execution":
            teststorun = "high,medium,unassigned"
            executetests = "false"

        if runtemplate == "prioritized tests no execution":
            teststorun = "high,medium,unassigned"
            executetests = "false"

        if runtemplate == "prioritized tests without unassigned no execution":
            teststorun = "high,medium"
            executetests = "false"

        if runtemplate == "no tests":
            teststorun = "none"
            fail = "newdefects, reopeneddefects, failedtests, brokentests"
            executetests = "false"

        if runtemplate == "notests":
            teststorun = "none"
            fail = "newdefects, reopeneddefects, failedtests, brokentests"
            executetests = "false"

        if runtemplate == "none":
            teststorun = "none"
            fail = "newdefects, reopeneddefects, failedtests, brokentests"
            executetests = "false"

        if runtemplate == "all tests":
            teststorun = "all"
            fail = "newdefects, reopeneddefects, failedtests, brokentests"

        if runtemplate == "all":
            teststorun = "all"
            fail = "newdefects, reopeneddefects, failedtests, brokentests"

        if runtemplate == "alltests":
            teststorun = "all"
            fail = "newdefects, reopeneddefects, failedtests, brokentests"

        if runtemplate == "top20":
            teststorun = "top20"
            fail = "newdefects, reopeneddefects, failedtests, brokentests"

        if runtemplate == "top20 no execution":
            teststorun = "top20"
            fail = "newdefects, reopeneddefects, failedtests, brokentests"
            executetests = "false"

        if len(sys.argv) > 1:
            for k in range(1, c):
                if sys.argv[k] == "--teststorun":
                    teststorun = sys.argv[k + 1]

        # Template Sahi
        # testsuitename#testname
        # addtestsuitename=true
        # testsuitesnameseparator=%23
        # Sahi Setup
        # testrunner.bat demo/demo.suite http://sahitest.com/demo/ firefox
        # startrun testrunner.bat temp.dd.csv
        # endrun as per setup
        # SET LOGS_INFO=junit:<LOCATION>
        # https://sahipro.com/docs/using-sahi/playback-commandline.html

        # Sahi Ant
        # https://sahipro.com/docs/using-sahi/playback-desktop.html#Playback%20via%20ANT
        # startrun ant -f demo.xml
        # <property name="scriptName" value="demo/ddcsv/temp.dd.csv"/>
        # <report type="junit" logdir="<LOCATION>"/>

        # To run tests with sahi
        # edit testrunner.bat or .sh - add line "SET LOGS_INFO=junit:<Directory of your choice>"
        # startrun = 'testrunner.bat or .sh temp.dd.csv'
        # endrun = ' <additional arguments>'
        # report = directory set when editing the testrunner/index.xml - we only want the index file

        if testtemplate == "sahi ant":
            testseparator = ",,"
            addtestsuitename = "true"
            testsuitesnameseparator = "#"
            generatefile = "sahi"
            startrunall = "ant -f " + testtemplatearg2
            startrunspecific = "ant -f " + testtemplatearg3
            report = testtemplatearg1

        # https://stackoverflow.com/questions/35166214/running-individual-xctest-ui-unit-test-cases-for-ios-apps-from-the-command-li
        if testtemplate == "kif":
            testseparator = " "
            addtestsuitename = "false"
            # testsuitesnameseparator="/"
            prefixtest = "-only-testing:"
            startrunall = "xcodebuild test " + testtemplatearg1
            startrunspecific = "xcodebuild test " + testtemplatearg1
            report = "Test.xml"
            trainer = "true"

        # set endrun to being final command for test runner i.e. browser etccls
        if testtemplate == "sahi testrunner":
            testseparator = ",,"
            addtestsuitename = "true"
            testsuitesnameseparator = "#"
            generatefile = "sahi"
            startrunspecific = "testrunner temp.dd.csv"
            startrunall = "testrunner " + testtemplatearg2
            report = testtemplatearg1

        # set endrun to being final command for test runner i.e. browser etccls
        if testtemplate == "sbt":
            testseparator = "--test "
            addtestsuitename = "true"
            testsuitesnameseparator = "."
            # startrunspecific = "gradle test --test '"
            startrunspecific = "gradle test"
            prefixtest = " --test '"
            postfixtest = "'"
            # endrunspecific = "'"
            startrunall = "gradle test"
            report = "./build/test-results/"
            reporttype = "directory"
            deletereports = "false"

        # https://stackoverflow.com/questions/22505533/how-to-run-only-one-unit-test-class-using-gradle
        if testtemplate == "gradle":
            testseparator = "--test "
            addtestsuitename = "true"
            testsuitesnameseparator = "."
            # startrunspecific = "gradle test --test '"
            startrunspecific = "gradle test"
            prefixtest = " --test '"
            postfixtest = "'"
            # endrunspecific = "'"
            startrunall = "gradle test"
            report = "./build/test-results/"
            reporttype = "directory"
            deletereports = "false"

        # need to set system property in gradle file for test
        # systemProperty("cucumber.filter.name", findProperty("appsurifytests"))
        # command sets appsurifytests which then gets run
        # to rungradlew test -Pappsurifytests=".*another.*"
        if testtemplate == "gradle cucumber":
            testseparator = "|"
            startrunspecific = "gradle test "
            prefixtest = ""
            postfixtest = ""
            # endrunspecific = "'"
            startrunall = "gradle test "
            report = "./build/test-results/"
            reporttype = "directory"
            deletereports = "false"
            endrunspecific = '"'
            endspecificrun = ' -Pappsurifytests="'

        # https://stackoverflow.com/questions/48098352/how-to-run-single-cucumber-scenario-by-name
        if testtemplate == "gradle cucumber old":
            testseparator = "|"
            startrunspecific = "gradle test "
            prefixtest = ""
            postfixtest = ""
            # endrunspecific = "'"
            startrunall = "gradle test "
            report = "./build/test-results/"
            reporttype = "directory"
            deletereports = "false"
            endrunspecific = '"'
            endspecificrun = ' -Pappsurifytests="'

        if testtemplate == "testcafe":
            testseparator = ","
            addtestsuitename = "true"
            testsuitesnameseparator = "#"
            startrunspecific = "mvn test"
            endrunspecific = ""
            startrunall = "mvn test"
            report = "./target/surefire-reports/"
            reporttype = "directory"
            deletereports = "false"
            endspecificrun = " -Dtest="

        # https://jadala-ajay16.medium.com/running-tests-from-command-line-different-options-427a5dadd224
        # https://maven.apache.org/surefire/maven-surefire-plugin/test-mojo.html
        if testtemplate == "mvn old":
            # testseparator = ","
            testseparator = "+"
            # addtestsuitename = "true"
            # testsuitesnameseparator = "#"
            startrunspecific = "mvn test"
            endrunspecific = '"'
            startrunall = "mvn test"
            report = "./target/surefire-reports/"
            reporttype = "directory"
            deletereports = "false"
            endspecificrun = ' -Dtest="#'

        if testtemplate == "mvn":
            testseparator = ","
            addtestsuitename = "true"
            testsuitesnameseparator = "#"
            startrunspecific = "mvn test"
            endrunspecific = ""
            startrunall = "mvn test"
            report = "./target/surefire-reports/"
            reporttype = "directory"
            deletereports = "false"
            endspecificrun = " -Dtest="

        if testtemplate == "printout":
            testseparator = "\n"
            startrunspecific = "mvn test "
            endrunspecific = '" '
            postfixtest = "$'"
            prefixtest = "--name '^"
            startrunall = "mvn test"
            report = "./target/surefire-reports/"
            reporttype = "directory"
            deletereports = "false"
            endspecificrun = ' -Dcucumber.options="'

        if testtemplate == "mvn screenplay":
            testseparator = ","
            addtestsuitename = "true"
            testsuitesnameseparator = "#"
            startrunspecific = "mvn test"
            endrunspecific = ""
            startrunall = "mvn test"
            report = "./target/surefire-reports/"
            reporttype = "directory"
            deletereports = "false"
            endspecificrun = " -Dtest="
            screenplay = True

        if testtemplate == "mvn integration old":
            # testseparator = ","
            testseparator = "+"
            # addtestsuitename = "true"
            # testsuitesnameseparator = "#"
            startrunspecific = "mvn test"
            endrunspecific = '"'
            startrunall = "mvn test"
            report = "./target/surefire-reports/"
            reporttype = "directory"
            deletereports = "false"
            endspecificrun = ' -Dit.test="#'

        if testtemplate == "mvn integration":
            testseparator = ","
            addtestsuitename = "true"
            testsuitesnameseparator = "#"
            startrunspecific = "mvn test"
            endrunspecific = ""
            startrunall = "mvn test"
            report = "./target/surefire-reports/"
            reporttype = "directory"
            deletereports = "false"
            endspecificrun = " -Dit.test="

        if testtemplate == "mvn integration screenplay":
            testseparator = ","
            addtestsuitename = "true"
            testsuitesnameseparator = "#"
            startrunspecific = "mvn test"
            endrunspecific = ""
            startrunall = "mvn test"
            report = "./target/surefire-reports/"
            reporttype = "directory"
            deletereports = "false"
            endspecificrun = " -Dit.test="
            screenplay = True

        if testtemplate == "webdriverio mocha":
            testseparator = "|"
            reporttype = "file"
            report = "test-results.xml"
            startrunspecific = "wdio "
            endrunspecific = "'"
            postfixtest = "$"
            prefixtest = "^"
            startrunall = "wdio test "
            webdriverio = "true"
            endspecificrun = " -g '"

        # behave
        # https://behave.readthedocs.io/en/latest/behave.html?highlight=command#command-line-arguments

        # https://www.npmjs.com/package/jest-junit
        # https://jestjs.io/docs/cli#--testnamepatternregex
        if testtemplate == "jest":
            testseparator = "|"
            reporttype = "file"
            report = "test-results.xml"
            startrunspecific = "wdio  -g '"
            endrunspecific = "'"
            postfixtest = ""
            prefixtest = ""
            startrunall = "wdio test "
            endspecificrun = " -g '"

        # protractor - https://stackoverflow.com/questions/24536572/how-to-run-a-single-specific-test-case-when-using-protractor
        # https://github.com/angular/protractor/issues/164
        
        if testtemplate == "cucumber mvn":
            testseparator = " "
            startrunspecific = "mvn test "
            endrunspecific = '" '
            postfixtest = "$'"
            prefixtest = "--name '^"
            startrunall = "mvn test"
            report = "./target/surefire-reports/"
            reporttype = "directory"
            deletereports = "false"
            endspecificrun = ' -Dcucumber.options="'

        #startrunspecific
                #+ startrunpostfix
                #+ testlist
                #+ endrunprefix
                #+ endrunspecific
                #+ endrunpostfix

                #-Dcucumber.filter.name="REGEXP"
        #https://github.com/cucumber/cucumber-jvm/tree/main/cucumber-core#properties-environment-variables-system-options

        # mvn test -Dcucumber.options="--name 'another scenario' --name '^a few cukes$'"
        if testtemplate == "cucumber6 mvn":
            testseparator = "|"
            startrunspecific = 'mvn test '
            endrunspecific = '" '
            postfixtest = "$"
            prefixtest = "^"
            startrunall = "mvn test"
            report = "./target/surefire-reports/"
            reporttype = "directory"
            deletereports = "false"
            endspecificrun = ' -Dcucumber.filter.name="'

        if testtemplate == "cucumber6mvn":
            testseparator = "|"
            startrunspecific = 'mvn test '
            endrunspecific = '" '
            postfixtest = "$"
            prefixtest = "^"
            startrunall = "mvn test"
            report = "./target/surefire-reports/"
            reporttype = "directory"
            deletereports = "false"
            endspecificrun = ' -Dcucumber.filter.name="'

        if testtemplate == "cucumber protractor":
            testseparator = " "
            startrunspecific = "mvn test "
            endrunspecific = '" '
            postfixtest = "$'"
            prefixtest = "--name '^"
            startrunall = "mvn test"
            report = "./target/surefire-reports/"
            reporttype = "directory"
            deletereports = "false"
            endspecificrun = ' -Dcucumber.options="'

        if testtemplate == "rspec":
            testseparator = " "
            startrunspecific = "rspec --format RspecJunitFormatter --out rspec.xml "
            prefixtest = "-e '"
            postfixtest = "'"
            startrunall = "rspec --format RspecJunitFormatter --out rspec.xml"
            reporttype = "file"
            report = "rspec.xml"
            endspecificrun = " "

        # startrun should be how your tests are executed i.e. java -jar robotframework.jar or robot
        # then -x robot.xml to create the output file
        # then --test ' if you are running specific tests
        # endrun should be the location of your tests
        if testtemplate == "robotframework":
            prefixtest = " --test '"
            postfixtest = "'"
            testseparator = " "
            reporttype = "file"
            report = testtemplatearg3
            startrunall = testtemplatearg1 + " -x " + testtemplatearg3 + " "
            endrunall = testtemplatearg2
            startrunspecific = testtemplatearg1 + " -x " + testtemplatearg3 + " "
            endrunall = testtemplatearg2
            endspecificrun = " "

        # mocha
        # install https://www.npmjs.com/package/mocha-junit-reporter
        # https://github.com/mochajs/mocha/issues/1565
        if testtemplate == "mocha":
            testseparator = "|"
            reporttype = "file"
            report = "test-results.xml"
            startrunspecific = "mocha test --reporter mocha-junit-reporter"
            endrunspecific = "'"
            postfixtest = "$"
            prefixtest = "^"
            startrunall = "mocha test --reporter mocha-junit-reporter "
            endspecificrun = " -g '"

        # pytest
        # https://stackoverflow.com/questions/36456920/is-there-a-way-to-specify-which-pytest-tests-to-run-from-a-file
        if testtemplate == "pytest":
            testseparator = " or "
            reporttype = "file"
            report = "test-results.xml"
            startrunspecific = "python -m pytest --junitxml=test-results.xml"
            endrunspecific = "'"
            startrunall = "python -m pytest --junitxml=test-results.xml"
            endspecificrun = " -k '"

        # testim
        # https://help.testim.io/docs/the-command-line-cli
        if testtemplate == "testim":
            testseparator = " --name '"
            reporttype = "file"
            report = "test-results.xml"
            startrunspecific = "testim --report-file test-results.xml"
            postfixtest = "'"
            startrunall = "testim --report-file test-results.xml"
            endspecificrun = " --name '"

        # testcomplete
        # TestComplete.exe "C:\My Projects\MySuite.pjs" /run /p:MyProj /ExportSummary:"C:\TestLogs\report.xml"
        # /test""ProjectTestItem1"
        # https://support.smartbear.com/testcomplete/docs/working-with/automating/command-line-and-exit-codes/command-line.html
        if testtemplate == "testcomplete":
            testseparator = "|"
            reporttype = "file"
            report = testtemplatearg2
            startrunspecific = "TestComplete.exe " + testtemplatearg1 + " "
            endrunspecific = testtemplatearg2
            startrunall = "TestComplete.exe " + testtemplatearg1 + " "
            endrunall = +" /ExportSummary:" + testtemplatearg2
            endspecificrun = " "
            prefixtest = '/test"'
            postfixtest = '"'

        # ranorex webtestit
        # https://discourse.webtestit.com/t/running-ranorex-webtestit-in-cli-mode/152
        if testtemplate == "ranorex webtestit":
            testseparator = "|"
            reporttype = "file"
            report = testtemplatearg2
            startrunspecific = "TestComplete.exe " + testtemplatearg1 + " "
            endrunspecific = testtemplatearg2
            startrunall = "TestComplete.exe " + testtemplatearg1 + " "
            endrunall = +" /ExportSummary:" + testtemplatearg2

        # cypress
        # https://github.com/bahmutov/cypress-select-tests
        # cypress run --reporter junit --reporter-options mochaFile=result.xml
        # updated to https://github.com/cypress-io/cypress-grep
        if testtemplate == "cypress":
            testseparator = "; "
            reporttype = "file"
            report = "results.xml"
            startrunspecific = (
                "cypress run --reporter junit --reporter-options mochaFile=result.xml"
            )
            endrunspecific = '"'
            postfixtest = ""
            prefixtest = ""
            startrunall = (
                "cypress run --reporter junit --reporter-options mochaFile=result.xml"
            )
            endspecificrun = ' --env grep="'

        if testtemplate == "cypress update":
            addtestsuitename = "true"
            testsuitesnameseparator = ";"
            testseparator = "; "
            reporttype = "file"
            report = "results.xml"
            startrunspecific = (
                "cypress run --reporter junit --reporter-options mochaFile=result.xml"
            )
            endrunspecific = '"'
            postfixtest = ""
            prefixtest = ""
            startrunall = (
                "cypress run --reporter junit --reporter-options mochaFile=result.xml"
            )
            endspecificrun = ' --env grep="'
            escapetests = "true"

        if testtemplate == "cypress inquirer":
            addtestsuitename = "true"
            testsuitesnameseparator = ";"
            testseparator = "; "
            reporttype = "file"
            report = "results.xml"
            startrunspecific = (
                "cypress run --reporter junit --reporter-options mochaFile=result.xml"
            )
            endrunspecific = '"'
            postfixtest = ""
            prefixtest = ""
            startrunall = (
                "cypress run --reporter junit --reporter-options mochaFile=result.xml"
            )
            endspecificrun = ' --env grep="'
            escapetests = "true"

        if testtemplate == "cypress update include env":
            addtestsuitename = "true"
            testsuitesnameseparator = ";"
            testseparator = "; "
            reporttype = "file"
            report = "results.xml"
            startrunspecific = (
                "cypress run --reporter junit --reporter-options mochaFile=result.xml"
            )
            endrunspecific = '"'
            postfixtest = ""
            prefixtest = ""
            startrunall = (
                "cypress run --reporter junit --reporter-options mochaFile=result.xml"
            )
            endspecificrun = ' grep="'

        if testtemplate == "cypress json":
            addtestsuitename = "true"
            testsuitesnameseparator = ";"
            testseparator = ","
            reporttype = "file"
            report = "results.xml"
            startrunspecific = (
                "cypress run --reporter junit --reporter-options mochaFile=result.xml"
            )
            endrunspecific = "}'"
            postfixtest = '"'
            prefixtest = '"'
            startrunall = (
                "cypress run --reporter junit --reporter-options mochaFile=result.xml"
            )
            endspecificrun = '"grep":'

        if testtemplate == "cypress circleci":
            testseparator = "; "
            reporttype = "file"
            report = "results.xml"
            startrunspecific = (
                "cypress run --reporter junit --reporter-options mochaFile=result.xml"
            )
            endrunspecific = '"'
            postfixtest = ""
            prefixtest = ""
            startrunall = (
                "cypress run --reporter junit --reporter-options mochaFile=result.xml"
            )
            endspecificrun = ' --env grep="'

        if testtemplate == "cypress filenames":
            testseparator = ", "
            filenames = "True"
            reporttype = "file"
            report = "results.xml"
            startrunspecific = (
                "cypress run --reporter junit --reporter-options mochaFile=result.xml"
            )
            endrunspecific = '"'
            postfixtest = ""
            prefixtest = ""
            startrunall = (
                "cypress run --reporter junit --reporter-options mochaFile=result.xml"
            )
            endspecificrun = ' --spec"'

        # mstest
        # /Tests:TestMethod1,testMethod2
        # mstest.exe"  /testcontainer:"%WORKSPACE%\MYPROJECT\bin\debug\MYTEST.dll" /test:"ABC" /resultsfile:"%WORKSPACE%\result_%BUILD_NUMBER%.xml"
        if testtemplate == "mstest":
            testseparator = ","
            reporttype = "file"
            startrunspecific = (
                "mstest /resultsfile:'"
                + testtemplatearg1
                + "' /testcontainer:'"
                + testtemplatearg2
                + "'"
                + "/tests:"
            )
            postfixtest = "'"
            prefixtest = "'"
            startrunall = (
                "mstest /resultsfile:'"
                + testtemplatearg1
                + "' /testcontainer:'"
                + testtemplatearg2
                + "'"
            )
            report = testtemplatearg1
            importtype = "trx"
            endspecificrun = " /tests:"

        # vstest
        # /Tests:TestMethod1,testMethod2
        # vstest.console.exe"  /testcontainer:"%WORKSPACE%\MYPROJECT\bin\debug\MYTEST.dll" /test:"ABC" /resultsfile:"%WORKSPACE%\result_%BUILD_NUMBER%.xml"
        if testtemplate == "vstest":
            testseparator = ","
            reporttype = "file"
            startrunspecific = (
                "vstest.console.exe /resultsfile:'"
                + testtemplatearg1
                + "' /testcontainer:'"
                + testtemplatearg2
                + "'"
                + "/tests:"
            )
            postfixtest = "'"
            prefixtest = "'"
            startrunall = (
                "vstest.console.exe /resultsfile:'"
                + testtemplatearg1
                + "' /testcontainer:'"
                + testtemplatearg2
                + "'"
            )
            report = testtemplatearg1
            importtype = "trx"
            endspecificrun = " /tests:"

        # vstest
        # /Tests:TestMethod1,testMethod2
        # vstest.console.exe"  /testcontainer:"%WORKSPACE%\MYPROJECT\bin\debug\MYTEST.dll" /test:"ABC" /resultsfile:"%WORKSPACE%\result_%BUILD_NUMBER%.xml"
        if testtemplate == "nunit":
            testseparator = ","
            reporttype = "file"
            startrunspecific = (
                "nunit.console.exe /resultsfile:'"
                + testtemplatearg1
                + "' /testcontainer:'"
                + testtemplatearg2
                + "'"
                + "/tests:"
            )
            postfixtest = "'"
            prefixtest = "'"
            startrunall = (
                "nunit.console.exe /resultsfile:'"
                + testtemplatearg1
                + "' /testcontainer:'"
                + testtemplatearg2
                + "'"
            )
            report = testtemplatearg1
            endspecificrun = " /tests:"

        # Name=IbsAlarmAudioDeterminerIsAudioOffTest\(RedAlarm,Off,True,True\)|Name=IbsAlarmAudioDeterminerIsAudioOffTest\(RedAlarm,Off,False,False\)
        # https://github.com/microsoft/vstest-docs/blob/master/docs/filter.md
        # https://stackoverflow.com/questions/38139803/using-vstest-console-exe-testcategory-with-equals-and-not-equals
        if testtemplate == "azure dotnet":
            encodetests = "true"
            executetests = "false"
            testseparator = "|"
            reporttype = "file"
            startrunspecific = (
                "vstest.console.exe /resultsfile:'"
                + testtemplatearg1
                + "' /testcontainer:'"
                + testtemplatearg2
                + "'"
                + '/TestCaseFilter:"'
            )
            endrunspecific = '"'
            postfixtest = ""
            prefixtest = "Name="
            startrunall = (
                "vstest.console.exe /resultsfile:'"
                + testtemplatearg1
                + "' /testcontainer:'"
                + testtemplatearg2
                + "'"
            )
            report = testtemplatearg1
            importtype = "trx"
            endspecificrun = " /tests:"

        if testtemplate == "azure specflow":
            encodetests = "true"
            executetests = "false"
            testseparator = "|"
            reporttype = "file"
            startrunspecific = (
                "vstest.console.exe /resultsfile:'"
                + testtemplatearg1
                + "' /testcontainer:'"
                + testtemplatearg2
                + "'"
                + '/TestCaseFilter:"'
            )
            endrunspecific = '"'
            postfixtest = ""
            prefixtest = "Name="
            startrunall = (
                "vstest.console.exe /resultsfile:'"
                + testtemplatearg1
                + "' /testcontainer:'"
                + testtemplatearg2
                + "'"
            )
            report = testtemplatearg1
            importtype = "trx"
            replaceretry = "true"
            endspecificrun = " /tests:"
            azurevariablenum = 1

        if testtemplate == "azure xunit":
            encodetests = "true"
            executetests = "false"
            testseparator = "|"
            reporttype = "file"
            startrunspecific = (
                "vstest.console.exe /resultsfile:'"
                + testtemplatearg1
                + "' /testcontainer:'"
                + testtemplatearg2
                + "'"
                + '/TestCaseFilter:"'
            )
            endrunspecific = '"'
            postfixtest = ""
            prefixtest = "DisplayName="
            startrunall = (
                "vstest.console.exe /resultsfile:'"
                + testtemplatearg1
                + "' /testcontainer:'"
                + testtemplatearg2
                + "'"
            )
            report = testtemplatearg1
            importtype = "trx"
            replaceretry = "true"
            endspecificrun = " /tests:"
            azurevariablenum = 1
            spliton = ","

        # Jasmine3
        # npm install -g jasmine-xml-reporter for jasmine 2.x then use --junitreport and --output to determine where to output the report.
        # npm install -g jasmine-junit-reporter requires jasmine --reporter=jasmine-junit-reporter creates file junit_report
        if testtemplate == "jasmine":
            testseparator = "|"
            reporttype = "file"
            report = "junit_report.xml"
            startrunspecific = "jasmine --reporter=jasmine-junit-reporter"
            endrunspecific = "'"
            postfixtest = "$"
            prefixtest = "^"
            startrunall = "jasmine test --reporter=jasmine-junit-reporter "
            endspecificrun = "  --filter='"

        # add reporter - https://playwright.dev/docs/test-reporters
        if testtemplate == "playwright net":
            testseparator = "|"
            reporttype = "file"
            report = "test-results.xml"
            startrunspecific = "playwright test "
            endrunspecific = "'"
            postfixtest = "$"
            prefixtest = "^"
            startrunall = "playwright test "
            endspecificrun = " -g '"

        # add reporter - https://playwright.dev/docs/test-reporters
        if testtemplate == "playwright node":
            testseparator = "|"
            reporttype = "file"
            report = "test-results.xml"
            startrunspecific = "playwright test "
            endrunspecific = "'"
            postfixtest = "$"
            prefixtest = "^"
            startrunall = "playwright test "
            endspecificrun = " -g '"

        # add reporter - https://playwright.dev/docs/test-reporters
        if testtemplate == "playwright java":
            testseparator = ","
            addtestsuitename = "true"
            testsuitesnameseparator = "#"
            startrunspecific = "mvn"
            endrunspecific = " test"
            startrunall = "mvn test"
            report = "./target/surefire-reports/"
            reporttype = "directory"
            deletereports = "false"
            endspecificrun = " -Dtest="

        # add reporter - https://playwright.dev/docs/test-reporters
        # if testtemplate == "playwright python":
        #    testseparator = "|"
        #    reporttype = "file"
        #    report = "test-results.xml"
        #    startrunspecific = "playwright test "
        #    endrunspecific = "'"
        #    postfixtest = "$"
        #    prefixtest = "^"
        #    startrunall = "playwright test "
        #    endspecificrun = " -g '"

        # pytest
        # https://stackoverflow.com/questions/36456920/is-there-a-way-to-specify-which-pytest-tests-to-run-from-a-file
        if testtemplate == "playwright python":
            testseparator = " or "
            reporttype = "file"
            report = "test-results.xml"
            startrunspecific = "python -m pytest --junitxml=test-results.xml"
            endrunspecific = "'"
            startrunall = "python -m pytest --junitxml=test-results.xml"
            endspecificrun = " -k '"

        # tosca
        # https://support.tricentis.com/community/article.do?number=KB0013693
        # https://documentation.tricentis.com/en/1000/content/continuous_integration/execution.htm
        # https://documentation.tricentis.com/en/1030/content/continuous_integration/configuration.htm
        # testset = https://documentation.tricentis.com/en/1010/content/tchb/tosca_executor.htm

        # katalon
        # katalonc -noSplash -runMode=console -projectPath="C:\Katalon\Test\Test Project\Test Project.prj" -retry=0 -testSuitePath="Test Suites/New Test Suite"
        # -executionProfile="default" -browserType="Chrome" -apiKey="ee04de44-b3c7-4c9e-b8cd-741157fd4324" -reportFolder="c:\katalon" -reportFileName="report"
        # JUnit_Report.xml gets generated
        # Has apiKey - https://forum.katalon.com/t/how-to-use-katalon-plugin-for-jenkins-on-windows/20326/3
        # -projectPath=<path>	Specify the project location (include .prj file). The absolute path must be used in this case.	Y
        # -testSuitePath=<path>	Specify the test suite file (without extension .ts). The relative path (root being project folder) must be used in this case.
        # -reportFolder=<path>	Specify the destination folder for saving report files. Can use absolute path or relative path (root being project folder).	N
        # -reportFileName=<name>	Specify the name for report files (.html, .csv, .log). If not provide, system uses the name "report" (report.html, report.csv, report.log). This option is only taken into account when being used with "-reportFolder" option.
        if testtemplate == "katalon":
            testseparator = ",,"
            reporttype = "file"
            report = testtemplatearg1
            head_tail = os.path.split(testtemplatearg1)
            report_folder = head_tail[0]
            report_file = head_tail[1]
            head_tail = os.path.split(testtemplatearg3)
            startrunspecific = (
                "katalonc -noSplash -runMode=console -projectPath='"
                + testtemplatearg2
                + "' -testSuitePath='"
                + "'"
                + os.path.join(head_tail[0], "temp.ts")
                + "' -apiKey='"
                + testtemplatearg4
                + "' -reportFolder='"
                + report_folder
                + " -reportFileName='"
                + report_file
                + "'"
            )
            startrunall = (
                "katalonc -noSplash -runMode=console -projectPath='"
                + testtemplatearg2
                + "' -testSuitePath='"
                + "'"
                + testtemplatearg3
                + "' -apiKey='"
                + testtemplatearg4
                + "' -reportFolder='"
                + report_folder
                + " -reportFileName='"
                + report_file
                + "'"
            )
            # endspecificrun = "  --filter='"
            generatefile = "katalon"

        # opentest
        # testtemplatearg1 = report
        # testtemplatearg2 = template of template with no tests
        # testtemplatearg3 = template with all tests
        if testtemplate == "opentest":
            testseparator = ",,"
            reporttype = "file"
            report = testtemplatearg1
            source = testtemplatearg2
            full_path = os.path.realpath(source)
            destination = os.path.join(os.path.dirname(full_path), "temp.yaml")
            startrunspecific = (
                "opentest session create --out '"
                + testtemplatearg1
                + "' --template '"
                + destination
                + "' "
            )
            startrunall = (
                "opentest session create --out '"
                + testtemplatearg1
                + "' --template '"
                + testtemplatearg3
                + "' "
            )
            generatefile = "opentest"

        if filenames == "True":
            addtestsuitename = "false"
            addclassname = "false"
            testsuitesnameseparator = ""
            classnameseparator = ""
            testseparator = ","
            prefixtest = ""
            postfixtest = ""

        # Todo
        # mstest
        # nunit
        # xunit
        # gradle/ant?
        # c?
        # c++
        # clojure
        # eunit
        # go
        # haskell
        # javascript
        # objective c
        # perl
        # php
        # scala
        # swift
        # htmlunit
        # ranorex
        # qmetry
        # leapwork
        # experitest
        # katalon
        # testsigma - currently not possible
        # lambdatest
        # smartbear crossbrowsertesting
        # uft
        # telerik test studio
        # perfecto
        # tosca test suite
        # mabl - currently not possible
        # test craft
        # squish
        # test cafe

        if len(sys.argv) > 1:
            for k in range(1, c):
                if sys.argv[k] == "--url":
                    url = sys.argv[k + 1]
                if sys.argv[k] == "--apikey":
                    apikey = sys.argv[k + 1]
                if sys.argv[k] == "--project":
                    project = sys.argv[k + 1]
                if sys.argv[k] == "--testsuite":
                    testsuite = sys.argv[k + 1]
                if sys.argv[k] == "--report":
                    report = sys.argv[k + 1].strip()
                if sys.argv[k] == "--reporttype":
                    reporttype = sys.argv[k + 1]
                if sys.argv[k] == "--teststorun":
                    teststorun = sys.argv[k + 1]
                if sys.argv[k] == "--importtype":
                    importtype = sys.argv[k + 1]
                if sys.argv[k] == "--addtestsuitename":
                    addtestsuitename = sys.argv[k + 1]
                if sys.argv[k] == "--testsuitesnameseparator":
                    testsuitesnameseparator = sys.argv[k + 1]
                if sys.argv[k] == "--addclassname":
                    addclassname = sys.argv[k + 1]
                if sys.argv[k] == "--classnameseparator":
                    classnameseparator = sys.argv[k + 1]
                if sys.argv[k] == "--rerun":
                    rerun = sys.argv[k + 1]
                if sys.argv[k] == "--maxrerun":
                    maxrerun = sys.argv[k + 1]
                if sys.argv[k] == "--failfast":
                    failfast = sys.argv[k + 1]
                if sys.argv[k] == "--fullname":
                    fullname = sys.argv[k + 1]
                if sys.argv[k] == "--fullnameseparator":
                    fullnameseparator = sys.argv[k + 1]
                if sys.argv[k] == "--startrunall":
                    startrunall = sys.argv[k + 1]
                if sys.argv[k] == "--startrunspecific":
                    startrunspecific = sys.argv[k + 1]
                if sys.argv[k] == "--prefixtest":
                    prefixtest = sys.argv[k + 1]
                if sys.argv[k] == "--postfixtest":
                    postfixtest = sys.argv[k + 1]
                if sys.argv[k] == "--testseparator":
                    testseparator = sys.argv[k + 1]
                if sys.argv[k] == "--testseparatorend":
                    testseparatorend = sys.argv[k + 1]
                if sys.argv[k] == "--endrunspecific":
                    endrunspecific = sys.argv[k + 1]
                if sys.argv[k] == "--endrunall":
                    endrunall = sys.argv[k + 1]
                if sys.argv[k] == "--additionalargs":
                    additionalargs = sys.argv[k + 1]
                if sys.argv[k] == "--fail":
                    fail = sys.argv[k + 1]
                if sys.argv[k] == "--commit":
                    commit = sys.argv[k + 1]
                if sys.argv[k] == "--branch":
                    branch = sys.argv[k + 1]
                if sys.argv[k] == "--maxtests":
                    maxtests = int(sys.argv[k + 1])
                if sys.argv[k] == "--scriptlocation":
                    scriptlocation = sys.argv[k + 1]
                if sys.argv[k] == "--runfrequency":
                    runfrequency = sys.argv[k + 1]
                if sys.argv[k] == "--fromcommit":
                    fromcommit = sys.argv[k + 1]
                if sys.argv[k] == "--repository":
                    repository = sys.argv[k + 1]
                if sys.argv[k] == "--generatefile":
                    generatefile = sys.argv[k + 1]
                if sys.argv[k] == "--startrunpostfix":
                    startrunpostfix = sys.argv[k + 1]
                if sys.argv[k] == "--endrunprefix":
                    endrunprefix = sys.argv[k + 1]
                if sys.argv[k] == "--endrunpostfix":
                    endrunpostfix = sys.argv[k + 1]
                if sys.argv[k] == "--proxy":
                    proxy = sys.argv[k + 1]
                if sys.argv[k] == "--username":
                    username = sys.argv[k + 1]
                if sys.argv[k] == "--password":
                    password = sys.argv[k + 1]
                if sys.argv[k] == "--executetests":
                    executetests = sys.argv[k + 1]
                if sys.argv[k] == "--trainer":
                    trainer = "true"
                if sys.argv[k] == "--azurevariable":
                    azure_variable = sys.argv[k + 1]
                if sys.argv[k] == "--pipeoutput":
                    pipeoutput = "true"
                if sys.argv[k] == "--bitrise":
                    bitrise = "true"
                if sys.argv[k] == "--recursive":
                    recursive = "true"
                if sys.argv[k] == "--replaceretry":
                    replaceretry = "true"
                if sys.argv[k] == "--githubactionsvariable":
                    githubactionsvariable = sys.argv[k + 1]
                if sys.argv[k] == "--circlecivariable":
                    circlecivariable = sys.argv[k + 1]
                if sys.argv[k] == "--circlecivariablenobash":
                    circlecivariablenobash = sys.argv[k + 1]
                if sys.argv[k] == "--executioncommand":
                    executioncommand = sys.argv[k + 1]
                if sys.argv[k] == "--printcommand":
                    printcommand = sys.argv[k + 1]
                if sys.argv[k] == "--azurefilter":
                    azurefilter = sys.argv[k + 1]
                if sys.argv[k] == "--azurefilteronall":
                    azurefilteronall = "false"
                if sys.argv[k] == "--percentage":
                    percentage = sys.argv[k + 1]
                if sys.argv[k] == "--percent":
                    percentage = sys.argv[k + 1]
                if sys.argv[k] == "--weekendrunall":
                    weekendrunall = "true"
                if sys.argv[k] == "--includefailing":
                    includefailing = "true"
                if sys.argv[k] == "--daysrunall":
                    daysrunall = sys.argv[k + 1].lower()
                if sys.argv[k] == "--newdays":
                    newdays = sys.argv[k + 1]
                if sys.argv[k] == "--azurevariablenum":
                    azurevariablenum = sys.argv[k + 1]
                if sys.argv[k] == "--alwaysrun":
                    alwaysrun = sys.argv[k + 1]
                    if alwaysrun.lower() != "none":
                        alwaysrunset = [x.strip() for x in alwaysrun.split(",")]
                if sys.argv[k] == "--azurealwaysrun":
                    azurealwaysrun = sys.argv[k + 1]
                    print("setting azurealwaysrun")
                    if azurealwaysrun.lower() != "none":
                        azurealwaysrunset = [
                            x.strip() for x in azurealwaysrun.split(",")
                        ]
                        print(azurealwaysrunset)
                if sys.argv[k] == "--runcommand":
                    commandset = sys.argv[k + 1]
                    startrunall = sys.argv[k + 1]
                    startrunspecific = sys.argv[k + 1] + endspecificrun
                    # print("fall back command = " + startrunall)
                    # print("prioritized run = " + startrunspecific)
                if sys.argv[k] == "--endcommand":
                    endcommand = sys.argv[k + 1]
                    # print("fall back command = " + startrunall)
                    # print("prioritized run = " + startrunspecific)
                # if sys.argv[k] == "--runnewtests":
                #    runnewtests = sys.argv[k+1]
                if sys.argv[k] == "--noupload":
                    upload = "false"
                if sys.argv[k] == "--createpropertiesfile":
                    createpropertiesfile = "true"
                if sys.argv[k] == "--createfile":
                    createfile = "true"
                if sys.argv[k] == "--createfiles":
                    createfiles = sys.argv[k + 1]
                if sys.argv[k] == "--createfilesdirectory":
                    createfilesdirectory = sys.argv[k + 1]
                if sys.argv[k] == "--nopush":
                    nopush = "true"
                if sys.argv[k] == "--spliton":
                    spliton = sys.argv[k + 1]
                if sys.argv[k] == "--repo_name":
                    repo_name = sys.argv[k + 1]
                if sys.argv[k] == "--maxretrytime":
                    maxretrytime = sys.argv[k + 1]
                if sys.argv[k] == "--testsetnum":
                    testsetnum = sys.argv[k + 1]
                if sys.argv[k] == "--numtestsets":
                    numtestsets = sys.argv[k + 1]
                if sys.argv[k] == "--filenames":
                    filenames = "True"
                if sys.argv[k] == "--printout":
                    printout = "True"
                if sys.argv[k] == "--convertcucumber":
                    convertcucumber = "True"
                if sys.argv[k] == "--mergereports":
                    mergereports = "True"
                if sys.argv[k] == "--mergefiles":
                    mergefiles = "True"
                if sys.argv[k] == "--fullreportdir":
                    fullreportdir = sys.argv[k + 1]
                if sys.argv[k] == "--azuretest":
                    azureTest = True
                if sys.argv[k] == "--dll":
                    dll = sys.argv[k + 1]
                    azureTest = True
                if sys.argv[k] == "--dlllocation":
                    dlllocation = sys.argv[k + 1]
                if sys.argv[k] == "--vstestlocation":
                    vstestlocation = sys.argv[k + 1]
                if sys.argv[k] == "--starttimerunall":
                    startTimeRunAll = sys.argv[k + 1]    

                if sys.argv[k] == "--help":
                    echo(
                        "please see url for more details on this script and how to execute your tests with appsurify - https://github.com/Appsurify/AppsurifyScriptInstallation"
                    )

        if commandset == "":
            startrunspecific = startrunspecific + endspecificrun
            print("################################################")
            # print("prioritized run = " + startrunspecific)

        if endcommand != "":
            endrunpostfix = endcommand

        if printout == "True":
            testseparator = testseparator + "\n"

        if githubactionsvariable != "" and githubactionsvariable is not None:
            executioncommand = (
                'echo "{githubactionsvariable}={[[teststorun]]}" >> $GITHUB_ENV'
            )
            printcommand = '"{githubactionsvariable}={[[teststorun]]}" >> $GITHUB_ENV'

        if circlecivariable != "" and circlecivariable is not None:
            executioncommand = (
                'echo \'export {circlecivariable}="[[teststorun]]"\' >> "$BASH_ENV"'
            )
            printcommand = (
                'echo \'export {circlecivariable}="[[teststorun]]"\' >> "$BASH_ENV"'
            )

        if circlecivariablenobash != "" and circlecivariablenobash is not None:
            executioncommand = (
                "echo 'export {circlecivariablenobash}=\"[[teststorun]]\"'"
            )
            printcommand = "echo 'export {circlecivariablenobash}=\"[[teststorun]]\"'"

        if "http://" in proxy:
            proxy = proxy.replace("http://", "")

        if "https://" in proxy:
            proxy = proxy.replace("https://", "")

        if url[-1:] == "/":
            url = url[:-1]
            echo("url = " + url)

        if repository == "p4":
            repository = "perforce"

        if report[-4:].find(".") >= 0:
            reporttype = "file"
        else:
            reporttype = "directory"

        if len(sys.argv) > 1:
            for k in range(1, c):
                if sys.argv[k] == "--reporttype":
                    reporttype = sys.argv[k + 1]

        testsuiteencoded = urlencode(testsuite)
        projectencoded = urlencode(project)
        testsuiteencoded = testsuite
        projectencoded = project

        # if commit == "" and repository == "git":
        #    commit = runcommand('git log -1 --pretty="%H"')
        #    commit = commit.rstrip().rstrip("\n\r")
        #    print(("commit id = " + commit))

        # git branch | grep \* | cut -d ' ' -f2
        # git rev-parse --abbrev-ref HEAD
        # https://stackoverflow.com/questions/6245570/how-to-get-the-current-branch-name-in-git

        # if branch == "" and repository == "git":
        #    branch = runcommand("git rev-parse --abbrev-ref HEAD").rstrip("\n\r").rstrip()
        #    print(("branch = " + branch))

        if url == "":
            echo("no url specified")
            exit(1)
        if apikey == "":
            echo("no apikey specified")
        if project == "":
            echo("no project specified")
            exit(1)
        if testsuite == "":
            echo("no testsuite specified")
            exit(1)
        if report == "":
            echo("no report specified")
            exit(1)
        if runfrequency == "betweeninclusive" and fromcommit == "":
            echo("no from commit specified and runfrequency set to betweeninclusive")
            exit(1)
        if runfrequency == "betweenexclusive" and fromcommit == "":
            echo("no from commit specified and runfrequency set to betweenexclusive")
            exit(1)
        # if runfrequency != "single" and branch == "":
        if branch == "":
            echo("no branch specified")
            exit(1)
        if commit == "":
            setVariables()
            echo("no commit specified")
            exit(1)

        if startrunspecific == "" and teststorun != "all":
            if teststorun != "none":
                echo("startrunspecific needs to be set in order to execute tests")
                exit(1)
        if startrunall == "" and teststorun == "all":
            echo("startrunall needs to be set in order to execute tests")
            exit(1)
        if startrunspecific == "" and teststorun == "all" and rerun == "true":
            echo(
                "startrunspecific needs to be set in order to rerun tests, either set rerun to false or set startrunspecific"
            )
            exit(1)

        # if [[ $teststorun == "" ]] ; then echo "no teststorun specified" ; exit 1 ; fi
        # if [[ $startrun == "" ]] ; then echo "no command used to start running tests specified" ; exit 1 ; fi

        ####example RunTestsWithAppsurify.sh --url "http://appsurify.dev.appsurify.com" --apikey "MTpEbzhXQThOaW14bHVQTVdZZXNBTTVLT0xhZ00" --project "Test" --testsuite "Test" --report "report" --teststorun "all" --startrun "mvn -tests"
        # example RunTestsWithAppsurify.sh --url "http://appsurify.dev.appsurify.com" --apikey "MTpEbzhXQThOaW14bHVQTVdZZXNBTTVLT0xhZ00" --project "Test" --testsuite "Test" --report "report" --teststorun "all" --startrun "C:\apache\apache-maven-3.5.0\bin\mvn tests "
        # ./RunTestsWithAppsurify.sh --url "https://demo.appsurify.com" --apikey "MTU6a3Q1LUlTU3ZEcktFSTFhQUNoYy1DU3pidkdz" --project "Spirent Demo" --testsuite "Unit" --report "c:\testresults\GroupedTests1.xml" --teststorun "all" --commit "44e9b51296e41e044e45b81e0ef65e9dc4c3bc23"
        # python3 RunTestsWithAppsurify3.py --url "http://appsurify.dev.appsurify.com" --apikey "MTpEbzhXQThOaW14bHVQTVdZZXNBTTVLT0xhZ00" --project "Test" --testsuite "Test" --runtemplate "no tests" --testtemplate "mvn"

        # run_id=""

        # $url $apiKey $project $testsuite $fail $additionalargs $endrun $testseparator $postfixtest $prefixtest $startrun $fullnameseparator $fullname $failfast $maxrerun $rerun $importtype $teststorun $reporttype $report $commit $run_id
        # if repo_name != "":
        #    print("Uploading results")
        #    from time import sleep
        #    sleep(30)
        #    print("Upload completed")
        #    return
        # print("Uploading results3")

        echo("Getting tests to run")

        valuetests = ""
        finalTestNames = ""
        testsrun = ""
        # print("test to run = " + teststorun)
        if teststorun == "all":
            execute_tests("", 0)
            # testsrun="all"

        if teststorun == "none":
            testsrun = "none"
            if nopush == "false":
                push_results()

        testtypes = []

        if percentage.isnumeric():
            testtypes.append(9)
        else:
            if "high" in teststorun:
                testtypes.append(1)
            if "medium" in teststorun:
                testtypes.append(2)
            if "low" in teststorun:
                testtypes.append(3)
            if "unassigned" in teststorun:
                testtypes.append(4)
            if "top20" in teststorun:
                testtypes.append(8)

        if runnewtests != "false":
            testtypes.append(11)

        weekno = datetime.datetime.today().weekday()
        if (
            teststorun != "all"
            and teststorun != "none"
            and weekendrunall == "true"
            and weekno >= 5
        ):
            print("Weekend running all tests")
            testtypes = []

        daysofweek = {
            0: "monday",
            1: "tuesday",
            2: "wednesday",
            3: "thursday",
            4: "friday",
            5: "saturday",
            6: "sunday",
        }
        day = daysofweek[weekno]
        runningallday = False
        

        if daysrunall != "":
            for runfullday in daysrunall.split(","):
                if (
                    teststorun != "all"
                    and teststorun != "none"
                    and (runfullday in day or day in runfullday)
                ):
                    print("Running all tests as we are on " + day)
                    testtypes = []
                    runningallday = True

            if not runningallday:
                if teststorun != "all" and teststorun != "none" and day in daysrunall:
                    print("Running all tests as we are on " + day)
                    testtypes = []
                    runningallday = True

        if startTimeRunAll != "":
            starthour = int(startTimeRunAll.split(":")[0])
            startmin = int(startTimeRunAll.split(":")[1])
            if isNowAfter(dt.time(starthour,startmin)):
                print("Running all tests as we are after " + startTimeRunAll)
                testtypes = []
                runningallday = True


        ####start loop
        for i in testtypes:
            # print(("testsrun1 = " + testsrun))
            try:
                testsrun = get_and_run_tests(i) + testsrun
            except Exception as e:
                print("Error running tests in set")
                # print(e)

        if executetests == "false":
            print("Tests to run")
            print(testsrun)

        # try:
        #    os.environ["TESTSTORUN"] = testsrun
        # except Exception as e:
        #    print(e)

        if testsrun == "":
            if executetests != "false" and teststorun != "all":
                print("executing all tests")
                execute_tests("", 0)
            # os.environ["TESTSTORUN"] = "*"

        if createfile == "true":
            filetosave = "appsurifytests.txt"
            if createfilesdirectory != "":
                os.makedirs(os.path.dirname(createfilesdirectory), exist_ok=True)
                filetosave = os.path.join(createfilesdirectory, filetosave)
            f = open(filetosave, "w+")
            f.write(testsrun)
            f.close()

        if createpropertiesfile == "true":
            f = open("appsurifytests.properties", "w+")
            f.write(f"appsurifytests={testsrun}")
            f.close()

        # print("tests " + os.environ.get('TESTSTORUN'))
        # print("##vso[task.setvariable variable=TestsToRun;isOutput=true]"+testsrun)
        if "azure" in testtemplate:
            max_length = 28000
            variable_num = 1

            if runnewtests != "false" and runnewtests != "true":
                old_percentage = percentage
                percentage = "100"
                testset = get_tests(9)
                count = 0
                alltests = runcommand(runnewtests)
                i = 0
                newtestset = ""
                for line in alltests.splitlines():
                    line = line.strip()
                    if i != 0:
                        newtest = True
                        count = 0
                        for element in testset:
                            count = count + 1
                            testName = element["name"]
                            if testName == line:
                                newtest = False
                        if newtest == True:
                            testtoadd = line
                            if encodetests == "true":
                                testtoadd = testtoadd.encode("unicode_escape").decode()
                                testtoadd = testtoadd.replace("\\", "\\\\")
                                testtoadd = strip_non_ascii(testtoadd)
                                # testtoadd = testtoadd.replace("\\u00F6", "")
                                testtoadd = testtoadd.replace("\n", "\\n")
                                testtoadd = testtoadd.replace("(", "\(")
                                testtoadd = testtoadd.replace(")", "\)")
                                testtoadd = testtoadd.replace("&", "\&")
                                testtoadd = testtoadd.replace("|", "\|")
                                testtoadd = testtoadd.replace("=", "\=")
                                testtoadd = testtoadd.replace("!", "\!")
                                testtoadd = testtoadd.replace("~", "\~")
                            testsrun = (
                                testsrun
                                + testseparator
                                + prefixtest
                                + testtoadd
                                + postfixtest
                            )
                            newtestset = (
                                newtestset
                                + testseparator
                                + prefixtest
                                + testtoadd
                                + postfixtest
                            )
                    if line == "The following Tests are available:":
                        i = i + 1
                percentage = old_percentage
                execute_tests(newtestset, 11)

            if numtestsets != "" and numtestsets != "1" and numtestsets != 1:
                try:
                    numtestsets = int(numtestsets)
                    testlength = len(testsrun)
                    new_max_length = int(testlength / numtestsets) + (
                        testlength % numtestsets > 0
                    )
                    # print("new max length = "+ str(new_max_length))
                    if new_max_length <= max_length:
                        max_length = new_max_length + 50
                except Exception as e:
                    print(e)
            if len(testsrun) == 0 or testsrun == "all":
                print("no tests to set for azure")
                if azurefilteronall == "false":
                    azurefilter = ""
                if azurefilter != "":
                    # print (f'##vso[task.setvariable variable={azure_variable}{variable_num}]{azurefilter}{testsrun}')
                    if azurefilter.endswith("&") is True:
                        azurefilter = azurefilter[:-1]
                    if azurefilter.endswith("|") is True:
                        azurefilter = azurefilter[:-1]
                    print("running all tests")
                    print(
                        f"##vso[task.setvariable variable={azure_variable}{variable_num}]{azurefilter}"
                    )
                    print(
                        f"##vso[task.setvariable variable={azure_variable}]{azurefilter}"
                    )
                if azurefilter == "":
                    print("running all tests")
                    # print (f'##vso[task.setvariable variable={azure_variable}{variable_num}]{testsrun}')
                    print(f"##vso[task.setvariable variable={azure_variable}]")
                    print(
                        f"##vso[task.setvariable variable={azure_variable}{variable_num}]"
                    )
                # print (f'##vso[task.setvariable variable={azurefilter}{azure_variable}{variable_num}]{testsrun}')
            else:
                azurealwaysruntestsformatted = get_always_tests_azure()
                print("running subset of azure tests")
                if (
                    azurefilter[0:-1].endswith("TestCategory=Batch")
                    and azurevariablenum != ""
                    and numtestsets != ""
                ):
                    azurefilter = azurefilter[0:-19]
                if azurefilter != "":
                    if (
                        azurefilter.endswith("&") is False
                        and azurefilter.endswith("|") is False
                    ):
                        azurefilter = azurefilter + "&"
                if azurevariablenum == 0:
                    print(
                        f"##vso[task.setvariable variable={azure_variable}]{azurefilter}({testsrun}){azurealwaysruntestsformatted}"
                    )
                azuresets = []
                while len(testsrun) > max_length:
                    stringtosplit = "|" + prefixtest
                    split_string = testsrun.find(stringtosplit, max_length)
                    setval = testsrun[:split_string]
                    if setval.startswith("|"):
                        setval = setval[1:]
                    testsrun = testsrun[split_string:]
                    print(
                        f"##vso[task.setvariable variable={azure_variable}{variable_num}]{azurefilter}({setval})"
                    )
                    testsettoappend = azurefilter + "(" + setval + ")"
                    azuresets.append(testsettoappend)
                    variable_num = variable_num + 1
                if testsrun.startswith("|"):
                    testsrun = testsrun[1:]
                print(
                    f"##vso[task.setvariable variable={azure_variable}{variable_num}]{azurefilter}({testsrun})"
                )
                testsettoappend = azurefilter + "(" + testsrun + ")"
                azuresets.append(testsettoappend)
                print("Number of variable sets = " + str(variable_num))
                if azurevariablenum != 0:
                    print(f"Setting main variable to varialbe num {azurevariablenum}")
                    azurefilter = azuresets[int(azurevariablenum) - 1]
                    print(
                        f"##vso[task.setvariable variable={azure_variable}]{azurefilter}{azurealwaysruntestsformatted}"
                    )
        # print("##vso[task.setvariable variable=BuildVersion;]998")

        # print("Execution command = " + executioncommand)

        if executioncommand != "" and executioncommand is not None:
            # max_length = 28000
            # variable_num = 1
            # while len(testsrun) > max_length:
            #    split_string = testsrun.find("|Name=",max_length)
            #    setval = testsrun[:split_string]
            #    testsrun = testsrun[split_string:]
            #    print (f'##vso[task.setvariable variable={azure_variable}{variable_num}]{setval}')
            #    variable_num = variable_num + 1
            # print (f'##vso[task.setvariable variable={azure_variable}{variable_num}]{testsrun}')
            executioncommand = executioncommand.replace("[[teststorun]]", testsrun)
            print("Execution command is " + executioncommand)
            runcommand(executioncommand, True)

        if printcommand != "" and printcommand is not None:
            # max_length = 28000
            # variable_num = 1
            # while len(testsrun) > max_length:
            #    split_string = testsrun.find("|Name=",max_length)
            #    setval = testsrun[:split_string]
            #    testsrun = testsrun[split_string:]
            #    print (f'##vso[task.setvariable variable={azure_variable}{variable_num}]{setval}')
            #    variable_num = variable_num + 1
            # print (f'##vso[task.setvariable variable={azure_variable}{variable_num}]{testsrun}')
            printcommand = printcommand.replace("[[teststorun]]", testsrun)
            print(printcommand)

        # if githubactionsvariable != "" and githubactionsvariable is not None:
        #    executioncommand = "echo \"\{githubactionsvariable\}={[[teststorun]]}\" >> $GITHUB_ENV"

        if bitrise == "true":
            print(f'envman add --key TESTS_TO_RUN --value "{testsrun}"')

        if failfast == "false" and rerun == "true" and teststorun != "none":
            rerun_tests()

        # try:
        if upload == "true":
            getresults()
        # except Exception as e:
        # print(e)
        # except:
        #    print("unable to find results")
        print("Command executed successfully")
    except Exception as ex:
        print(ex)
    exit()


if __name__ == "__main__":
    runtestswithappsurify(sys.argv)

# def main(*sys.argv):
# print(sys.argv)
#    runtestswithappsurify(sys.argv)

#    exit()

# main(sys.sys.argv)

#!/bin/bash
# Bash Shell Script to facilitate Code Style Testing
# Python Flake8 Testing of the Python Eve REST Server Modules

#__author__ = "Sanjay Joshi"
#__copyright__ = "Copyright 2016 IBM"
#__credits__ = ["Sanjay Joshi"]
#__license__ = "Apache 2.0"
#__version__ = "1.0"
#__maintainer__ = "Sanjay Joshi"
#__email__ = "joshisa@us.ibm.com"
#__status__ = "Demo"

##########
# Colors##
##########
Green='\e[0;32m'
Red='\e[0;31m'
Yellow='\e[0;33m'
Cyan='\e[0;36m'
no_color='\e[0m' # No Color
beer='\xF0\x9f\x8d\xba'
delivery='\xF0\x9F\x9A\x9A'
beers='\xF0\x9F\x8D\xBB'
eyes='\xF0\x9F\x91\x80'
cloud='\xE2\x98\x81'
litter='\xF0\x9F\x9A\xAE'
fail='\xE2\x9B\x94'
harpoons='\xE2\x87\x8C'
tools='\xE2\x9A\x92'
present='\xF0\x9F\x8E\x81'
#############

export TESTNAME="PEP8 TESTING"

# Download and install ez_setup and pip
echo -e "${harpoons}  ${Yellow}Fetching EZ_SETUP and PIP setup files${no_color}"
wget https://bootstrap.pypa.io/ez_setup.py -nv -O - | python - --user > /dev/null 2>&1
wget https://bootstrap.pypa.io/get-pip.py -nv -O - | python - --user > /dev/null 2>&1
# Install flake8
echo -e "${tools}  ${Yellow}Installing Flake8 Test Framework${no_color}"
~/.local/bin/pip install --user flake8 > /dev/null 2>&1
~/.local/bin/pip install --user flake8-junit-report > /dev/null 2>&1
echo ""
echo -e "${tools}  ${Yellow}Begin Flake8 Testing ....${no_color}"
echo -e "${eyes}    Default Flake8 Settings in effect ..."
echo -e "${eyes}    Max Complexity Allowed: ${Cyan}10${no_color} (see https://en.wikipedia.org/wiki/Cyclomatic_complexity#Limiting_complexity_during_development)"
echo -e "${eyes}    Coding Style: ${Cyan}PEP8${no_color}"
echo ""

# Execute Flake8
flakeError=$(~/.local/bin/flake8 --count --output-file=flake8.txt --exit-zero .)

# Assess Flake8 Results
if [ $flakeError -eq 0 ] ; then
    echo -e "${eyes} TEST RESULT (Code Hygiene): ${Green}Pass${no_color}" 
    echo -e "${beers}  ${Yellow}Sweeeeet.  Zero (0) Errors. Code looks clean to Flake8 validation${no_color}"
    echo -e "${beers}  ${Yellow}finis coronat opus - Bluemix Rox!${no_color}"
    echo ""
    echo -e "${tools}  ${Yellow}Converting Flake8 output to XUnit XML format${no_color}"
    echo "<?xml version='1.0' encoding='utf-8'?>" > flake8.xml
    echo "<testsuite errors='0' failures='0' name='flake8' tests='1' time='1'>" >> flake8.xml
    echo "<testcase result='pass' name='PyFlakes_pycodestyle_McCabe_script_wrapper'/>" >> flake8.xml
    echo "</testsuite>" >> flake8.xml
    echo -e "\n"
else
    echo -e "${eyes} TEST RESULT (Code Hygiene): ${Red}Fail${no_color}" 
    echo -e "${eyes}  ${Yellow}Uh oh!  (${no_color}${flakeError}${Yellow}) error(s) found. Code needs remediation to pass Flake8 validation.  See below.${no_color}"
    echo ""
    echo -e "======= ${Cyan}Error(s)${no_color} ======"
    cat flake8.txt
    echo ""
    echo -e "${tools}  ${Yellow}Converting Flake8 output to XUnit XML format${no_color}"
    ~/.local/bin/flake8_junit flake8.txt flake8.xml
    echo -e "\n"
    # Indicate to pipeline job that we failed
    exit 1
fi

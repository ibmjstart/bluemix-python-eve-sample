#!/bin/bash -ex
# Bash Shell Script to facilitate Setup and Teardown of Test Infra
# To Facilitate Python Nose Unit Testing of the Python Eve REST Server

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

export TESTNAME="NOSE UNIT TESTING"

echo -e "${cloud}  ${Cyan}FYI: Estimated time of job completion: ~5 minutes${no_color}"
echo -e "${tools}  ${Yellow}Updating apt-get ...${no_color}"
sudo apt-get update > /dev/null 2>&1
# Install Python-dev tooling headers for Gevent
echo -e "${tools}  ${Yellow}Setting up Python-dev tooling headers ...${no_color}"
sudo apt-get --assume-yes install python-dev > /dev/null 2>&1
echo -e "${tools}  ${Yellow}Setting up libffi-dev tooling headers ...${no_color}"
sudo apt-get --assume-yes install libffi-dev > /dev/null 2>&1
echo -e "${tools}  ${Yellow}Setting up libssl-dev tooling headers ...${no_color}"
sudo apt-get --assume-yes install libssl-dev > /dev/null 2>&1

# Setup Mongo
echo -e "${tools}  ${Yellow}Install, Start and Configure Local MongoDB Test instance${no_color}"
echo -e "${delivery}   ${Yellow}Creating MongoDB Install Dirs ...${no_color}"
mkdir ~/mongodb
mkdir ~/mongodb/log
touch ~/mongodb/log/mongodb.log
mkdir ~/mongodb/data
mkdir ~/mongodb/data/db
echo -e "${harpoons}    ${Yellow}Fetching Mongodb binary${no_color}"
wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.2.8.tgz -nv -O ~/mongodb/mongodb.tgz
echo -e "${delivery}   ${Yellow}Extracting Mongodb binary${no_color}"
tar -zxvf ~/mongodb/mongodb.tgz -C ~/mongodb > /dev/null 2>&1
echo -e "${delivery}   ${Yellow}Creating Symbolic Links for Mongodb executables${no_color}"
ln -s ~/mongodb/mongodb-linux-x86_64-3.2.8/bin/mongod ~/mongod
ln -s ~/mongodb/mongodb-linux-x86_64-3.2.8/bin/mongo ~/mongo

echo -e "${eyes}   ${Yellow}Starting MongoDB on ${Cyan}localhost${no_color}:${Cyan}27017${no_color}"
~/mongod --quiet --nojournal --logappend --smallfiles --dbpath ~/mongodb/data/db --logpath ~/mongodb/log/mongodb.log --pidfilepath ~/mongodb/data/mongod.lock --fork
sleep 2
echo -e "${delivery}   ${Yellow}Creating ${Cyan}user${Yellow} on database ${Cyan}apitest${no_color}"
~/mongo apitest --eval 'db.createUser({user: "user", pwd:"user", roles: ["readWrite"]})' > /dev/null 2>&1

# Run Server
echo -e "${harpoons}  ${Yellow}Fetching EZ_SETUP and PIP setup files${no_color}"
wget https://bootstrap.pypa.io/ez_setup.py -nv -O - | python - --user > /dev/null 2>&1
wget https://bootstrap.pypa.io/get-pip.py -nv -O - | python - --user > /dev/null 2>&1
echo -e "${tools}  ${Yellow}Installing Redis, Flask, Eve, Eve-docs, Eve-Swagger and gevent ...${no_color}"
~/.local/bin/pip install --user -r ./requirements.txt > /dev/null 2>&1

echo -e "${eyes} ${Yellow}Running Python-Eve REST API Test Server${no_color}"
python ./macreduce/run.py &
sleep 2

# Setup Nose
echo -e "${tools}  ${Yellow}Installing Nose Test Framework${no_color}"
~/.local/bin/pip install --user nose > /dev/null 2>&1

# Run Nose Testing ... booyah!
echo -e "${eyes} ${Yellow}Executing Nose Tests${no_color}"
echo -e ""
~/.local/bin/nosetests --verbosity=2 --stop --cover-html --with-xunit .

echo -e ""
echo -e "${litter}  ${Red}Tearing Down Test Infrastructure${no_color}"

# Tear Down Python-Eve Server
echo -e "      ${Red}Tearing down Python-Eve REST API Test Server${no_color}"
pkill python > /dev/null 2>&1

# Tear Down Mongo Test DB Server
echo -e "      ${Red}Tearing down Mongodb Server${no_color}"
pkill mongo > /dev/null 2>&1

echo -e "${beer}  ${Yellow}finis coronat opus - Bluemix Rox!${no_color}"


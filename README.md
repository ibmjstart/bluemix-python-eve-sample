# Python Eve Sample Deploy Powered by IBM Bluemix

This project is a [Python-Eve Framework](http://python-eve.org/) application backend deployed on IBM Bluemix&trade; that provides a practical illustration of setting up a python REST API to support mobile workloads and integration with 3rd party API platforms.

### Version
1.0

### Deployment
- Cloud

  [![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy?repository=https://github.com/ibmjstart/bluemix-python-eve-sample.git)

- Local
  1. Clone this repository to your local machine
  2. Install and start a local MongoDB listening on default settings
  3. Run Application
  
     `$ python macreduce/run.py`
  4. Browse to http://localhost:5005/api/v1
  5. Invoke the custom endpoint to populate your local application with MAC Address Data hosted on the IEEE organizations site
  
     `$ curl -u bluemix:devfun http://localhost:5005/populate`
  6. Awesome.  You now have a REST API server that can be used to cross-correlate the 3 leading pairs of a MAC Address with its owning Organization.  Have fun.
  7. Fun Enhancement:  Try to extend the model schema to also include the address information for an organization.  Hint: You'll need to tweak the helper module which parses (and ignores the address info from) the IEEE raw data.

### Assumptions/Limitations/Constraints
- Using Python 2.7.9 as declared in the runtime.txt file

### Dependencies
#### Services
- MongoDB provided by MongoLabs
- Redis Cache provided by RedisCloud (Not needed for Local Deploys)

#### Key Python Modules and Frameworks
- Eve (Rest API framework)
- GEvent (WSGI Server wrapper around Flask to bolster performance)
- Requests (Module for invoking HTTP Requests to 3rd party platforms and APIs)

#### Useful Binaries and Platforms
- IBM Bluemix
- IBM DevOps Services
- flake8 to provide PEP8 code syntax testing
- nosetests to provide Unit testing support

### Supporting Resources
[Python-Eve Framework StackOverflow](http://stackoverflow.com/questions/tagged/eve)
[IBM Bluemix](https://www.bluemix.net)
[Python Buildpack](https://github.com/cloudfoundry/python-buildpack)

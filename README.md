# Python Eve Sample Deploy Powered by IBM Bluemix

This project is a [Python-Eve Framework](http://python-eve.org/) application (Flask-based) backend deployed on IBM Bluemix&trade; that provides a practical illustration of setting up a python server REST API to support mobile workloads and integration with 3rd party API platforms.  After deployment, you'll have a REST API server that can be populated with the IEEE MA-L Public Listing.  Using the first three-octet addresses (XX-XX-XX or XXXXXX), a deploy like this could be used as a lookup API and supports guidance given on the IEEE site for individuals interested in querying the public listing to download and parse the data locally.  Some use cases include identifying if a client MAC Address is associated with a particular organization and identifying what three-octet addresses does an organization own.  This sort of API can be handy in conjunction with Internet of Things (IoT) data analytics where MAC address data is common. 

### Version
1.0

### Deployment
- [Live Demo](http://macreduce.mybluemix.net/api/v1/mac)
- Cloud [~10 mins == A publicly visible deploy in the cloud.  Sweet!]

  [![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy/index.html?repository=https://github.com/ibmjstart/bluemix-python-eve-sample.git)

- Local Dev
  1. Clone this repository to your local machine
  2. Install and start a local MongoDB listening on default settings
  3. Install dependencies to your local environment
  
     `$ pip install -r requirements.txt`

  4. Run Application
  
     `$ python macreduce/run.py`

- Data Population
  1. To verify basic server access, browse to ...
     * http://localhost:5005/api/v1
     * http://{enter_your_bluemixhost}.mybluemix.net/api/v1
  2. Invoke the appropriate custom endpoint to populate your deployed application with MAC Address Data hosted from the IEEE organizations site. This endpoint is protected via basic authentication.  This will take a few minutes to process.
  
     `$ curl -u bluemix:devfun http://localhost:5005/populate`

     `$ curl -u bluemix:devfun http://{enter_your_bluemixhost}.mybluemix.net/populate`
     
  3. Awesome.  You now have a REST API server that can be used to cross-correlate the 3 leading pairs of a MAC Address with its owning Organization.  Have fun.  Here's an example of the type of query that you can try ...

    ```$ curl -g -X GET -H "Accept: application/json; charset=utf-8" -H "Cache-Control: no-cache" 'http://{your_host}.mybluemix.net/api/v1/mac?where={"organization":{"$regex":"^ibm.*?$","$options":"i"}}'```
  4. Fun Enhancement:  Try to extend the model schema to also include the address information for an organization.  Hint: You'll need to tweak the helper module which parses (and ignores the address info from) the IEEE raw data.

- [Event Hooks](http://python-eve.org/features.html#event-hooks) (NEW)
  1. Python Eve supports pre-request, post-request and database event hooks. When a particular request is received, an event is raised. You can subscribe to these events with multiple callback functions.  Database event hooks work like request event hooks. These events are fired before and after a database action.
  2. This sample implements an example of a pre and post request event hook.
     - pre-request: Located within [event.py](/macreduce/hooks/event.py) is a method entitled **before_returning_items**.  It prints out the detected Accept-Language request header.
     - post-request: Located within [event.py](/macreduce/hooks/event.py) is a method entitled **after_returning_items**.  It prints a message for all endpoints that were accessed via HTTP GET.
  3. The hooks are configured within [run.py](/macreduce/run.py#L69-L74).  Enabling pre-request hooks involves syntax with **on_pre_** while post-request hooks use **on_post_**.

### Assumptions/Limitations/Constraints
- Using Python 2.7.11 as declared in the runtime.txt file
- Cross-origin resource sharing (CORS) is enabled within [settings.py](/macreduce/settings.py#L120-L122)
- Sample is compatible for deployment on both the US South and United Kingdom Bluemix Regions.  Sydney is not supported at this time.
- **Cloning repository** step within the deploy to bluemix button may show as failing.  This is most likely due to an existing Free tier RedisCloud instance already in existence for your Bluemix organization.  A fallback deploy job is included within this repo to handle this condition.  You can either ignore the error and browse to the build pipeline manually within the jazz.net project or remove your existing RedisCloud service and try the button again.
- When attempting to populate your deployed application with MAC Address Data by invoking the authenticated endpoint (/populate), you may encounter a **500 Error: Failed to establish a backside connection** response.  This error is benign and most likely caused by a timeout upstream.  You can continue to monitor the console output (local deploy) or use **cf logs {bluemix_app_name}** to wait/confirm completion of the population step.  A successful STDOUT sequence will look similar to:
```
  Starting app instance (index 0) with guid d5xxxx-4e7f-xxxx-9206-dcxxxxxxxxx3
  2016-08-12T02:09:06.73-0400 [App/0]      OUT Welcome to Bluemix
  2016-08-12T02:09:06.73-0400 [App/0]      OUT Running on Python version: 2.7.11
  2016-08-12T02:10:11.46-0400 [App/0]      OUT Evaluating if Now is >= Criteria ...
  2016-08-12T02:10:11.46-0400 [App/0]      OUT Refresh criteria has been met
  2016-08-12T02:10:11.46-0400 [App/0]      OUT Begin MAC Address population ...
  2016-08-12T02:10:11.46-0400 [App/0]      OUT Deleting (reset) Mongo Collection named 'mac'
  2016-08-12T02:10:11.46-0400 [App/0]      OUT The best matched Accept-Language Header is: en (English)
  2016-08-12T02:14:23.27-0400 [RTR/1]      OUT macreduce.mybluemix.net - [12/08/2016:06:10:11.453 +0000] "GET /populate HTTP/1.1" 200 0 56 "-" "curl/7.43.0" 169.54.202.28:15063 x_forwarded_for:"23.114.41.234" x_forwarded_proto:"http" vcap_request_id:886b3293-5432-4a10-75fd-01b267cdde51 response_time:251.819555383 app_id:d5xxxx-4e7f-xxxx-9206-dcxxxxxxxxx3 x_global_transaction_id:"587954813"
  2016-08-12T02:14:23.27-0400 [App/0]      OUT Number of MAC Entries matched: 22213
  2016-08-12T02:14:23.27-0400 [App/0]      OUT {"message": "Whoaa! MacReduce Data Populated/Refreshed"}
  2016-08-12T02:14:23.28-0400 [App/0]      ERR 169.55.202.148 - - [2016-08-12 06:14:23] "GET /populate HTTP/1.1" 200 164 251.815483
```
### Dependencies
#### Services
- MongoDB provided by Bluemix Experimental Service
  -  **WARNING**:  For production usage, you should strongly consider using alternate services such as MongoDB by Compose or MongoLabs
- Redis provided by Bluemix Experimental Service or RedisCloud
  -  **WARNING**:  For production usage, you should strongly consider using alternate services such as Redis by Compose or Redis Cache provided by RedisCloud.  The Redis service is **NOT** needed for local Dev/Deployment.

#### [Key Python Modules/Frameworks and EVE extensions](/requirements.txt)
- Eve (Rest API framework) - latest **develop** Branch
- GEvent (WSGI Server wrapper around Flask to bolster performance)
- Requests (Module for invoking HTTP Requests to 3rd party platforms and APIs)
- [Python Eve-Docs](https://github.com/charlesflynn/eve-docs) - A blueprint that generates documentation for Eve APIs in HTML and JSON formats. Eve-docs creates the documentation from your existing Eve configuration file, with no additional configuration required. After deployment, it can be accessed at the api endpoint (/docs) [example](http://macreduce.mybluemix.net/docs)
- [Python Eve-Swagger](https://github.com/nicolaiarocci/eve-swagger) (NEW) - [Swagger](http://swagger.io/) extension for Eve powered RESTful APIs.  After deployment, it can be accessed at the api endpoint (/api-docs) [example](http://macreduce.mybluemix.net/api-docs)
  
  You can use the Swagger 2.0 compliant JSON output from this endpoint in conjunction with other swagger tooling to help document and manage access to your REST APIs.  This also typically requires Cross-origin resource sharing (CORS) to be enabled. See [Assumptions](#assumptionslimitationsconstraints).  Using the [editor.swagger.io](http://editor.swagger.io/#/) web application paired with the JSON output ...

  ![editor.swagger.io screenshot](/macreduce/static/img/editor_swagger_io.png)

#### Custom DevOps Pipeline and Testing (NEW)
![custom pipeline](/macreduce/static/img/custom_devops_pipeline.png)
- Test Jobs for the pipeline are defined within the **[.bluemix/pipeline.yml](/.bluemix/pipeline.yml)** configuration file used by the deploy-to-bluemix button when setting up the devOps pipeline for the first time
- Test Jobs are configured to kill/stop the pipeline if any failures are encountered
- A SetupServices Deploy Job is included as a fallback for service creation if automatic creation via the deploy-to-bluemix button fails 
- Two executable (+x) bash shell scripts located within the **tests** folder
  - [pep8_style_tests.sh](/macreduce/tests/pep8_style_tests.sh) : Purpose is to setup and run Flake8 syntax testing
  
  ![pep8 pipeline test job](/macreduce/static/img/pep8_testjob_pipeline.png)

  - [nose_unit_tests.sh](/macreduce/tests/nose_unit_tests.sh) : Purpose is to setup and run nosetests for all unit tests within the **tests** folder
  
  ![nosetests pipeline test job](/macreduce/static/img/nosetests_testjob_pipeline.png)

- Providing them as source controlled files allows reuse within other projects

#### Useful Binaries and Platforms
- IBM Bluemix
- IBM DevOps Services
- flake8 to provide PEP8 code syntax testing
- nosetests to provide Unit testing support

### License: Apache 2.0

### Supporting Resources
[Python-Eve Framework StackOverflow](http://stackoverflow.com/questions/tagged/eve)

[IBM Bluemix](https://www.bluemix.net)

[Python Buildpack](https://github.com/cloudfoundry/python-buildpack)

[IEEE MA-L Public Listing](http://standards.ieee.org/develop/regauth/oui/public.html)

[IEEE Public OUI Text Document](http://standards-oui.ieee.org/oui.txt) - Updated Daily

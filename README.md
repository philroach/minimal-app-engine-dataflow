# minimal-app-engine-dataflow

Some notes chiefly for myself for future reference.

## Key technologies

* Google Cloud Dataflow
* Python 3.7
* App Engine Flex

## Background

Goal: create some kind of cloud service that can kick-off Dataflow jobs. Parameters will need to be sent to
the service (so Dataflow Templates are out). Secondary - use Python 3.7 rather than 2.7 (there are examples 
to found of the former).

Creating pipelines is relatively easy as is running locally as DirectRunner as is running
locally using DataflowRunner. So the pipeline in this example will be as basic as possible.

Problems begin when a web service kicks of a Dataflow job, either locally or deploying the pipeline generator 
somewhere within GCP.

Here's a non-exhaustive list of gotchas:

* A Dataflow pipeline cannot be bundled with code that handles a web-server request in a single lump of code. This
rules out Google Cloud Functions

* Because of the above, a Dataflow pipeline must include a setup.py

* Because of the above, App Engine Standard cannot be used since (setup.py requires local write permissions)

* Pipeline code must exist as a package (i.e. in it's own directory with an __init__.py)

* A requirements.txt file are required for BOTH app deploy AND the pipeline! This creates dependencies on for
 example gunicorn within the pipeline! 
 
Example errors in GCP Dataflow:
```
ModuleNotFoundError: No module named 'main'
ModuleNotFoundError: No module named 'gunicorn'
```
 
## How to run
 
There are 4 runtime scenarios of interest:
 
1. Run via a local web server using DirectRunner
 
2. Run via a local web server using DataflowRunner

3. Run from App Engine Flex using DataflowRunner 

## Setup

1. Follow basic quick-start steps: https://cloud.google.com/dataflow/docs/quickstarts/quickstart-python but think 
Python 3.7 so use venv (https://docs.python.org/3/library/venv.html) rather than virtualenv.

2. git clone https://github.com/philroach/minimal-app-engine-dataflow.git

3. pip install -r requirements.txt

4. Edit main.py and substitute your own details for project and temp_location:

```python
def runtime_options(is_cloud):
    return {
        'is_cloud': is_cloud,
        'project': 'your_google_cloud_project',
        'temp_location': 'your_cloud_storage_folder'  # example: gs://your_bucket/dataflow/temp
    }
```
5. gunicorn --workers=1 main:app

## Run Local

Point a browser at:

http://127.0.0.1:8000/local

This will execute a local Dataflow pipeline with DirectRunner. The only browser output is "local". You will see
the output of the pipeline in the gunicorn debug at the command prompt.

To send a Dataflow job to GCP:

http://127.0.0.1:8000/cloud

You will need to track progress of the job in GCP. 

## Run on App Engine

1. Edit app.yaml to match your project - note the example points to a service rather than default. If you have not 
got a default service, delete this line.

2. gcloud app deploy

3. Point your browser at https://yourservice-dot-yourproject.appspot.com/cloud
For example, if use default 'dataflow' as service name in app.yaml and your project id is phil:

`https://default-dot-phil.appspot.com/cloud`

This should create and send the dataflow job to GCP.

Now you can go ahead and build that pipeline! 
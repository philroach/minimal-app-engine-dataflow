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
 
 TODO: how to run it all



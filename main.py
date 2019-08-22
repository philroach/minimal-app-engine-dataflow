from flask import Flask, request
from pipeline.minpipeline import minpipeline

app = Flask(__name__)


@app.route('/local')
def local():
    return run(False)


@app.route('/cloud')
def cloud():
    return run(True)


def run(is_cloud):
    options = runtime_options(is_cloud)
    p = minpipeline(options)
    p.run()
    return "cloud" if is_cloud else "local"


def runtime_options(is_cloud):
    return {
        'is_cloud': is_cloud,
        'project': 'your_google_cloud_project',
        'temp_location': 'your_cloud_storage_folder'  # example: gs://your_bucket/dataflow/temp
    }


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)




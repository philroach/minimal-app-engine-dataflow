import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions, GoogleCloudOptions, SetupOptions


class minpipeline:
    def __init__(self, runtime_options):
        self.runtime_options = runtime_options
        self.options = self.make_options()

    def run(self):
        """
        Turn a simple list into a dictionary - add string length to each list item
        """
        p = beam.Pipeline(options=self.options)
        pdict = (
            p
            | beam.Create(['blue', 'black', 'green'])
            | beam.Map(self.do_something)
        )
        p.run()

    def do_something(self, color):
        row = {'color': color, 'len': len(color)}
        print(row)  # local only - output to command prompt (gunicorn)
        return row

    def make_options(self):
        options = PipelineOptions()
        standard_options = options.view_as(StandardOptions)

        google_cloud_options = options.view_as(GoogleCloudOptions)
        google_cloud_options.project = self.runtime_options['project']

        if self.runtime_options['is_cloud']:
            google_cloud_options.job_name = 'minimal-app-engine-dataflow-job'
            google_cloud_options.temp_location = self.runtime_options['temp_location']
            options.view_as(SetupOptions).setup_file = './setup.py'
            standard_options.runner = 'DataflowRunner'
        else:
            standard_options.runner = 'DirectRunner'
        return options


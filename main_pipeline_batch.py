import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from google.cloud import bigquery
import re
import logging
import sys

PROJECT="wellio-integration"

class Split(beam.DoFn):

    def process(self, element):
        from datetime import datetime
        element = element.split(",")
        
        return [{ 
            'full_name': element[0],
            'item_1': element[1],
            'item_2': element[2],
            'item_3': element[3],
            'item_4': element[4],
            'item_5': element[5],
            'item_6': element[6]
    
        }]


def main(argv=None):

   p = beam.Pipeline(options= PipelineOptions(
    flags=argv,
    runner='DataflowRunner',
    project='wellio-integration',
    job_name='test-job3',
    temp_location='gs://dataflow_test_pipeline/temp',
    region='us-central1'))


   (p
      | 'ReadData' >> beam.io.ReadFromText('gs://dataflow_test_pipeline/test.csv')
      # | "clean address" >> beam.Map(regex_clean)
      | 'Preprocess' >> beam.ParDo(Split())
      | 'WriteToBigQuery' >> beam.io.WriteToBigQuery('{0}:dataflow_pipeline.test_table'.format(PROJECT),
        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
   )

   p.run()

if __name__ == '__main__':
  logger = logging.getLogger().setLevel(logging.INFO)
  main()

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from google.cloud import bigquery
import re
import logging
import sys

PROJECT="wellio-integration"
schema = 'full_name:STRING, timelocal:STRING, request_type:STRING, status:STRING, body_bytes_sent:STRING, http_referer:STRING, http_user_agent:STRING'


src_path = "test_user_log_fileC.csv"

def regex_clean(data):

    PATTERNS =  [r'(^\S+\.[\S+\.]+\S+)\s',r'(?<=\[).+?(?=\])',
           r'\"(\S+)\s(\S+)\s*(\S*)\"',r'\s(\d+)\s',r"(?<=\[).\d+(?=\])",
           r'\"[A-Z][a-z]+', r'\"(http|https)://[a-z]+.[a-z]+.[a-z]+']
    result = []
    for match in PATTERNS:
      try:
        reg_match = re.search(match, data).group()
        if reg_match:
          result.append(reg_match)
        else:
          result.append(" ")
      except:
        print("There was an error with the regex search")
    result = [x.strip() for x in result]
    result = [x.replace('"', "") for x in result]
    res = ','.join(result)
    return res




class Split(beam.DoFn):

    def process(self, element):
        from datetime import datetime
        element = element.split(",")
      # d = datetime.strptime(element[1], "%d/%b/%Y:%H:%M:%S")
        # date_string = d.strftime("%Y-%m-%d %H:%M:%S")
        
        return [{ 
            'full_name': "element[0]",
            'timelocal': "element[1]",
            'request_type': "element[2]",
            'body_bytes_sent': "element[3]",
            'status': "element[4]",
            'http_referer': "element[5]",
            'http_user_agent': "element[6]"
    
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
      | 'ReadData' >> beam.io.ReadFromText('gs://dataflow_test_pipeline/test_user_log_fileC.csv')
      | "clean address" >> beam.Map(regex_clean)
      | 'ParseCSV' >> beam.ParDo(Split())
      | 'WriteToBigQuery' >> beam.io.WriteToBigQuery('{0}:dataflow_pipeline.test_table'.format(PROJECT),
        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
   )

   p.run()

if __name__ == '__main__':
  logger = logging.getLogger().setLevel(logging.INFO)
  main()
  
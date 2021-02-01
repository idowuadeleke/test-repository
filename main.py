from googleapiclient.discovery import build

project = 'wellio-integration'
job = 'template-api'



def trigger_dataflow(event, context):
    """Background Cloud Function to be triggered by Cloud Storage.
       This generic function logs relevant data when a file is changed.

    Args:
        event (dict):  The dictionary with data specific to this type of event.
                       The `data` field contains a description of the event in
                       the Cloud Storage `object` format described here:
                       https://cloud.google.com/storage/docs/json_api/v1/objects#resource
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to Stackdriver Logging
    """
    parameters = {
        'temp_location': 'gs://dataflow_test_pipeline/temp',
        'staging_location': 'gs://dataflow_test_pipeline/staging'
    }

    template = 'gs://dataflow_test_pipeline/templates'
    dataflow = build('dataflow', 'v1b3')
    request = dataflow.projects().templates().launch(
        projectId=project,
        gcsPath=template,
        body={
            'jobName': job,
            'parameters': parameters,
        }
    )

    response = request.execute()
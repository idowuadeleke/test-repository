import apache_beam as beam
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that
from apache_beam.testing.util import equal_to
from main_pipeline_batch import Split


abcd = [{ 
            'full_name': "grocery_1",
            'item_1': "apple",
            'item_2': "orange",
            'item_3': "banana",
            'item_4': "lemon",
            'item_5': "strawberry",
            'item_6': "mango"
    
        }]

# class TestCases(unittest.TestCase):

#     def test_count(self):

#         # Create a test pipeline.
#         with TestPipeline() as p:
#             # Create an input PCollection.
#             input = p | beam.Create(WORDS)
#             output = input | beam.ParDo(Split())
#             # Assert on the results.
#             assert_that(output,equal_to())


# TestCases().test_count()

def test_count():

    # Create a test pipeline.
    with TestPipeline() as p:
        # Create an input PCollection.
        input = p | beam.io.ReadFromText('test.csv')
        output = input | beam.ParDo(Split())
        # Assert on the results.
        assert_that(output,equal_to(abcd))


test_count()

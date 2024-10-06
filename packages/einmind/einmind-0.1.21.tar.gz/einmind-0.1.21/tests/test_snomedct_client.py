import unittest
from einmind import SNOMEDCTClient
from einmind.snomed_ct.schemas import TaskStates, TermCategories

class TestSNOMEDCTClient(unittest.TestCase):

    def setUp(self):
        # Initialize the ICD10CMClient for public use
        self.public_client = SNOMEDCTClient()

    def test_public_client_headache(self):
        result = self.public_client.code_term(
            term='headache',
            term_category=TermCategories.PROBLEM
        )
        # Make sure that valid response is created
        self.assertIsNotNone(result)

        # Make sure that mapping is completed
        self.assertEqual(result.task_state, TaskStates.COMPLETED)

        # Make sure that prediction is created
        self.assertIsNotNone(result.prediction)

        # Make sure that prediction is correct
        self.assertIsNotNone(result.prediction.code, "25064002")

    def test_public_client_colonoscopy(self):
        result = self.public_client.code_term(
            term='colonoscopy',
            term_category=TermCategories.PROCEDURE,
        )
        # Make sure that valid response is created
        self.assertIsNotNone(result)

        # Make sure that mapping is completed
        self.assertEqual(result.task_state, TaskStates.COMPLETED)

        # Make sure that prediction is created
        self.assertIsNotNone(result.prediction)

        # Make sure that prediction is correct
        self.assertIsNotNone(result.prediction.code, "73761001")


if __name__ == '__main__':
    unittest.main()

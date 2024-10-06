import unittest
from einmind import ICD10CMClient
from einmind.icd10cm.schemas import TaskStates

class TestICD10CMClient(unittest.TestCase):

    def setUp(self):
        # Initialize the ICD10CMClient for public use
        self.public_client = ICD10CMClient()

    def test_public_client_headache(self):
        result = self.public_client.code_term(term='headache')
        # Make sure that valid response is created
        self.assertIsNotNone(result)

        # Make sure that mapping is completed
        self.assertEqual(result.task_state, TaskStates.COMPLETED)

        # Make sure that prediction is created
        self.assertIsNotNone(result.prediction)

        # Make sure that prediction is correct
        self.assertIsNotNone(result.prediction.code, "R51.9")

    def test_public_client_diabetes_t2(self):
        result = self.public_client.code_term(term='diabetes t2')
        # Make sure that valid response is created
        self.assertIsNotNone(result)

        # Make sure that mapping is completed
        self.assertEqual(result.task_state, TaskStates.COMPLETED)

        # Make sure that prediction is created
        self.assertIsNotNone(result.prediction)

        # Make sure that prediction is correct
        self.assertIsNotNone(result.prediction.code, "E11.9")


if __name__ == '__main__':
    unittest.main()

import unittest
from FreddyApi.module import FreddyApi, MessageRequestPayload, Message
from config import Config
from tqdm import tqdm
import time  # Simulate waiting


class TestFreddyApi(unittest.TestCase):

    def setUp(self):
        # Load a real API token from your config
        token = Config.load_token()
        self.api = FreddyApi(token)

    def test_send_message_success(self):
        # Create the payload with real data
        payload = MessageRequestPayload(
            organization_id=1,  # Real organization ID
            assistant_id=15,  # Real assistant ID
            messages=[Message(content="Hello", role="user")]
        )

        # Perform a real API call
        try:
            response = self.api.create_run(payload)  # Assuming this function sends the message
            self.assertIsNotNone(response, "The response should not be None")
            print("API Response:", response)
        except Exception as e:
            self.fail(f"API call failed: {e}")

    def test_send_message_failure(self):
        # Create an invalid payload that should fail (example: invalid assistant ID)
        payload = MessageRequestPayload(
            organization_id=1,  # Real organization ID
            assistant_id=9999,  # Invalid assistant ID to simulate failure
            model="gpt-4o",  # Model name (e.g., gpt-4o)
            messages=[Message(content="Hello", role="user")]
        )

        # Perform a real API call and expect failure
        with self.assertRaises(Exception) as context:
            self.api.create_run(payload)  # Assuming this function sends the message

        self.assertIn("API request failed", str(context.exception))

    def test_check_run_status_completed(self):
        # Use real organization_id, run_key, and thread_key from a previous run
        organization_id = 1  # Real organization ID
        run_key = "run_zYJ14m8sGAqt7JBZ3NzVUaiu"  # Replace with a valid run_key
        thread_key = "thread_3T6BSDLITANwaGIkWaychThJ"  # Replace with a valid thread_key

        # Poll for the status of the run
        try:
            for _ in tqdm(range(100), desc="Checking run status", unit="attempt"):
                status = self.api.check_run_status(organization_id=organization_id, run_key=run_key,
                                                   thread_key=thread_key)

                if status == "completed":
                    self.assertEqual(status, "completed", "Run status should be completed")
                    print("Run Status:", status)
                    break
                time.sleep(2)  # Simulate waiting period between status checks
            else:
                self.fail("Run did not complete after multiple attempts.")

        except Exception as e:
            self.fail(f"API call failed: {e}")

    def test_get_run_response(self):
        # Use real organization_id and thread_key from a previous run to get the response
        organization_id = 2  # Real organization ID
        thread_key = "thread_WQWyoPExdIpJF8P9NqldtBZL"  # Replace with a valid thread_key

        # Perform a real API call to get the final run response
        try:
            response = self.api.get_run_response(organization_id=organization_id, thread_key=thread_key)
            self.assertIsNotNone(response, "The response should not be None")
            self.assertIn("response", response, "The response should contain the 'response' key")
            print("Run Response:", response["response"])
        except Exception as e:
            self.fail(f"API call failed: {e}")

    def test_execute_run_live(self):
        # Create a sample payload
        messages = [
            Message(content="Tell me a joke.", role="user"),
        ]
        payload = MessageRequestPayload(
            organization_id=1,  # Real organization ID
            assistant_id=2,  # Real assistant ID
            instructions="Provide a joke",
            additional_instructions="Use humor",
            messages=messages
        )

        # Perform the full live run, checking the status and getting the response
        try:
            response = self.api.execute_run(payload)

            # Ensure that the response is not None
            self.assertIsNotNone(response, "The response should not be None")

            # Assert that the response is a list and has at least one element
            self.assertIsInstance(response, list, "The response should be a list")
            self.assertGreater(len(response), 0, "The response list should not be empty")

            # Extract the first dictionary from the list
            first_event = response[0]

            # Ensure that 'response' is a key in the first event
            self.assertIn("response", first_event, "The response should contain the 'response' key")

            # Print the actual response content
            print("Run Response:", first_event["response"])

        except Exception as e:
            self.fail(f"An error occurred during the test: {e}")


if __name__ == "__main__":
    unittest.main()
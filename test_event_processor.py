import json
import os
import unittest
from event_processor import EventProcessor, EVENT_LOG_FILE, CHECKPOINT_FILE

# Sample test events representing different categories and values
test_events = [
    {"id": "A1", "category": "sales", "value": 100},
    {"id": "A2", "category": "sales", "value": 200},
    {"id": "A3", "category": "inventory", "value": 50},
    {"id": "A4", "category": "sales", "value": 300},
    {"id": "A5", "category": "inventory", "value": 75},
    {"id": "A6", "category": "inventory", "value": 55},
]

def reset_files():
    """
    Resets the event log and checkpoint files before running each test.
    This ensures each test starts with a clean slate.
    """
    for file in [EVENT_LOG_FILE, CHECKPOINT_FILE]:
        if os.path.exists(file):
            os.remove(file)

class TestEventProcessor(unittest.TestCase):
    """
    Test suite for the EventProcessor class.
    Covers various scenarios including initial processing, crash recovery, 
    duplicate event handling, out-of-order processing, and large-scale event handling.
    """

    def setUp(self):
        """
        Runs before each test case.
        Resets files and initializes a new EventProcessor instance.
        """
        reset_files()
        self.processor = EventProcessor()

    def write_events(self, events):
        """
        Writes a list of events to the event log file.
        
        Parameters:
            events (list): A list of event dictionaries.
        """
        with open(EVENT_LOG_FILE, "w") as f:
            for event in events:
                f.write(json.dumps(event) + "\n")  # Ensures each event is written on a new line

    def test_initial_processing(self):
        """
        Test Scenario 1: Initial Processing
        Ensures that the processor correctly processes all events when run for the first time.
        """
        print("\nRunning test_initial_processing...")
        self.write_events(test_events)  # Write test events to the event log
        self.processor.recover_and_process()  # Process events
        print("State after processing:", json.dumps(self.processor.state, indent=2))
        self.assertEqual(len(self.processor.state), len(test_events))  # Validate correct processing

    def test_crash_recovery(self):
        """
        Test Scenario 2: Simulated Crash & Recovery
        Ensures that the processor correctly resumes processing from the last checkpoint.
        """
        print("\nRunning test_crash_recovery...")
        self.write_events(test_events[:3])  # Write only first 3 events to simulate a crash
        self.processor.recover_and_process()
        print("State after first processing:", json.dumps(self.processor.state, indent=2))
        self.assertEqual(len(self.processor.state), 3)  # Only 3 events should be processed

        self.write_events(test_events)  # Rewrite all events (simulate recovery)
        self.processor.recover_and_process()
        print("State after recovery:", json.dumps(self.processor.state, indent=2))
        self.assertEqual(len(self.processor.state), len(test_events))  # All events should be processed now

    def test_duplicate_events(self):
        """
        Test Scenario 3: Duplicate Event Handling
        Ensures that duplicate events are ignored and not reprocessed.
        """
        print("\nRunning test_duplicate_events...")
        self.write_events(test_events)
        self.processor.recover_and_process()

        # Add a duplicate event and process again
        self.write_events([test_events[0]])
        self.processor.recover_and_process()
        
        print("State after handling duplicate events:", json.dumps(self.processor.state, indent=2))
        self.assertEqual(len(self.processor.state), len(test_events))  # Count should remain the same

    def test_out_of_order_events(self):
        """
        Test Scenario 4: Out-of-Order Events
        Ensures that events are processed in correct order, even if they arrive out of sequence.
        """
        print("\nRunning test_out_of_order_events...")
        out_of_order_events = [
            {"id": "A3", "category": "inventory", "value": 50},
            {"id": "A1", "category": "sales", "value": 100},
            {"id": "A2", "category": "sales", "value": 200},
            {"id": "A6", "category": "inventory", "value": 55},
            {"id": "A5", "category": "inventory", "value": 75},
            {"id": "A4", "category": "sales", "value": 300},
        ]
        self.write_events(out_of_order_events)
        self.processor.recover_and_process()

        print("State after handling out-of-order events:", json.dumps(self.processor.state, indent=2))
        self.assertEqual(len(self.processor.state), len(test_events))  # Should still process all events

    def test_large_volume(self):
        """
        Test Scenario 5: Large Volume Handling
        Tests how the processor handles a large dataset (1,000+ events).
        """
        print("\nRunning test_large_volume...")
        large_event_log = [{"id": f"A{i}", "category": "sales", "value": i * 10} for i in range(1, 1001)]
        self.write_events(large_event_log)
        self.processor.recover_and_process()

        print(f"Processed {len(self.processor.state)} events in large volume test.")
        self.assertEqual(len(self.processor.state), 1000)  # Ensure all events are processed correctly

if __name__ == "__main__":
    unittest.main()

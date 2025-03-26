import json
import os
from datetime import datetime

# Constants for file storage
EVENT_LOG_FILE = "events.jsonl"  # Stores incoming event data
CHECKPOINT_FILE = "checkpoint.json"  # Stores the last processing state

class EventProcessor:
    """
    EventProcessor is responsible for processing events from a log file,
    maintaining state, handling duplicate events, and ensuring fault tolerance
    using a checkpointing mechanism.
    """

    def __init__(self):
        """
        Initializes the event processor.
        Loads the last checkpoint (if available) to resume processing
        from the last successfully processed event.
        """
        self.state = {}  # Dictionary to store processed events
        self.processed_events = set()  # Set to track processed event IDs
        self.load_checkpoint()  # Load the last saved processing state

    def process_event(self, event):
        """
        Processes an individual event while ensuring duplicates are skipped.

        Parameters:
            event (dict): The event data containing 'id', 'category', and 'value'.
        """
        event_id = event["id"]
        
        # Skip processing if the event was already handled
        if event_id in self.processed_events:
            return  

        # Store the event in state with timestamp
        self.state[event_id] = {
            "category": event["category"],
            "value": event["value"],
            "processed_at": datetime.utcnow().isoformat()  # Record processing timestamp
        }
        self.processed_events.add(event_id)  # Mark as processed

    def save_checkpoint(self):
        """
        Saves the current processing state and list of processed events
        to a checkpoint file to enable crash recovery.
        """
        checkpoint = {
            "processed_events": list(self.processed_events),  # Convert set to list for JSON serialization
            "timestamp": datetime.utcnow().isoformat(),
            "state": self.state
        }

        # Write the checkpoint to file
        with open(CHECKPOINT_FILE, "w") as f:
            json.dump(checkpoint, f)

    def load_checkpoint(self):
        """
        Loads the last saved processing state from the checkpoint file.
        If no checkpoint exists, starts from an empty state.
        """
        if os.path.exists(CHECKPOINT_FILE):
            with open(CHECKPOINT_FILE, "r") as f:
                checkpoint = json.load(f)
                self.state = checkpoint.get("state", {})
                self.processed_events = set(checkpoint.get("processed_events", []))  # Convert back to set for fast lookup

    def recover_and_process(self):
        """
        Recovers the last processing state and processes new events from the log file.
        Ensures events are processed in order and prevents duplicate processing.
        
        Returns:
            bool: True if new events were processed, False otherwise.
        """
        if not os.path.exists(EVENT_LOG_FILE):
            print("No event log found. Nothing to process.")
            return False  # No event log means nothing to process

        # Read events from the log file and clean up whitespace
        with open(EVENT_LOG_FILE, "r") as f:
            events = [json.loads(line.strip()) for line in f if line.strip()]  # Strip extra whitespace and filter empty lines

        # Ensure events are processed in a sequential order
        events.sort(key=lambda x: x["id"])

        processed_any = False  # Flag to track if new events were processed

        for event in events:
            if event["id"] in self.processed_events:
                continue  # Skip already processed events
            
            self.process_event(event)  # Process new event
            processed_any = True

        if processed_any:
            self.save_checkpoint()  # Save updated state after processing new events

        return processed_any  # Return whether any new events were processed

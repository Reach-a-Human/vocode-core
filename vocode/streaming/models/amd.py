from vocode.streaming.models.events import  Event, EventType, Sender

class DetectionEvent(Event):
    sender: Sender = Sender.TWILO_AMD
    confidence: float
    duration: float | None = None  # Optional duration

class AnsweringMachineDetectedEvent(DetectionEvent, type=EventType.ANSWERING_MACHINE_DETECTED):
    pass

class HumanDetectedEvent(DetectionEvent, type=EventType.HUMAN_DETECTED):
    pass

class FaxDetectedEvent(DetectionEvent, type=EventType.FAX_DETECTED):
    pass

class UnknownDetectedEvent(DetectionEvent, type=EventType.UNKNOWN_DETECTED):
    pass

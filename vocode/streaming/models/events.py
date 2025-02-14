from enum import Enum
from typing import Optional

from vocode.streaming.models.model import TypedModel


class Sender(str, Enum):
    HUMAN = "human"
    BOT = "bot"
    ACTION_WORKER = "action_worker"
    VECTOR_DB = "vector_db"
    CONFERENCE = "conference"


class EventType(str, Enum):
    TRANSCRIPT = "event_transcript"
    TRANSCRIPT_COMPLETE = "event_transcript_complete"
    PHONE_CALL_CONNECTED = "event_phone_call_connected"
    PHONE_CALL_ENDED = "event_phone_call_ended"
    PHONE_CALL_DID_NOT_CONNECT = "event_phone_call_did_not_connect"
    RECORDING = "event_recording"
    ACTION = "event_action"

    ANSWERING_MACHINE_DETECTED = "answering_machine_detected"  # Voicemail detected
    HUMAN_DETECTED = "human_detected"  # Live person detected
    FAX_DETECTED = "fax_detected"  # Fax machine detected
    UNKNOWN_DETECTED = "unknown_detected"  # Twilio couldn't determine

    # General Call Status Events
    CALL_INITIATED = "initiated"  # Call has been created but not yet ringing
    CALL_RINGING = "ringing"  # Call is ringing
    CALL_ANSWERED = "answered"  # Call was answered
    CALL_COMPLETED = "completed"  # Call ended normally
    CALL_BUSY = "busy"  # Call was rejected due to the line being busy
    CALL_FAILED = "failed"  # Call failed to connect
    CALL_NO_ANSWER = "no_answer"  # Call rang but was not answered
    CALL_CANCELED = "canceled"  # Call was canceled before connecting


class Event(TypedModel):
    conversation_id: str


class PhoneCallConnectedEvent(Event, type=EventType.PHONE_CALL_CONNECTED):  # type: ignore
    to_phone_number: str
    from_phone_number: str


class PhoneCallEndedEvent(Event, type=EventType.PHONE_CALL_ENDED):  # type: ignore
    conversation_minutes: float = 0


class PhoneCallDidNotConnectEvent(Event, type=EventType.PHONE_CALL_DID_NOT_CONNECT):  # type: ignore
    telephony_status: str


class RecordingEvent(Event, type=EventType.RECORDING):  # type: ignore
    recording_url: str


class ActionEvent(Event, type=EventType.ACTION):  # type: ignore
    action_input: Optional[dict] = None
    action_output: Optional[dict] = None

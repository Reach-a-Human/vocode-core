from enum import Enum
from typing import Any, Dict, Literal, Optional, Union

from vocode.streaming.models.agent import AgentConfig
from vocode.streaming.models.model import BaseModel, TypedModel
from vocode.streaming.models.synthesizer import AzureSynthesizerConfig, SynthesizerConfig
from vocode.streaming.models.transcriber import (
    DeepgramTranscriberConfig,
    PunctuationEndpointingConfig,
    TranscriberConfig,
)
from vocode.streaming.telephony.constants import (
    DEFAULT_AUDIO_ENCODING,
    DEFAULT_CHUNK_SIZE,
    DEFAULT_SAMPLING_RATE,
    VONAGE_AUDIO_ENCODING,
    VONAGE_CHUNK_SIZE,
    VONAGE_SAMPLING_RATE,
)


class TelephonyProviderConfig(BaseModel):
    record: bool = False


class TwilioConfig(TelephonyProviderConfig):
    account_sid: str
    auth_token: str
    extra_params: Optional[Dict[str, Any]] = {}
    account_supports_any_caller_id: bool = True
    answering_machine_detection: bool = False
    answering_machine_callback_url: Optional[str] = None
    status_callback_url: Optional[str] = None

class VonageConfig(TelephonyProviderConfig):
    api_key: str
    api_secret: str
    application_id: str
    private_key: str


class CallEntity(BaseModel):
    phone_number: str


class CreateInboundCall(BaseModel):
    recipient: CallEntity
    caller: CallEntity
    transcriber_config: Optional[TranscriberConfig] = None
    agent_config: AgentConfig
    synthesizer_config: Optional[SynthesizerConfig] = None
    vonage_uuid: Optional[str] = None
    twilio_sid: Optional[str] = None
    conversation_id: Optional[str] = None
    twilio_config: Optional[TwilioConfig] = None
    vonage_config: Optional[VonageConfig] = None


class EndOutboundCall(BaseModel):
    call_id: str
    vonage_config: Optional[VonageConfig] = None
    twilio_config: Optional[TwilioConfig] = None


class CreateOutboundCall(BaseModel):
    recipient: CallEntity
    caller: CallEntity
    transcriber_config: Optional[TranscriberConfig] = None
    agent_config: AgentConfig
    synthesizer_config: Optional[SynthesizerConfig] = None
    conversation_id: Optional[str] = None
    vonage_config: Optional[VonageConfig] = None
    twilio_config: Optional[TwilioConfig] = None
    # TODO add IVR/etc.


class DialIntoZoomCall(BaseModel):
    recipient: CallEntity
    caller: CallEntity
    zoom_meeting_id: str
    zoom_meeting_password: Optional[str]
    transcriber_config: Optional[TranscriberConfig] = None
    agent_config: AgentConfig
    synthesizer_config: Optional[SynthesizerConfig] = None
    conversation_id: Optional[str] = None
    vonage_config: Optional[VonageConfig] = None
    twilio_config: Optional[TwilioConfig] = None


class CallConfigType(str, Enum):
    BASE = "call_config_base"
    TWILIO = "call_config_twilio"
    VONAGE = "call_config_vonage"


PhoneCallDirection = Literal["inbound", "outbound"]


class BaseCallConfig(TypedModel, type=CallConfigType.BASE.value):  # type: ignore
    transcriber_config: TranscriberConfig
    agent_config: AgentConfig
    synthesizer_config: SynthesizerConfig
    from_phone: str
    to_phone: str
    sentry_tags: Dict[str, str] = {}
    conference: bool = False
    telephony_params: Optional[Dict[str, str]] = None
    direction: PhoneCallDirection

    @staticmethod
    def default_transcriber_config():
        raise NotImplementedError

    @staticmethod
    def default_synthesizer_config():
        raise NotImplementedError


class TwilioCallConfig(BaseCallConfig, type=CallConfigType.TWILIO.value):  # type: ignore
    twilio_config: TwilioConfig
    twilio_sid: str

    @staticmethod
    def default_transcriber_config():
        return DeepgramTranscriberConfig(
            sampling_rate=DEFAULT_SAMPLING_RATE,
            audio_encoding=DEFAULT_AUDIO_ENCODING,
            chunk_size=DEFAULT_CHUNK_SIZE,
            model="phonecall",
            tier="nova",
            endpointing_config=PunctuationEndpointingConfig(),
        )

    @staticmethod
    def default_synthesizer_config():
        return AzureSynthesizerConfig(
            sampling_rate=DEFAULT_SAMPLING_RATE,
            audio_encoding=DEFAULT_AUDIO_ENCODING,
        )


class VonageCallConfig(BaseCallConfig, type=CallConfigType.VONAGE.value):  # type: ignore
    vonage_config: VonageConfig
    vonage_uuid: str
    output_to_speaker: bool = False

    @staticmethod
    def default_transcriber_config():
        return DeepgramTranscriberConfig(
            sampling_rate=VONAGE_SAMPLING_RATE,
            audio_encoding=VONAGE_AUDIO_ENCODING,
            chunk_size=VONAGE_CHUNK_SIZE,
            model="phonecall",
            tier="nova",
            endpointing_config=PunctuationEndpointingConfig(),
        )

    @staticmethod
    def default_synthesizer_config():
        return AzureSynthesizerConfig(
            sampling_rate=VONAGE_SAMPLING_RATE,
            audio_encoding=VONAGE_AUDIO_ENCODING,
        )


TelephonyConfig = Union[TwilioConfig, VonageConfig]

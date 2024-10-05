from .base_evaluator import BaseEvaluator
from .services.api_service import NeuralTrustApiService

from .client import NeuralTrust, EventType
from .api_client.types import User, Metadata


def firewall(text):
    return NeuralTrustApiService().firewall(text)

__all__ = [
    "BaseEvaluator",
    "NeuralTrust",
    "User",
    "Metadata",
    "EventType",
    "firewall",
]
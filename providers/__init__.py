"""providers/__init__.py — Provider management + multi-key rotation.

§25 Phase 1 ③. Each provider has a base_url and one or more aliased keys.
Keys carry a user-assigned status (high/medium/low). Galaxy rotates within a
provider before falling back to a different provider. The active key is
chosen by status and recent real error rate — there is no internal
budget or rate-limit-headroom tracker; spend/rate caps are the provider's
own job, set at the API-key level in the provider's dashboard.

A built-in deterministic "galaxy-echo" provider is registered by default so
the system runs end-to-end with no API key configured (and so the eval suite
can execute without spending money). Real providers come online the moment a
key is added via /provider add.
"""

from .manager import ProviderManager, get_provider_manager
from .client import LLMClient, LLMResponse, LLMError
from .echo import EchoProvider

__all__ = [
    "ProviderManager",
    "get_provider_manager",
    "LLMClient",
    "LLMResponse",
    "LLMError",
    "EchoProvider",
]

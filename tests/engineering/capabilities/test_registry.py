from platform_core.engineering.capabilities.models import Capability
from platform_core.engineering.capabilities.registry import CapabilityRegistry


def test_add_capability() -> None:

    registry = CapabilityRegistry()

    runtime = Capability(
        id="runtime", name="Runtime", owner="runtime", status="active", description=""
    )

    registry.add(runtime)

    assert registry.get("runtime") is runtime

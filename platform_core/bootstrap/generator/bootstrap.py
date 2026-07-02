from .generator_engine import GeneratorEngine

from .generators.engine_generator import EngineGenerator
from .generators.capability_generator import CapabilityGenerator
from .project_generator import ProjectGenerator


engine = GeneratorEngine()

engine.registry.register(
    "project",
    ProjectGenerator,
)

engine.registry.register(
    "engine",
    EngineGenerator,
)

engine.registry.register(
    "capability",
    CapabilityGenerator,
)

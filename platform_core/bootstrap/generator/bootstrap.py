from .generator_engine import GeneratorEngine
from .generators.capability_generator import CapabilityGenerator
from .generators.engine_generator import EngineGenerator
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

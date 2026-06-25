from __future__ import annotations

import threading
from collections import defaultdict
from typing import Any, Callable


class CircularDependencyError(Exception):
    """Raised when a circular dependency is detected."""

    def __init__(self, chain: list[type]) -> None:
        self.chain = chain
        chain_names = " -> ".join(t.__name__ for t in chain)
        super().__init__(f"Circular dependency detected: {chain_names}")


class ServiceRegistration:
    __slots__ = (
        "service_type",
        "implementation",
        "factory",
        "lifetime",
        "instance",
    )

    def __init__(
        self,
        service_type: type,
        implementation: type | None = None,
        factory: Callable[..., Any] | None = None,
        lifetime: str = "scoped",
    ) -> None:
        self.service_type = service_type
        self.implementation = implementation
        self.factory = factory
        self.lifetime = lifetime
        self.instance: Any = None


class ServiceScope:
    """Scoped dependency container."""

    def __init__(self, parent: ServiceContainer) -> None:
        self._parent = parent
        self._scoped_instances: dict[type, Any] = {}

    def resolve(self, service_type: type) -> Any:
        registration = self._parent._registrations.get(service_type)
        if registration is None:
            raise KeyError(f"Service not registered: {service_type.__name__}")

        if registration.lifetime == "singleton":
            if registration.instance is None:
                registration.instance = self._create_instance(registration)
            return registration.instance

        if registration.lifetime == "scoped":
            if service_type not in self._scoped_instances:
                self._scoped_instances[service_type] = self._create_instance(
                    registration
                )
            return self._scoped_instances[service_type]

        return self._create_instance(registration)

    def _create_instance(self, registration: ServiceRegistration) -> Any:
        if registration.instance is not None:
            return registration.instance

        if registration.factory is not None:
            return registration.factory()

        if registration.implementation is not None:
            impl = registration.implementation
            deps = self._get_dependencies(impl)
            return impl(*deps)

        raise RuntimeError(
            f"Cannot create instance for {registration.service_type.__name__}"
        )

    def _get_dependencies(self, cls: type) -> list[Any]:
        deps: list[Any] = []
        hints = getattr(cls, "__init__", None)
        if hints is None:
            return deps

        import inspect

        sig = inspect.signature(cls.__init__)
        for name, param in sig.parameters.items():
            if name == "self":
                continue
            if param.annotation is inspect.Parameter.empty:
                continue
            try:
                dep = self.resolve(param.annotation)
                deps.append(dep)
            except KeyError:
                if param.default is not inspect.Parameter.empty:
                    deps.append(param.default)
                else:
                    raise
        return deps

    def dispose(self) -> None:
        for instance in self._scoped_instances.values():
            if hasattr(instance, "shutdown"):
                try:
                    import asyncio

                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        asyncio.ensure_future(instance.shutdown())
                    else:
                        loop.run_until_complete(instance.shutdown())
                except Exception:
                    pass
        self._scoped_instances.clear()


class ServiceContainer:
    """Dependency injection container with singleton, scoped, and transient lifetimes."""

    def __init__(self) -> None:
        self._registrations: dict[type, ServiceRegistration] = {}
        self._lock = threading.RLock()
        self._singleton_lock = threading.Lock()

    def register(
        self,
        service_type: type,
        implementation: type | None = None,
        lifetime: str = "scoped",
    ) -> None:
        with self._lock:
            self._registrations[service_type] = ServiceRegistration(
                service_type=service_type,
                implementation=implementation or service_type,
                lifetime=lifetime,
            )

    def register_factory(
        self,
        service_type: type,
        factory: Callable[..., Any],
        lifetime: str = "scoped",
    ) -> None:
        with self._lock:
            self._registrations[service_type] = ServiceRegistration(
                service_type=service_type,
                factory=factory,
                lifetime=lifetime,
            )

    def register_instance(self, service_type: type, instance: Any) -> None:
        with self._lock:
            reg = ServiceRegistration(
                service_type=service_type,
                lifetime="singleton",
            )
            reg.instance = instance
            self._registrations[service_type] = reg

    def resolve(self, service_type: type) -> Any:
        with self._lock:
            registration = self._registrations.get(service_type)
            if registration is None:
                raise KeyError(f"Service not registered: {service_type.__name__}")

            if registration.lifetime == "singleton":
                if registration.instance is None:
                    with self._singleton_lock:
                        if registration.instance is None:
                            registration.instance = self._create_instance(
                                registration
                            )
                return registration.instance

            if registration.lifetime == "scoped":
                if registration.instance is None:
                    registration.instance = self._create_instance(registration)
                return registration.instance

            return self._create_instance(registration)

    def resolve_all(self, service_type: type) -> list[Any]:
        results: list[Any] = []
        with self._lock:
            for reg_type, reg in self._registrations.items():
                if reg_type == service_type or (
                    reg.implementation
                    and issubclass(reg.implementation, service_type)
                ):
                    results.append(self.resolve(reg_type))
        return results

    def _create_instance(self, registration: ServiceRegistration) -> Any:
        if registration.instance is not None:
            return registration.instance

        if registration.factory is not None:
            return registration.factory()

        if registration.implementation is not None:
            impl = registration.implementation
            deps = self._get_dependencies(impl)
            return impl(*deps)

        raise RuntimeError(
            f"Cannot create instance for {registration.service_type.__name__}"
        )

    def _get_dependencies(self, cls: type) -> list[Any]:
        deps: list[Any] = []
        import inspect

        try:
            sig = inspect.signature(cls.__init__)
        except (ValueError, TypeError):
            return deps

        for name, param in sig.parameters.items():
            if name == "self":
                continue
            if param.annotation is inspect.Parameter.empty:
                continue
            annotation = param.annotation
            if isinstance(annotation, str):
                try:
                    module = inspect.getmodule(cls)
                    if module:
                        annotation = getattr(module, annotation, annotation)
                except Exception:
                    pass
            if isinstance(annotation, str):
                if param.default is not inspect.Parameter.empty:
                    deps.append(param.default)
                continue
            try:
                dep = self.resolve(annotation)
                deps.append(dep)
            except KeyError:
                if param.default is not inspect.Parameter.empty:
                    deps.append(param.default)
                else:
                    raise
        return deps

    def validate(self) -> list[str]:
        errors: list[str] = []
        visited: set[type] = set()
        path: list[type] = []

        def dfs(service_type: type) -> None:
            if service_type in path:
                cycle_start = path.index(service_type)
                chain = path[cycle_start:] + [service_type]
                errors.append(
                    f"Circular dependency: {' -> '.join(t.__name__ for t in chain)}"
                )
                return
            if service_type in visited:
                return

            visited.add(service_type)
            path.append(service_type)

            registration = self._registrations.get(service_type)
            if registration and registration.implementation:
                import inspect

                try:
                    sig = inspect.signature(registration.implementation.__init__)
                    for name, param in sig.parameters.items():
                        if name == "self":
                            continue
                        if param.annotation is inspect.Parameter.empty:
                            continue
                        if param.annotation in self._registrations:
                            dfs(param.annotation)
                except (ValueError, TypeError):
                    pass

            path.pop()

        for service_type in list(self._registrations.keys()):
            dfs(service_type)

        return errors

    def get_registration(self, service_type: type) -> dict[str, Any] | None:
        with self._lock:
            reg = self._registrations.get(service_type)
            if reg is None:
                return None
            return {
                "service_type": reg.service_type.__name__,
                "implementation": reg.implementation.__name__ if reg.implementation else None,
                "lifetime": reg.lifetime,
                "has_instance": reg.instance is not None,
            }

    def create_scope(self) -> ServiceScope:
        return ServiceScope(self)

    def dispose(self) -> None:
        with self._lock:
            for reg in self._registrations.values():
                if reg.instance is not None and hasattr(reg.instance, "shutdown"):
                    try:
                        import asyncio

                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            asyncio.ensure_future(reg.instance.shutdown())
                        else:
                            loop.run_until_complete(reg.instance.shutdown())
                    except Exception:
                        pass
                reg.instance = None

    @property
    def registered_types(self) -> list[str]:
        with self._lock:
            return [t.__name__ for t in self._registrations.keys()]

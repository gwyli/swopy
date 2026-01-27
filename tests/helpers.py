import inspect

from numberology import systems

MODULES: list[str] = getattr(systems, "__all__", [])


def get_systems() -> set[type]:
    """Helper to get all system classes."""
    system_classes: set[type] = set()

    for module_name in MODULES:
        module = getattr(systems, module_name)

        for _, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                if obj.__name__ == "System":
                    continue

                system_classes.add(obj)

    return system_classes


SYSTEMS: list[type] = list(get_systems())
SYSTEMS_WITHOUT_ARABIC: list[type] = list(
    {s for s in SYSTEMS if s.__name__ != "Arabic"}
)

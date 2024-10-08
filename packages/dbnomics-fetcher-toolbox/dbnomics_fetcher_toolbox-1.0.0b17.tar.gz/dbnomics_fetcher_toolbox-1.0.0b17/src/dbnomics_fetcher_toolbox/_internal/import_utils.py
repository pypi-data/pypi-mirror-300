import importlib

__all__ = ["load_class_from_string"]


def load_class_from_string(class_path: str) -> type:
    module_path, class_name = class_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

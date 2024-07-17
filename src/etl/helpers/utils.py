from pathlib import Path


def get_dag_id(name: str) -> str:
    """Generate dag id from file"""
    return Path(name).stem.replace("_", "-").removesuffix("-dag")

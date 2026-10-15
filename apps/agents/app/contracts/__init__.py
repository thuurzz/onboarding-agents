import json
from pathlib import Path

CONTRACT_PATH: Path = Path(__file__).resolve().parent / "platforms.json"


def load_contract() -> dict:
    with open(CONTRACT_PATH, encoding="utf-8") as handle:
        return json.load(handle)


def common_fields(contract: dict | None = None) -> list[str]:
    data = contract or load_contract()
    return list(data["common_fields"])


def platform_ids(contract: dict | None = None) -> list[str]:
    data = contract or load_contract()
    return [platform["id"] for platform in data["platforms"]]


def platform_required_fields(platform_id: str, contract: dict | None = None) -> list[str]:
    data = contract or load_contract()
    for platform in data["platforms"]:
        if platform["id"] == platform_id:
            return list(platform["required_fields"])
    return []


def platform_name(platform_id: str, contract: dict | None = None) -> str | None:
    data = contract or load_contract()
    for platform in data["platforms"]:
        if platform["id"] == platform_id:
            return platform["name"]
    return None


def all_required_fields(platform_id: str, contract: dict | None = None) -> list[str]:
    return common_fields(contract) + platform_required_fields(platform_id, contract)

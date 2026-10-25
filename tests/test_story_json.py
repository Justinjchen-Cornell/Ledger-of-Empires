import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
STORIES = sorted((ROOT / "05-输出/工作台/stories").glob("*.json"))

def load_all():
    return [(path, json.loads(path.read_text(encoding="utf-8"))) for path in STORIES]

@pytest.mark.parametrize("path,data", load_all())
def test_required_fields(path, data):
    assert data["id"]
    assert data["title"]
    assert data["start"] in data["scenes"]

@pytest.mark.parametrize("path,data", load_all())
def test_all_next_targets_exist(path, data):
    scenes = data["scenes"]
    for name, scene in scenes.items():
        for choice in scene.get("choices", []):
            assert choice["next"] in scenes, f"{name} -> {choice['next']}"
        if "next" in scene:
            assert scene["next"] in scenes, f"{name} -> {scene['next']}"

@pytest.mark.parametrize("path,data", load_all())
def test_every_scene_has_text_and_continuation(path, data):
    for name, scene in data["scenes"].items():
        assert scene.get("text"), name
        assert scene.get("choices") or scene.get("next") or scene.get("card"), name

@pytest.mark.parametrize("path,data", load_all())
def test_three_acts_and_end(path, data):
    acts = {scene.get("act") for scene in data["scenes"].values() if scene.get("act")}
    assert acts == {1, 2, 3}
    assert any(scene.get("card") for scene in data["scenes"].values())

@pytest.mark.parametrize("path,data", load_all())
def test_reachable_end(path, data):
    scenes = data["scenes"]
    seen = set()
    stack = [data["start"]]
    while stack:
        name = stack.pop()
        if name in seen:
            continue
        seen.add(name)
        scene = scenes[name]
        for choice in scene.get("choices", []):
            stack.append(choice["next"])
        if "next" in scene:
            stack.append(scene["next"])
    assert any(scenes[name].get("card") for name in seen)

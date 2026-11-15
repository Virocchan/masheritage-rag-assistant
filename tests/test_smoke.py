import pathlib
import json


def test_required_files_exist():
    for p in [
        "README.md",
        "data/SOURCES.md",
        "data/sources.csv",
        "docs/week1_project_scope.md",
        "docs/risk_analysis.md",
        "docs/week2_requirements.md",
        "docs/week2_architecture_decisions.md",
        "docs/week2_evaluation_criteria.md",
        "docs/week3_data_inventory.md",
        "docs/week3_pipeline_decisions.md",
        "docs/week3_pipeline_diagram.png",
        "notebooks/week3_pipeline.ipynb",
        "data/week3_manifest.json",
        "data/pipeline_v1/documents/pipeline_manifest.json",
        "data/pipeline_v1/documents/prepared_text.jsonl",
    ]:
        assert pathlib.Path(p).exists(), f"Missing required file: {p}"


def test_manifest_integrity():
    week3_manifest = pathlib.Path("data/week3_manifest.json")
    assert week3_manifest.exists()
    data = json.loads(week3_manifest.read_text(encoding="utf-8"))
    assert data["pipeline_version"] == "week3-v1"
    assert data["source_count"] >= 2
    assert data["prepared_chunk_count"] > 0


def test_pipeline_v1_integrity():
    pipe_manifest = pathlib.Path("data/pipeline_v1/documents/pipeline_manifest.json")
    assert pipe_manifest.exists()
    data = json.loads(pipe_manifest.read_text(encoding="utf-8"))
    assert data["status"] == "SUCCESS"
    assert len(data["input_sources"]) >= 2


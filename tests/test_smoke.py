import pathlib
import json
import pickle


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


def test_week4_deliverables():
    for p in [
        "notebooks/week4_quality.ipynb",
        "data/prepared_chunks.jsonl",
        "data/chunks.pkl",
        "data/prepared_chunks_clean.jsonl",
        "data/chunks_clean.pkl",
        "docs/week4_data_quality_report.md",
        "docs/week4_validation_failures.csv",
        "docs/week4_duplicate_review.csv",
        "docs/week4_coverage_by_source.png",
    ]:
        assert pathlib.Path(p).exists(), f"Missing Topic 4 deliverable: {p}"

    # Verify cleaned corpus alignment
    clean_jsonl = pathlib.Path("data/prepared_chunks_clean.jsonl")
    clean_pkl = pathlib.Path("data/chunks_clean.pkl")
    
    with open(clean_pkl, "rb") as f:
        pkl_chunks = pickle.load(f)
    
    with open(clean_jsonl, "r", encoding="utf-8") as f:
        jsonl_records = [json.loads(line) for line in f if line.strip()]

    assert len(pkl_chunks) == len(jsonl_records) == 189, f"Count mismatch: PKL ({len(pkl_chunks)}) vs JSONL ({len(jsonl_records)})"

    # Verify report quality gate decision
    report = pathlib.Path("docs/week4_data_quality_report.md").read_text(encoding="utf-8")
    assert "GO WITH CONDITIONS" in report, "Missing quality gate decision in report"

import pathlib


def test_required_files_exist():
    for p in ["README.md", "data/SOURCES.md", "docs/project_scope.md", "docs/risk_analysis.md"]:
        assert pathlib.Path(p).exists(), p

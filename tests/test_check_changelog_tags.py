"""Tests for scripts/check_changelog_tags.py (KI-056-8)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_changelog_tags as cct

TAGS = ["v4.38.0", "v4.37.0", "v3.4.0", "v3.5.2"]
GAPS = ["v3.4.0", "v3.5.2"]
CLEAN = "# Changelog\n\n## [Unreleased]\n\n## [4.38.0] - x\n- a\n\n## [4.37.0] - y\n- b\n"


def test_clean_pass() -> None:
    assert cct.check(TAGS, CLEAN) == []


def test_deleted_header_fused_into_bullet() -> None:
    text = CLEAN.replace("## [4.38.0] - x\n- a", "- a")
    text = text.replace("- a", "- a ## [4.38.0] - x")
    errors = cct.check(TAGS, text)
    assert len(errors) == 1
    assert "v4.38.0" in errors[0]


def test_out_of_order() -> None:
    text = "## [4.37.0]\n\n## [4.38.0]\n"
    errors = cct.check(["v4.37.0", "v4.38.0", *GAPS], text)
    assert errors and "header order" in errors[0]


def test_numeric_order() -> None:
    tags = ["v4.9.0", "v4.10.0", *GAPS]
    assert cct.check(tags, "## [4.10.0]\n\n## [4.9.0]\n") == []
    assert cct.check(tags, "## [4.9.0]\n\n## [4.10.0]\n") != []


def test_duplicate_header_is_not_descending() -> None:
    assert cct.check(["v1.0.0", *GAPS], "## [1.0.0]\n## [1.0.0]\n") != []


def test_gap_entry_skipped() -> None:
    assert "v3.4.0" in cct.HISTORICAL_GAPS
    assert cct.check_presence(cct.parse_tags(["v3.4.0", "v3.5.2"]), set()) == []


def test_stale_gap_entry_no_tag() -> None:
    errors = cct.check_presence(cct.parse_tags([]), set())
    assert any("no longer a tag" in e for e in errors)


def test_stale_gap_entry_has_header() -> None:
    errors = cct.check_presence(cct.parse_tags(["v3.4.0", "v3.5.2"]), {(3, 4, 0), (3, 5, 2)})
    assert sum("now has its header" in e for e in errors) == 2


def test_non_semver_tags_ignored() -> None:
    tags = ["v4.38.0", "v4.37.0", "v3.4.0", "v3.5.2", "v5.0", "release-1", "v1.2.3-rc1"]
    assert cct.check(tags, CLEAN) == []


def test_missing_changelog_exits_2(tmp_path: Path) -> None:
    assert cct.main(["--changelog", str(tmp_path / "absent.md")]) == 2


def test_zero_tags_good_order_skips_presence() -> None:
    assert cct.check([], CLEAN) == []
    assert cct.check(["v5.0", "release-1"], CLEAN) == []
    assert cct.NO_TAGS_NOTICE.startswith("no semver tags visible")


def test_zero_tags_bad_order_exits_2(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cct, "read_git_tags", list)
    bad = tmp_path / "CHANGELOG.md"
    bad.write_text("## [4.37.0]\n\n## [4.38.0]\n", encoding="utf-8")
    assert cct.main(["--changelog", str(bad)]) == 2
    good = tmp_path / "good.md"
    good.write_text(CLEAN, encoding="utf-8")
    assert cct.main(["--changelog", str(good)]) == 0


def test_notice_printed_on_stderr(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(cct, "read_git_tags", list)
    good = tmp_path / "good.md"
    good.write_text(CLEAN, encoding="utf-8")
    cct.main(["--changelog", str(good)])
    assert cct.NO_TAGS_NOTICE in capsys.readouterr().err


def test_real_repo() -> None:
    assert cct.main([]) == 0


@pytest.mark.parametrize("version", [(4, 10, 0)])
def test_fmt(version: tuple[int, int, int]) -> None:
    assert cct.fmt(version) == "4.10.0"

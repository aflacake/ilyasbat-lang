# tests/test_impor.py

import io
import os
import sys
import tempfile
import builtins
import pytest

from helpers import impor
from helpers.fungsi_registry import fungsi_registry


@pytest.fixture
def sample_code():
    """Contoh kode IlyasBat sederhana untuk diuji."""
    return """
fungsi sapa(nama)
    menampilkan Halo, %nama%
selesai

kalku hasil = 5 + 3
menampilkan hasil
"""


def test_load_file(tmp_path, sample_code):
    """Pastikan load_file() bisa membaca file dengan benar."""
    file_path = tmp_path / "contoh.ibat"
    file_path.write_text(sample_code, encoding="utf-8")

    content = impor.load_file(str(file_path))
    assert "fungsi sapa" in content
    assert "kalku hasil" in content


def test_analyze_code(sample_code):
    """Pastikan fungsi dan variabel bisa terdeteksi dengan benar."""
    functions, variables = impor.analyze_code(sample_code)

    assert "sapa" in functions
    assert "hasil" in variables


def test_register_functions_from_code(sample_code):
    """Pastikan fungsi terdaftar ke fungsi_registry."""
    impor.register_functions_from_code(sample_code)

    assert "sapa" in fungsi_registry
    entry = fungsi_registry["sapa"]
    assert entry["args"] == ["nama"]
    assert any("menampilkan" in line for line in entry["body"])


def test_run_module_code_executes(monkeypatch, sample_code):
    """Pastikan run_module_code() bisa mengeksekusi baris non-fungsi."""

    env = {}

    printed = []
    monkeypatch.setattr(builtins, "print", lambda *a, **kw: printed.append(" ".join(map(str, a))))

    impor.run_module_code(sample_code, env)

    joined_output = "\n".join(printed)
    assert "hasil" in joined_output or "Halo" in joined_output


def test_pretty_print_does_not_crash(sample_code, capsys):
    """Pastikan pretty_print() bisa menampilkan kode tanpa error."""
    impor.pretty_print(sample_code)
    output = capsys.readouterr().out
    assert ">>> fungsi sapa(nama)" in output or ">>> fungsi sapa" in output


def test_file_not_found():
    """Pastikan load_file() melempar FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        impor.load_file("tidak_ada.ibat")

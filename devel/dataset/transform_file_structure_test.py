import pytest
import os
import unittest
from pathlib import Path
from devel.dataset import transform_file_structure


@unittest.skipIf(os.environ.get("TRAVIS", False), "Skip on Travis-CI")
def test_pilsen_pigs():
    input_dir = r'H:\biomedical\orig\pilsen_pigs_raw\transplantation'
    output_dir = Path(r"H:\biomedical\orig\pilsen_pigs")
    transform_file_structure.prepare_pilsen_pigs_dataset(input_dir, output_dir=output_dir, output_format=".mhd")

    assert (output_dir / "pilsen_pigs_Tx041D_Ven" / "PATIENT_DICOM" / "pilsen_pigs_Tx041D_Ven.mhd").exists()
    assert (output_dir / "pilsen_pigs_Tx041D_Ven" / "PATIENT_DICOM" / "pilsen_pigs_Tx041D_Ven.raw").exists()

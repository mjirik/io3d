import pytest
import os
import unittest
from pathlib import Path
from devel.dataset import transform_file_structure
import io3d
from loguru import logger


@unittest.skipIf(os.environ.get("TRAVIS", False), "Skip on Travis-CI")
def test_pilsen_pigs():
    input_dir = r'H:\biomedical\orig\pilsen_pigs_raw\transplantation'
    output_dir = Path(r"H:\biomedical\orig\pilsen_pigs")
    input_dir = io3d.joinp("pilsen_pigs_raw/transplantation")   # r'H:\biomedical\orig\pilsen_pigs_raw\transplantation'
    input_dir = Path(r'G:\.shortcut-targets-by-id\1Vq6QAiJ7cHDJUdgKXjUxx5iw7zk6MMPI\transplantation')
    output_dir = Path(r'G:\.shortcut-targets-by-id\1nz7i4Zssar8075yu6J5QpHdph6oi3uF8\pilsen_pigs')
    file_list1 = list(input_dir.glob('*_Ven*'))
    transform_file_structure.prepare_pilsen_pigs_dataset(input_dir, output_dir=output_dir, output_format=".mhd")
    file_list2 = list(input_dir.glob('*_Ven*'))

    # assert (output_dir / "pilsen_pigs_Tx041D_Ven" / "PATIENT_DICOM" / "pig_001.mhd").exists()
    # assert (output_dir / "pilsen_pigs_Tx041D_Ven" / "PATIENT_DICOM" / "pilsen_pigs_Tx041D_Ven.raw").exists()

    assert (len(file_list1) < len(file_list2))


@unittest.skipIf(os.environ.get("TRAVIS", False), "Skip on Travis-CI")
def test_pilsen_pigs_create_in_dataset_dir():
    input_mask="*Tx029D_Ven*"
    # input_mask="*D_Ven*" # to run all data
    input_dir = io3d.joinp("biomedical/orig/pilsen_pigs_raw/transplantation")   # r'H:\biomedical\orig\pilsen_pigs_raw\transplantation'
    output_type = ".mhd"
    output_dir = io3d.datasets.get_dataset_path("pilsen_pigs", "data3d", data_id=1).parents[2]
    # input_dir = r'H:\biomedical\orig\pilsen_pigs_raw\transplantation'
    # output_dir = Path(r"H:\biomedical\orig\pilsen_pigs")
    assert input_dir.exists()
    # input_dir = Path(r'G:\.shortcut-targets-by-id\1Vq6QAiJ7cHDJUdgKXjUxx5iw7zk6MMPI\transplantation')
    # output_dir = Path(r'G:\.shortcut-targets-by-id\1nz7i4Zssar8075yu6J5QpHdph6oi3uF8\pilsen_pigs')
    file_list1 = list(input_dir.glob('*_Ven*'))
    logger.debug(output_dir)
    transform_file_structure.prepare_pilsen_pigs_dataset(input_dir, output_dir=output_dir,input_mask=input_mask, output_format=output_type, dirname_pattern='{re_out[0]}', regexp_pattern='(Tx[0-9]+D_Ven)')

    file_list2 = list(input_dir.glob('*_Ven*'))

    # assert (output_dir / "pilsen_pigs_Tx041D_Ven" / "PATIENT_DICOM" / "pig_001.mhd").exists()
    # assert (output_dir / "pilsen_pigs_Tx041D_Ven" / "PATIENT_DICOM" / "pilsen_pigs_Tx041D_Ven.raw").exists()

    # assert (len(file_list1) < len(file_list2))

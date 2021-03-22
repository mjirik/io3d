import pytest
from pathlib import Path
import nibabel as nib
from matplotlib import pylab as plt
from loguru import logger
import numpy as np
import io3d
import io3d.network
from io3d import nifti_io


# @unittest.skipIf(os.environ.get("TRAVIS", True), "Skip on Travis-CI")
def test_read_nifti():
    pth = io3d.datasets.fetch_file(r"https://nifti.nimh.nih.gov/pub/dist/data/nifti2/avg152T1_LR_nifti2.nii.gz")

    # pth = Path('~/Downloads/avg152T1_LR_nifti2.nii.gz').expanduser()
    img = nib.load(pth)
    data3d = img.dataobj
    img.shape
    plt.imshow(data3d[:,:, 50])
    plt.show()

    logger.debug(img.header.get_zooms())
    logger.debug(img.affine)
    logger.debug(np.asarray(img.shape) * 1)
    logger.debug(np.asarray(img.shape) * 2)

    data = np.arange(4 * 4 * 3).reshape(4, 4, 3)



    voxelsize_mm = [1., 2., 3.]

    diag = np.ones([4])
    diag[:3] = voxelsize_mm[:]
    affine = np.diag(diag)
    new_image = nib.Nifti1Image(data, affine=affine)

    new_image.header.set_zooms(voxelsize_mm)

    logger.debug(new_image.header.get_zooms())
    logger.debug(new_image.affine)
    # ornt_my = nib.orientations.axcodes2ornt(new_image.orientations)
    # import SimpleITK as sitk
    # im = sitk.ReadImage(str(pth))
    # voxelsize_mm = im.GetSpacing()
    # print(voxelsize_mm)


def test_write_and_read_nifi():
    shape = [5, 6, 7]
    voxelsize_mm = [1., 2., 3.]
    fn = 'test.nii'
    data3d = np.array(range(np.prod(shape))).reshape(shape)

    nifti_io.write_nifti(
        dict(data3d=data3d, voxelsize_mm=voxelsize_mm, orientation_axcodes='RAS'),
        fn
    )

    new_data3d, metadata = nifti_io.read_nifti(fn)

    for i, val in np.ndenumerate(data3d):
        assert new_data3d[i] == data3d[i]

    assert voxelsize_mm[0] == metadata["voxelsize_mm"][0]
    assert voxelsize_mm[1] == metadata["voxelsize_mm"][1]
    assert voxelsize_mm[2] == metadata["voxelsize_mm"][2]


def test_write_and_read_nifi_with_datap():
    shape = [5, 6, 7]
    voxelsize_mm = [1., 2., 3.]
    fn = 'test.nii.gz'
    data3d = np.array(range(np.prod(shape))).reshape(shape)

    datap = io3d.image.DataPlus(
        dict(data3d=data3d, voxelsize_mm=voxelsize_mm, orientation_axcodes='RAS'))
    logger.debug(datap.orientation_axcodes)
    io3d.write(datap, fn)

    new_datap = io3d.read(fn, orientation_axcodes="RAS")
    logger.debug(data3d.shape)
    logger.debug(new_datap.data3d.shape)
    assert data3d.shape[0] == new_datap.data3d.shape[0]
    assert data3d.shape[1] == new_datap.data3d.shape[1]
    assert data3d.shape[2] == new_datap.data3d.shape[2]

    for i, val in np.ndenumerate(data3d):
        assert new_datap.data3d[i] == data3d[i]

    assert voxelsize_mm[0] == new_datap["voxelsize_mm"][0]
    assert voxelsize_mm[1] == new_datap["voxelsize_mm"][1]
    assert voxelsize_mm[2] == new_datap["voxelsize_mm"][2]



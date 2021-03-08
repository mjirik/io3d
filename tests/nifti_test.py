import pytest
from pathlib import Path
import nibabel as nib
from matplotlib import pylab as plt



def test_read_nifti():
    pth = Path('~/Downloads/avg152T1_LR_nifti2.nii.gz').expanduser()
    img = nib.load(pth)
    data3d = img.dataobj
    img.shape
    plt.imshow(data3d[:,:, 50])
    plt.show()
    print(img.affine)

    # import SimpleITK as sitk
    # im = sitk.ReadImage(str(pth))
    # voxelsize_mm = im.GetSpacing()
    # print(voxelsize_mm)


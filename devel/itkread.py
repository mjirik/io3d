from pathlib import Path
import SimpleITK as sitk
import numpy as np

# pth = Path("~/data/medical/orig/")
pth = r"G:\Můj disk\data\medical\orig\sliver07\training\liver-orig001.mhd"


def readim(pth):
    ppth = Path(pth)

    print(ppth.exists())
    im = sitk.ReadImage(pth)
    imnp = sitk.GetArrayFromImage(im)

    print(f"shape={imnp.shape}")
    mx = np.max(imnp)
    print(f"max={mx}")
    print(f"min={np.min(imnp)}")


pth1 = r"h:\medical\orig\sliver07\training\liver-orig001.mhd"
pth2 = r"G:\Můj disk\data\medical\orig\sliver07\training\liver-orig001.mhd"

readim(pth1)
readim(pth2)

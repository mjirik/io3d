# %%
import io3d
import sed3
import imma
import imma.image
from loguru import logger
from pathlib import Path


# min=40-200 max=40+200
def export_to_jpg(input_path, output_path, output_name, width, center, cmap='gray', resize_to_shape=None,
                  **resize_kwargs):
    import matplotlib.pyplot as plt
    import os
    # !!!!!!! watch, if you have folder "JPG" and it conteins important files

    output_path = Path(f'{output_path}')
    output_path.mkdir(parents=True, exist_ok=True)
    dr = io3d.DataReader()
    datap = dr.Get3DData(input_path, dataplus_format=True)
    data3d = datap['data3d']
    if resize_to_shape:
        data3d = imma.image.resize_to_shape(data3d, shape=resize_to_shape, **resize_kwargs)

    PixMin = center - width / 2
    PixMax = center + width / 2
    logger.debug(data3d.shape)
    for i in range(0, data3d.shape[0]):  # shape - numpy pole, rekne jaki jsou roymery v jednotlive dimenze
        logger.info(i)
        plt.imsave(output_path / f'{output_name}_{i:05}.jpg', data3d[i, :, :], vmin=PixMin, vmax=PixMax, cmap=cmap)


# %%

# colorMap='gray'
# input_path=f'F:\Diplom\Diplom\Tx036D_Ven'
input_path = r'H:\biomedical\orig\pilsen_pigs_raw\transplantation\Tx021D_Ven'
input_path = r"H:\medical\orig\3Dircadb1.1\PATIENT_DICOM"
# output_path=input_path
output_path = r"H:\paper_graphics\2021_detska_univerzita\JPG2"
output_name = 'Tx021D_Ven'  # zahlavní jmeno pacientu
center = 40
width = 400

for i in range(5,7):
    input_path = fr"H:\medical\orig\3Dircadb1.{i}\PATIENT_DICOM"
    output_path = fr"H:\paper_graphics\2021_detska_univerzita\JPG_{i}"
    output_name = f'Tx0{i:02d}D_Ven'  # zahlavní jmeno pacientu
    export_to_jpg(input_path, output_path, output_name, width, center, resize_to_shape=[16, 512, 512], order=1, anti_aliasing=True)



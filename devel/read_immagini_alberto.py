# import dicom
import SimpleITK as sitk


# does not work:w
def readim(pth):
    im = sitk.ReadImage(pth)
    imnp = sitk.GetArrayFromImage(im)

    print(f"shape={imnp.shape}")
    mx = imnp.max()
    print(f"max={mx}")
    print(f"min={imnp.min()}")


fn = r"C:\Users\Jirik\my_bc_data\data\medical\orig\immagini_alberto\Immagini Nuewa\PATIENTDATAI9\PATIENTDATA\20230919\20230919-170746-0005-0F0A\4607170008000F14270F0A\202309191710330081GYN\BC_CinePartition0.bin"
fn = r"C:\Users\Jirik\my_bc_data\data\medical\orig\immagini_alberto\Immagini Nuewa\PATIENTDATAI9\PATIENTDATA\20230919\20230919-170746-0005-0F0A\4607170008000F14270F0A\202309191710330081GYN\DcmRegionPara.txt"
readim(fn)
# # dcm = dicom.read_file(fn)
# # print(dcm)
# img = sitk.ReadImage(fn)

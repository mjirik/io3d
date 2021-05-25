import io3d
from pathlib import Path
import SimpleITK
import regex
from loguru import logger


def prepare_pilsen_pigs_dataset(input_dir, output_dir, input_mask='*_Ven*', start_index = 0, output_format=".mhd", dirname_pattern='pig_{i:04d}', regexp_pattern="Tx([0-9]+)"):
    """
    :param input_dir: vstupni cesta
    :param output_dir: vystup. cesta
    :param input_mask: cast nazvu zvol. souboru (pro fci. glob)
    :param start_index: cislo od ktereho zacneme vytvaret slozky
    :param dirname_pattern: pattern used for construction of output directory name, `i` or `re_out` can be used. I.e. 'pig_{re_out[0]}', or '{re_out[0]}
    :param regexp_pattern: used to extract regex_i from filename. I.e. '(Tx[0-9]+D_Ven)'
    """


    # ukladani obsahu slozek
    file_list = list(input_dir.glob(input_mask))
    i = start_index
    for f_name in file_list:
        re_out = regex.findall(regexp_pattern, str(f_name))
        regex_i = re_out[0] if len(re_out) else None
        p = output_dir/ dirname_pattern.format(i=i, regex_i=regex_i, re_out=re_out)


        p1 = p /'LABELED_DICOM'
        p2 = p / 'MASKS_DICOM'
        p3 = p / 'MESHES_VTK'
        p4 = p / 'PATIENT_DICOM'

        p1 = Path(p1)
        p1.mkdir(parents=True, exist_ok=True)
        # dp = io3d.read(f_name)
        # output_f = p1 / (f_name.stem + output_format)
        # io3d.write(dp, output_f)

        p2 = Path(p2)
        p2.mkdir(parents=True, exist_ok=True)
        # dp = io3d.read(f_name)
        # output_f = p2 / (f_name.stem + output_format)
        # io3d.write(dp, output_f)

        p3 = Path(p3)
        p3.mkdir(parents=True, exist_ok=True)
        dp = io3d.read(f_name)
        output_f = p3 / (f_name.stem + '.vkt')
        io3d.write(dp, output_f)

        p4 = Path(p4)
        p4.mkdir(parents=True, exist_ok=True)
        dp = io3d.read(f_name)
        output_f = p4 / (f_name.stem + output_format)
        logger.debug(f"writiong into {output_f}")
        io3d.write(dp, output_f)

        #     p4 = Path(p4)
        #     p4.parent.mkdir(parents=True, exist_ok=True)

        i = i + 1

    pass



#  Hello

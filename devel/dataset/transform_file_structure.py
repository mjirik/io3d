


def prepare_pilsen_pigs_dataset(input_dir, output_dir, input_mask='*_Ven*', start_index = 0, output_format=".mhd"):
    """
    input_dir: vstupni cesta
    output_dir: vystup. cesta
    input_mask: cast nazvu zvol. souboru (pro fci. glob)
    start_index: cislo od ktereho zacneme vytvaret slozky
    """

    import io3d
    from pathlib import Path
    import SimpleITK

    # ukladani obsahu slozek
    file_list = list(input_dir.glob(input_mask))
    for f_name in file_list:
        p = output_dir/ f'pig_{start_index:04d}'


        p1 = p /'LABELED_DICOM'
        p2 = p / 'MASKS_DICOM'
        p3 = p / 'MESHES_VTK'
        p4 = p / 'PATIENT_DICOM'

        p1 = Path(p1)
        p1.mkdir(parents=True, exist_ok=True)

        dp = io3d.read(f_name)
        output_f = p1 / (f_name.stem + output_format)
        io3d.write(dp, output_f)

        p2 = Path(p2)
        p2.mkdir(parents=True, exist_ok=True)

        dp = io3d.read(f_name)
        output_f = p2 / (f_name.stem + output_format)
        io3d.write(dp, output_f)

        p3 = Path(p3)
        p3.mkdir(parents=True, exist_ok=True)

        dp = io3d.read(f_name)
        output_f = p3 / (f_name.stem + output_format)
        io3d.write(dp, output_f)

        p4 = Path(p4)
        p4.mkdir(parents=True, exist_ok=True)

        dp = io3d.read(f_name)
        output_f = p4 / (f_name.stem + output_format)
        io3d.write(dp, output_f)

        #     p4 = Path(p4)
        #     p4.parent.mkdir(parents=True, exist_ok=True)

        start_index = start_index + 1

    pass



#  Hello

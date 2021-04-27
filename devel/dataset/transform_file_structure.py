


def prepare_pilsen_pigs_dataset(input_dir, output_dir, output_format=".mhd"):
    # from google_drive_downloader import GoogleDriveDownloader as gdd
    import io3d
    from pathlib import Path
    import SimpleITK

    # teoretické načtení složky T040
    imput_dir = Path(r'G:\.shortcut-targets-by-id\1Vq6QAiJ7cHDJUdgKXjUxx5iw7zk6MMPI\transplantation')
    dp = io3d.read(list(imput_dir.glob('*040D_V*'))[0])
    f_name = list(imput_dir.glob('*040D_V*'))[0]

    output_dir = Path(r'G:\.shortcut-targets-by-id\1nz7i4Zssar8075yu6J5QpHdph6oi3uF8\pilsen_pigs')
    io3d.write({'data3d': np.zeros([10, 10, 10])}, output_dir / 'pokus.pklz')

    # ukladani obsahu slozek
    k = 0
    file_list = list(p.glob('*04?D_V*'))
    for f_name in file_list:
        p = str(r'C:\Users\janar\data\biomedical\orig\Pilsen_pigs\pig_')
        p = p + str(k)
        print(p)

        p1 = p + '\LABELED_DICOM'
        p2 = p + '\MASKS_DICOM'
        p3 = p + '\MESHES_VTK'
        p4 = p + '\PATIENT_DICOM'

        p1 = Path(p1)
        p1.mkdir(parents=True, exist_ok=True)

        dp = io3d.read(f_name)
        output_f = p1 / (f_name.stem + '.mhd')
        io3d.write(dp, output_f)

        p2 = Path(p2)
        p2.mkdir(parents=True, exist_ok=True)

        dp = io3d.read(f_name)
        output_f = p2 / (f_name.stem + '.mhd')
        io3d.write(dp, output_f)

        p3 = Path(p3)
        p3.mkdir(parents=True, exist_ok=True)

        dp = io3d.read(f_name)
        output_f = p3 / (f_name.stem + '.mhd')
        io3d.write(dp, output_f)

        p4 = Path(p4)
        p4.mkdir(parents=True, exist_ok=True)

        dp = io3d.read(f_name)
        output_f = p4 / (f_name.stem + '.mhd')
        io3d.write(dp, output_f)

        #     p4 = Path(p4)
        #     p4.parent.mkdir(parents=True, exist_ok=True)

        k = k + 1
    print(k)

    pass



#  Hello

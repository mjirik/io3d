


def prepare_pilsen_pigs_dataset(input_dir, output_dir, output_format=".mhd"):
    # from google_drive_downloader import GoogleDriveDownloader as gdd
    import io3d
    from pathlib import Path
    import SimpleITK

    # teoretické načtení složky T040
    imput_dir = Path(r'G:\.shortcut-targets-by-id\1Vq6QAiJ7cHDJUdgKXjUxx5iw7zk6MMPI\transplantation')
    dp = io3d.read(list(imput_dir.glob('*040D_V*'))[0])
    f_name = list(imput_dir.glob('*040D_V*'))[0]

    pass



#  Hello

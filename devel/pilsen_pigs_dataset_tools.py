from pathlib import Path
import io3d
from loguru import logger
import json
import tqdm
import traceback
from typing import Union
import numpy as np
import pandas as pd


def get_series_description(dcm_info, series_number):
    series_description = ""
    if "SeriesDescription" in dcm_info:
        series_description = " " + dcm_info["SeriesDescription"]

    return str(series_number) + series_description

def get_stats_of_series_in_dir(dir_path:str):
    dicomdirectory = io3d.dcmreaddata.DicomDirectory(
        str(dir_path)
    )
    return dicomdirectory.get_stats_of_series_in_dir()

def get_stats_of_series_in_dir_nice_list(current_fn, debug=False) -> list:
    series_metadata = get_stats_of_series_in_dir(current_fn)
    for kkey in series_metadata:
        if "dcmfilelist" in series_metadata[kkey]:
            # dir_info = series_metadata
            series_metadata[kkey]["dcmfilelist_len"] = len(series_metadata[kkey]["dcmfilelist"])
            series_metadata[kkey]["dcmfilelist"] = None
        if "SeriesNumber" in series_metadata[kkey]:
            series_metadata[kkey]["SeriesNumber"] = int(series_metadata[kkey]["SeriesNumber"])
        if "Count" in series_metadata[kkey]:
            series_metadata[kkey]["Count"] = int(series_metadata[kkey]["Count"])
        if 'PatientName' in series_metadata[kkey]:
            series_metadata[kkey]["PatientName"] = str(series_metadata[kkey]["PatientName"])
        # check if is json serializable
        series_metadata[kkey]["Path"] = str(current_fn)
        if debug:
            for kkk in series_metadata[kkey].keys():
                logger.debug(f"{kkk}:{type(kkk)}   = {series_metadata[kkey][kkk]}: {type(series_metadata[kkey][kkk])}")
            # logger.debug(series_metadata[kkey].keys())
            # logger.debug(series_metadata[kkey].values())
            series_metadata_list = list(series_metadata.values())
            logger.debug(series_metadata_list)
    series_metadata_list = list(series_metadata.values())
    return series_metadata_list


def get_projection(
        datap:io3d.image.DataPlus, axis:Union[int,str], method:str="max"
):
    """Get projection of 3D data to 2D."""
    if isinstance(axis, str):
        dict_axis = {"axial": 0, "coronal": 1, "sagittal": 2}
        if axis in dict_axis:
            axis = dict_axis[axis]
        else:
            raise ValueError(f"Unknown axis {axis}, use one of {list(dict_axis.keys())} or 0, 1, 2")

    data3d = datap.data3d
    axcodes = datap.orientation_axcodes
    data3d = io3d.image.transform_orientation(data3d, axcodes, "SPL")
    if method == "max":
        data2d = data3d.max(axis=axis)
    elif method == "mean":
        data2d = data3d.mean(axis=axis)
    else:
        raise ValueError(f"Unknown method {method}")
    return data2d


def create_one_file_from_one_dicom_dir(
        fnlist:list,
        base_path:Path,
        fn_prefix:str,
        output_path:Path,
        force:bool=True,
        force_rewrite:bool=False
):


    print(f"Number of leaf dirs: {len(fnlist)}")
    from joblib import Parallel, delayed
    #
    stats_subset = []
    for fn in tqdm.auto.tqdm(fnlist[:]):
        # iterate over series

        # dir_info = io3d.dcmreaddata.dicomdir_info(fn, gui=False)
        tqdm.tqdm.write(f"Dir {fn}:")
        dir_info = get_stats_of_series_in_dir(fn)
        # for series_number in dir_info.keys():
        #     if 'Count' in dir_info[series_number]:
        #         tqdm.tqdm.write(f"  Series {series_number} with {dir_info[series_number]['Count']} files.")
        #     else:
        #         tqdm.tqdm.write(f'{dir_info[series_number].keys()=}')

        for series_number in dir_info.keys():
            if series_number == None:
                series_number = "first"
            # series_description = get_series_description(dir_info, series_number).replace(" ", "_")



            count = int(dir_info[series_number]["Count"]) if "Count" in dir_info[series_number] else 0

            info_str = ""
            try:
                if "voxelsize_mm" in dir_info[series_number]:
                    vs_0 = dir_info[series_number]["voxelsize_mm"][0]
                    # print(f"{dir_info[series_number]["voxelsize_mm"]=}")
                    info_str += f"{vs_0:.2f}"
            except Exception as e:
                tqdm.tqdm.write(f"voxelsize problem")
                tqdm.tqdm.write(traceback.format_exc())
            try:
                if 'SeriesDescription' in dir_info[series_number]:
                    series_description = str(dir_info[series_number]["SeriesDescription"])
                    series_description = series_description.replace(" ", "_").replace("(", "_").replace(")", "_")
                    series_description_lower = series_description.lower()
                    info_str += f"_{series_description_lower}"[:35]
                if 'StudyDescription' in dir_info[series_number]:
                    study_description = str(dir_info[series_number]["StudyDescription"])
                    study_description = study_description.replace(" ", "_").replace("(", "_").replace(")", "_")
                    study_description_lower = study_description.lower()
                    info_str += f"_{study_description_lower}"[:35]
            except Exception as e:
                tqdm.tqdm.write(f"study description problem")
                tqdm.tqdm.write(traceback.format_exc())

            # i want to have there the parent directory
            # fn_name = str(fn.relative_to(base_path)).replace("\\", "-").replace("/", "-")
            fn_name = (fn_prefix + str(fn.relative_to(base_path))).replace("\\", "-").replace("/", "-").replace(" ", "_")
            fn_name += f"_N{count:03d}"
            fn_name += f"_{series_number:02d}"
            if info_str != "":
                fn_name += "_"
                fn_name += info_str

            # logger.info(fn)
            fn_in = fn
            # fn_out = raw_path / fn.name / f"{fn.name}.mhd"
            fn_out = output_path / fn_name / f"{fn_name}.nii.gz"
            if fn_out.exists() and not force_rewrite:
                tqdm.tqdm.write(f"File {fn_out.name} already exists. skipping.")
                continue

            fn_meta = fn_out.parent / "meta.json"
            if force or (not fn_out.exists()):
                # if count of files is lower than 2, skip
                if dir_info[series_number]["Count"] <2:
                    continue


                try:
                    # tqdm.tqdm.write(f"Reading series {series_number} with {dir_info[series_number]["Count"]} files in {fn_in} and writing {fn_out}")
                    # tqdm.tqdm.write(f"Number of files in the directory: {len(fn_fns)}")
                    # Parallel(n_jobs=2)(delayed(touch_file)(fn) for fn in tqdm.tqdm(fn_fns, desc="touching files"))

                    axcodes = "IPL"
                    # logger.debug(f"Reading {fn_in} with axcodes={axcodes}")
                    datap = io3d.read(fn_in,
                                      # series_number="first",
                                      series_number=series_number,
                                      orientation_axcodes=axcodes)
                    # logger.debug(datap.keys())
                    fn_out.parent.mkdir(parents=True, exist_ok=True)
                    io3d.write(datap, fn_out)
                    # logger.debug("writing done, creating projections")
                    for axis in ["axial", "coronal", "sagittal"]:
                        data2d = get_projection(datap, axis, "max")
                        import skimage.io
                        # change intensity to range 0..1
                        data2d = data2d.astype(float)
                        data2d_min = np.min(data2d)
                        data2d_max = np.max(data2d)
                        data2d = (255 * (data2d - data2d_min) / (data2d_max - data2d_min))
                        data2d = data2d.astype(np.uint8)
                        skimage.io.imsave(fn_out.parent / f"{fn_out.stem}_{axis}.jpg", data2d)

                    stats_i = get_stats_of_series_in_dir_nice_list(fn_in)
                    stats_subset.extend(stats_i)
                    try:
                        with open(fn_out.parent / f"{fn_out.stem}_stats.json", "w") as f:
                            json.dump(stats_i, f)
                    except TypeError as e:
                        tqdm.tqdm.write(f"Error in JSON export {fn_in}: {e}")
                        tqdm.tqdm.write(traceback.format_exc())
                        tqdm.tqdm.write(str(stats_i))
                        get_stats_of_series_in_dir_nice_list(fn_in, debug=True)

                    # logger.debug("projections done")
                except Exception as e:
                    import traceback
                    tqdm.tqdm.write(f"Error in reading {fn_in}: {e}")
                    tqdm.tqdm.write(traceback.format_exc())
                if len(list(fn_out.parent.glob("*"))) == 0:
                    fn_out.parent.rmdir()
                    # logger.debug(f"shape={datap.data3d.shape}, {datap.orientation_axcodes}")
                # with open(fn_meta, "w") as f:
                #     json.dump(dict(row), f)


    df_subset = pd.DataFrame(stats_subset)
    df_subset.to_csv(base_path / "meta.csv", index=False)


from pathlib import Path
import pandas as pd
import numpy as np
import io3d

def save_projections_in_image_files(
        datap:io3d.image.DataPlus,
        out_path:Path):
    """Saves axial, coronal and sagittal projections of 3D data to 2D images."""
    for axis in ["axial", "coronal", "sagittal"]:
        data2d = get_projection(datap, axis, "max")
        import skimage.io
        # change intensity to range 0..1
        data2d = data2d.astype(float)
        data2d_min = np.min(data2d)
        data2d_max = np.max(data2d)
        data2d = (255 * (data2d - data2d_min) / (data2d_max - data2d_min))
        data2d = data2d.astype(np.uint8)
        skimage.io.imsave(out_path.parent / f"{out_path.stem}_{axis}.jpg", data2d)


def merge_several_dirs_with_one_series(
        g, out_fn,
        save_projections=True,
        min_slices=5
):
    """Merge already-selected group of rows (one StudyID + SeriesNumber)."""

    # logger.debug(f"Merging series  {g=}")
    logger.debug(f"  to {out_fn=}")

    if len(g) == 0:
        logger.warning("Group is empty → no data")
        return
        # raise ValueError("Group is empty → no data")
    if g.Count.sum() < min_slices:
        logger.warning(f"Not enough slices to merge (<{min_slices}, have {g.Count.sum()})")
        return
    try:


        g_sorted = g.sort_values("SliceLocation", ascending=False)
        # print(f"length of g_sorted: {len(g_sorted)}")

        volumes = []
        datap = None

        # Read volumes in order
        for _, row in g_sorted.iterrows():
            d = io3d.read(row["Path"], series_number=row["SeriesNumber"])
            if datap is None:
                datap = d  # this copies metadata
            volumes.append(d["data3d"])

        # Merge along Z axis
        data3d_merged = np.concatenate(volumes, axis=0)
        datap["data3d"] = data3d_merged

        # Save nii.gz
        Path(out_fn).parent.mkdir(parents=True, exist_ok=True)
        io3d.write(datap, out_fn)

        # Optional projections
        if save_projections:
            logger.debug("Saving projections...")
            # print("Saving projections...")
            save_projections_in_image_files(datap, out_fn)
            # save_projections_in_image_files

        # Save stats from first directory
        fn_first = g_sorted.iloc[0]["Path"]
        stats_i = get_stats_of_series_in_dir_nice_list(fn_first)
        stats_i[0]["Count"] = int(data3d_merged.shape[0])
        stats_i[0]["Paths"] = ",".join(g.Path)
        with open(Path(out_fn).parent / f"{Path(out_fn).stem}_stats.json", "w") as f:
            json.dump(stats_i, f)

        logger.debug(f"Saved merged volume: {out_fn}")
    except Exception as e:
        logger.error(f"Error in merging series to {out_fn}: {e}")
        logger.error(traceback.format_exc())
        raise e




# def merge_series(df, study_id, series_number, out_fn,
#                  save_projections=True):
#     """Sloučí více adresářů stejného StudyID + SeriesNumber do jednoho NIfTI."""
#
#     # get group
#     g = df[(df.StudyID == study_id) & (df.SeriesNumber == series_number)]
#     if len(g) == 0:
#         raise ValueError("No data for this StudyID+SeriesNumber")
#
#     # sort by SliceLocation
#     g_sorted = g.sort_values("SliceLocation")
#
#     volumes = []
#     datap = None
#
#     for _, row in g_sorted.iterrows():
#         d = io3d.read(row["Path"], series_number=row["SeriesNumber"])
#         if datap is None:
#             datap = d  # copy full metadata
#         volumes.append(d["data3d"])
#
#     # merge along z
#     data3d_merged = np.concatenate(volumes, axis=0)
#
#     # update metadata
#     datap["data3d"] = data3d_merged
#     # meta_first["MergedSlices"] = len(data3d_merged)
#     # meta_first["Subdirs"] = list(g_sorted["Path"])
#
#     Path(out_fn).parent.mkdir(parents=True, exist_ok=True)
#
#     io3d.write(datap, out_fn)
#     if save_projections:
#         save_projections_in_image_files(datap, out_fn)
#
#     fn_first = g_sorted.iloc[0]["Path"]
#     stats_i = get_stats_of_series_in_dir_nice_list(fn_first)
#     try:
#         with open(Path(out_fn).parent / f"{Path(out_fn).stem}_stats.json", "w") as f:
#             json.dump(stats_i, f)
#     except TypeError as e:
#         logger.error(f"Error in JSON export {fn_first}: {e}")
#         logger.error(traceback.format_exc())
#         logger.error(str(stats_i))
#         get_stats_of_series_in_dir_nice_list(fn_first, debug=True)
#     print(f"Saved merged volume: {out_fn}")



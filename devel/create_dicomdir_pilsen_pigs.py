import io3d
from pathlib import Path
from loguru import logger
from pprint import pprint, pformat
import pandas as pd
import re
import json

logger.enable("io3d")

base_path = Path(r"H:\biomedical\orig\pilsen_pigs_raw\transplantation")
output_path = Path(r"H:\biomedical\orig\pilsen_pigs")

metafn = base_path / "meta.csv"

if metafn.exists():
    df = pd.read_csv(metafn)
else:
    df = pd.DataFrame()


def create_meta(base_path, metafn):
    data = {
        "dirname": [],
        "dataset_type": [],
        "id": [],
    }
    i_train = 0
    i_test = 0
    i_val = 0
    fnlist = base_path.glob("*Tx0*D_V*")
    logger.info(pformat(list(map(str, list(fnlist)))))
    fnlist = base_path.glob("*Tx0*D_V*")
    for fn in fnlist:
        ia = int(re.findall(r"([0-9]+)", fn.name)[0])
        ii = None
        tp = None
        if (ia % 4) == 0:
            i_test += 1
            ii = i_test
            tp = "test"
        elif (ia % 2) == 0:
            i_val += 1
            ii = i_val
            tp = "val"
        else:
            i_train += 1
            ii = i_train
            tp = "train"

        data["dirname"].append(fn.name)
        data["dataset_type"].append(tp)
        data["id"].append(ii)

    df = pd.DataFrame(data)
    df.to_csv(metafn, index=None)


create_meta(base_path, metafn)


df = pd.read_csv(metafn)
print(df)
# fnlist = base_path.glob("*debug*")
# fnlist = base_path.glob("*Tx041D_V*")


for i, row in df.iterrows():
    fn_in = base_path / row["dirname"]
    fn_out = (
        output_path
        / row["dataset_type"]
        / f"PP_{row['id']:04}"
        / "PATIENT_DICOM"
        / f"PP_{row['id']:04}.mhd"
    )
    fn_meta = fn_out.parent / "meta.json"
    logger.debug(fn_in)
    logger.debug(fn_out)

    fn_out.parent.mkdir(parents=True, exist_ok=True)
    if (
        not fn_meta.exists()
    ):  # we do not need to read the data again if everything is done. We are checkin:w

        datap = io3d.read(fn_in)
        io3d.write(datap, fn_out)
        with open(fn_meta, "w") as f:
            json.dump(dict(row), f)


# # preprocessing for to prepare dicomdir.pkl to every directory
# for fn in fnlist:
#     logger.debug(f"{fn}")
#     if not (fn / "dicomdir.pkl").exists():
#         try:
#             io3d.read(str(fn))
#         except Exception as e:
#             logger.warning(e)
#         # io3d.read(fn)
#
#         logger.debug(f"{(fn /'dicomdir.pkl').exists()}")


# for fn in fnlist:
#     logger.debug(f"{fn}")
#     if not (fn / "dicomdir.pkl").exists():
#         try:
#             io3d.read(str(fn))
#         except Exception as e:
#             logger.warning(e)
#         # io3d.read(fn)
#
#         logger.debug(f"{(fn /'dicomdir.pkl').exists()}")

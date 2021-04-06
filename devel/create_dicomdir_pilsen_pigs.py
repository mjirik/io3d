import io3d
from pathlib import Path
from loguru import logger
logger.enable("io3d")

base_path = Path(r'H:\biomedical\orig\pilsen_pigs_raw\transplantation')

# fnlist = base_path.glob("*debug*")
fnlist = base_path.glob("*Tx041D_V*")

for fn in fnlist:
    if not (fn / "dicomdir.pkl").exists():
        logger.debug(f"{fn}")
        io3d.read(str(fn))
        # io3d.read(fn)

        logger.debug(f"{(fn /'dicomdir.pkl').exists()}")


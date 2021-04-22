import io3d
from pathlib import Path
from loguru import logger
logger.enable("io3d")

base_path = Path(r'H:\biomedical\orig\pilsen_pigs_raw\transplantation')

# fnlist = base_path.glob("*debug*")
# fnlist = base_path.glob("*Tx041D_V*")
fnlist = base_path.glob("*Tx0*D_V*")

for fn in fnlist:
    logger.debug(f"{fn}")
    if not (fn / "dicomdir.pkl").exists():
        try:
            io3d.read(str(fn))
        except Exception as e:
            logger.warning(e)
        # io3d.read(fn)

        logger.debug(f"{(fn /'dicomdir.pkl').exists()}")


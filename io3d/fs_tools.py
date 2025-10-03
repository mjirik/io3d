from pathlib import Path
from typing import Union
from joblib import Parallel, delayed


def get_leaf_dirs_with_files(base_path:Union[Path, str], with_tqdm:bool=True) -> list[Path]:


    first_layer_dirs = [p for p in base_path.glob("*") if p.is_dir()]

    if with_tqdm:
        import tqdm.auto
        progress = tqdm.auto.tqdm(first_layer_dirs, desc="Checking first layer dirs")
    leaf_dirs = []


    for first_layer_dir in first_layer_dirs:

        # List all directories under base_path (recursively)
        all_dirs = list(first_layer_dir.rglob("*"))
        # all_dirs = [p for p in first_layer_dir.rglob("*") if p.is_dir()]

        if all_dirs:
            update_fraction = 1. / len(all_dirs) if all_dirs else 1.0
            for d in all_dirs:
                if d.is_dir():
                    has_subdir = False
                    has_file = False
                    for child in d.iterdir():
                        if child.is_dir():
                            has_subdir = True
                            break
                        elif child.is_file():
                            has_file = True

                    # children = list(d.iterdir())
                    # has_subdir = any(child.is_dir() for child in children)
                    # if has_subdir:
                    #     progress.update(update_fraction)
                    #     continue
                    # has_file = any(child.is_file() for child in children)
                    if not has_subdir and has_file:
                        leaf_dirs.append(d)
                if with_tqdm:
                    progress.update(update_fraction)
        else:
            if with_tqdm:
                progress.update(1.)
    return leaf_dirs


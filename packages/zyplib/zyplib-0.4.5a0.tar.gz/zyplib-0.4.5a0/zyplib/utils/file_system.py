import os
import shutil
from typing import Literal

from .print import debug


def ensure_dir(dir: str, if_not_empty: Literal['keep', 'clean', 'error'] = 'keep'):
    """检查用于保存日志、Checkpoint 等的目录如果 dir 不存在，则创建

    Parameters
    ----------
    - `dir` : `str`
        - 目录
    - `if_not_empty` : `Literal['keep', 'clean', 'error']`, optional
        - 如果目录不为空，则执行的操作
        - `"keep"` | `"clean"` | `"error"`
    """
    if not os.path.exists(dir):
        os.makedirs(dir)
    elif any(os.scandir(dir)):
        if if_not_empty is None or if_not_empty == 'keep':
            debug(f'Exists: {dir}!')
        elif if_not_empty == 'clean':
            debug(f'Clean up: {dir}!')
            shutil.rmtree(dir)
            os.makedirs(dir)
        elif if_not_empty == 'error':
            raise Exception(f'目录 {dir} 不为空!')
        else:
            raise ValueError(f'check_dir 参数错误: if_not_empty = {if_not_empty}')

import os
import sys

# 将项目根目录加入 sys.path，确保 'app' 可被测试导入
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
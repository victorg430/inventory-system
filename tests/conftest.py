import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)                                       # for `import app`
sys.path.insert(0, os.path.join(ROOT, "API"))                   # for `import external_api`
sys.path.insert(0, os.path.join(ROOT, "API", "intergration"))   # for `import cli`

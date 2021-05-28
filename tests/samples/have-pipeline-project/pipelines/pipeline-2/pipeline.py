import sys
sys.path.append("../..")

import kfp

@kfp.dsl.pipeline(name="pipeline-2")
def pipeline():
    pass

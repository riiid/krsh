import sys
sys.path.append("../..")

import kfp


@kfp.dsl.pipeline(name="pipeline-1")
def pipeline():
    pass

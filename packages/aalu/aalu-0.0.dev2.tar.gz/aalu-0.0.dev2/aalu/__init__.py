"""
Implements all global variables
"""

import os
import multiprocessing

# Determines how many workers to run the common multiprocessing pool with
# If the AALU_LOCAL_WORKERS is not set, uses 1
# If the AALU_LOCAL_WORKERS is set to <=0, uses all available CPUs
# Otherwise, uses the value of AALU_LOCAL_WORKERS

LOCAL_WORKERS = max(
    int(os.environ.get("AALU_LOCAL_WORKERS", 1)), multiprocessing.cpu_count()
)

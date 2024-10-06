#!/bin/bash
# This script is meant to be called by the "install" step defined in
# build.yml. The behavior of the script is controlled by environment 
# variables defined in the build.yml in .github/workflows/.

set -e

conda config --set remote_connect_timeout_secs 30.0
conda config --set remote_max_retries 10
conda config --set remote_backoff_factor 2
conda config --set remote_read_timeout_secs 120.0

if [[ "$PYTHON_VERSION" == "3.8" ]] && [[ "$RUNNER_OS" == "macos-11" ]]; then
  conda install scipy=1.3 numpy=1.18 mkl pip pytest pytest-cov lapack ecos scs osqp cvxopt proxsuite "setuptools>68.1.0" pybind11
elif [[ "$PYTHON_VERSION" == "3.8" ]]; then
  conda install scipy=1.3 numpy=1.18 mkl pip pytest pytest-cov lapack ecos scs osqp cvxopt proxsuite "setuptools>68.1.0" pybind11
elif [[ "$PYTHON_VERSION" == "3.9" ]]; then
  # The earliest version of numpy that works is 1.19.
  # Given numpy 1.19, the earliest version of scipy we can use is 1.5.
  conda install scipy=1.5 numpy=1.19 mkl pip pytest lapack ecos scs osqp cvxopt proxsuite "setuptools>68.1.0" pybind11
elif [[ "$PYTHON_VERSION" == "3.10" ]]; then
    # The earliest version of numpy that works is 1.21.
    # Given numpy 1.21, the earliest version of scipy we can use is 1.7.
    conda install scipy=1.7 numpy=1.21 mkl pip pytest lapack ecos scs osqp cvxopt proxsuite "setuptools>68.1.0" pybind11
elif [[ "$PYTHON_VERSION" == "3.11" ]]; then
    # The earliest version of numpy that works is 1.23.4.
    # Given numpy 1.23.4, the earliest version of scipy we can use is 1.9.3.
    conda install scipy=1.9.3 numpy=1.23.4 mkl pip pytest lapack ecos scs cvxopt proxsuite "setuptools>68.1.0" pybind11
elif [[ "$PYTHON_VERSION" == "3.12" ]]; then
    # The earliest version of numpy that works is 1.26.4
    # Given numpy 1.26.4, the earliest version of scipy we can use is 1.9.3.
    conda install scipy=1.11.3 numpy=1.26.4 mkl pip pytest lapack ecos scs cvxopt proxsuite daqp "setuptools>68.1.0" pybind11
fi

if [[ "$PYTHON_VERSION" == "3.12" ]]; then
  python -m pip install coptpy gurobipy piqp osqp clarabel
elif [[ "$PYTHON_VERSION" == "3.11" ]]; then
  python -m pip install coptpy gurobipy cplex piqp osqp diffcp "ortools>=9.7,<9.10" clarabel
# Python 3.8 on Windows will uninstall NumPy 1.16 and install NumPy 1.24 without the exception.
elif [[ "$RUNNER_OS" == "Windows" ]] && [[ "$PYTHON_VERSION" == "3.8" ]]; then
  python -m pip install gurobipy clarabel osqp 
elif [[ "$PYTHON_VERSION" == "3.8" ]] && [[ "$RUNNER_OS" != "macos-11" ]]; then
  python -m pip install gurobipy clarabel piqp
else
  python -m pip install "ortools>=9.3,<9.10" coptpy sdpa-python diffcp gurobipy clarabel sdpa-python
fi

# cylp has wheels for all versions 3.7 - 3.10, except for 3.7 on Windows
if [[ "$PYTHON_VERSION" != "3.11" ]] && [[ "$RUNNER_OS" != "Windows" ]]; then
  python -m pip install cylp
fi

# SCIP only works with scipy >= 1.5 due to dependency conflicts when installing on Linux/macOS
if [[ "$PYTHON_VERSION" == "3.9" ]] && [[ "$RUNNER_OS" == "Windows" ]]; then
  conda install pyscipopt
fi

# Only install Mosek if license is available (secret is not copied to forks)
if [[ -n "$MOSEK_CI_BASE64" ]] && [[ "$PYTHON_VERSION" != "3.11" ]]; then
    python -m pip install mosek
fi

if [[ "$USE_OPENMP" == "True" ]]; then
  conda install -c conda-forge openmp
fi

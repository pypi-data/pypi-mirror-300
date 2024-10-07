use furiosa_smi_rs::SmiError;
use pyo3::{exceptions::PyRuntimeError, PyErr};

pub(crate) fn to_py_err(err: SmiError) -> PyErr {
    PyRuntimeError::new_err(err.to_string())
}

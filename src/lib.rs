use std::{io, path::PathBuf};

use pyo3::prelude::*;
use pyo3::{
    create_exception,
    exceptions::{PyException, PyUnicodeError, PyValueError},
};

create_exception!(
    paqpy,
    PaqError,
    PyException,
    "Fallback error raised when paq cannot hash a source."
);

#[pyfunction]
#[pyo3(name = "hash_source")]
fn hash_source(py: Python<'_>, source: PathBuf, ignore_hidden: bool) -> PyResult<String> {
    py.detach(|| paq::try_hash_source(&source, ignore_hidden))
        .map(|hash| hash.to_string())
        .map_err(paq_error_to_py)
}

fn paq_error_to_py(error: paq::Error) -> PyErr {
    let message = error.to_string();

    match error {
        paq::Error::Io { source, .. } => io_error_to_py(source.kind(), message),
        paq::Error::Walk(source) => source
            .io_error()
            .map(|error| io_error_to_py(error.kind(), message.clone()))
            .unwrap_or_else(|| PaqError::new_err(message)),
        paq::Error::InvalidUtf8Path(_) => PyUnicodeError::new_err(message),
        paq::Error::OutsideSource { .. } => PyValueError::new_err(message),
        _ => PaqError::new_err(message),
    }
}

fn io_error_to_py(kind: io::ErrorKind, message: String) -> PyErr {
    io::Error::new(kind, message).into()
}

#[pymodule]
fn paqpy(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("PaqError", m.py().get_type::<PaqError>())?;
    m.add_function(wrap_pyfunction!(hash_source, m)?)?;
    Ok(())
}

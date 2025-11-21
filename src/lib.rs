use std::path::Path;

use pyo3::prelude::*;


#[pyfunction]
#[pyo3(name = "hash_source")]
fn hash_source(py: Python<'_>, source: String, ignore_hidden: bool) -> String {
    // py.allow_threads releases the Global Interpreter Lock (GIL).
    // allows Python to do other things while paq executes.
    py.allow_threads(|| {
        let path = Path::new(&source);
        // 'paq' returns an ArrayString and must be converted to a standard String
        paq::hash_source(path, ignore_hidden).to_string()
    })
}

#[pymodule]
fn paqpy(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hash_source, m)?)?;
    Ok(())
}

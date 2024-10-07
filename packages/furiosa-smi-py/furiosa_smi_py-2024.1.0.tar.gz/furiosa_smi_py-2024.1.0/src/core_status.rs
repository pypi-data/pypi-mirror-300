use furiosa_smi_rs::CoreStatus;
use pyo3::{pyclass, pymethods};

#[pyclass(name = "CoreStatus")]
#[derive(Clone)]
/// Represents a core status
pub enum CoreStatusPy {
    /// When a core is available.
    Available = CoreStatus::Available as isize,

    /// When a core is occupied.
    Occupied = CoreStatus::Occupied as isize,
}

impl From<CoreStatus> for CoreStatusPy {
    fn from(core_status: CoreStatus) -> Self {
        match core_status {
            CoreStatus::Available => CoreStatusPy::Available,
            CoreStatus::Occupied => CoreStatusPy::Occupied,
        }
    }
}

#[pymethods]
impl CoreStatusPy {
    fn __str__(&self) -> String {
        match self {
            CoreStatusPy::Available => "available",
            CoreStatusPy::Occupied => "occupied",
        }
        .to_string()
    }
}

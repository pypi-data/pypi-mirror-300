use furiosa_smi_rs::DeviceFile;
use pyo3::pyclass;
use pyo3::pymethods;
use std::sync::Arc;

#[pyclass(name = "DeviceFile")]
#[derive(Clone)]
/// A struct for device file
pub struct DeviceFilePy {
    pub inner: Arc<DeviceFile>,
}

impl DeviceFilePy {
    pub(crate) fn new(dev_file: DeviceFile) -> Self {
        Self {
            inner: Arc::new(dev_file),
        }
    }
}

#[pymethods]
impl DeviceFilePy {
    /// Get a list of core for device file
    fn cores(&self) -> Vec<u32> {
        self.inner.cores()
    }

    /// Get a device file path
    fn path(&self) -> String {
        self.inner.path()
    }
}

use furiosa_smi_rs::DeviceErrorInfo;
use pyo3::pyclass;
use pyo3::pymethods;
use std::sync::Arc;

#[pyclass(name = "DeviceErrorInfo")]
#[derive(Clone)]
/// A struct for device error information
pub struct DeviceErrorInfoPy {
    inner: Arc<DeviceErrorInfo>,
}

impl DeviceErrorInfoPy {
    pub(crate) fn new(dev_error_info: DeviceErrorInfo) -> Self {
        Self {
            inner: Arc::new(dev_error_info),
        }
    }
}

#[pymethods]
impl DeviceErrorInfoPy {
    /// Get a axi post error count
    pub fn axi_post_error_count(&self) -> u32 {
        self.inner.axi_post_error_count()
    }

    /// Get a axi fetch error count
    pub fn axi_fetch_error_count(&self) -> u32 {
        self.inner.axi_fetch_error_count()
    }

    /// Get a axi discard error count
    pub fn axi_discard_error_count(&self) -> u32 {
        self.inner.axi_discard_error_count()
    }

    /// Get a axi doorbell error count
    pub fn axi_doorbell_error_count(&self) -> u32 {
        self.inner.axi_doorbell_error_count()
    }

    /// Get a pcie post error count
    pub fn pcie_post_error_count(&self) -> u32 {
        self.inner.pcie_post_error_count()
    }

    /// Get a pcie fetch error count
    pub fn pcie_fetch_error_count(&self) -> u32 {
        self.inner.pcie_fetch_error_count()
    }

    /// Get a pcie discard error count
    pub fn pcie_discard_error_count(&self) -> u32 {
        self.inner.pcie_discard_error_count()
    }

    /// Get a pcie doorbell error count
    pub fn pcie_doorbell_error_count(&self) -> u32 {
        self.inner.pcie_doorbell_error_count()
    }

    /// Get a device error count
    pub fn device_error_count(&self) -> u32 {
        self.inner.device_error_count()
    }
}

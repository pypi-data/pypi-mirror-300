use crate::types::ArchPy;
use crate::version::VersionInfoPy;
use furiosa_smi_rs::DeviceInfo;
use pyo3::pyclass;
use pyo3::pymethods;
use std::sync::Arc;

#[pyclass(name = "DeviceInfo")]
#[derive(Clone)]
/// A struct for device information
pub struct DeviceInfoPy {
    pub inner: Arc<DeviceInfo>,
}

impl DeviceInfoPy {
    pub(crate) fn new(dev_info: DeviceInfo) -> Self {
        Self {
            inner: Arc::new(dev_info),
        }
    }
}

#[pymethods]
impl DeviceInfoPy {
    /// Get a architecture of device
    fn arch(&self) -> ArchPy {
        self.inner.arch().into()
    }

    /// Get a number of cores
    fn core_num(&self) -> u32 {
        self.inner.core_num()
    }

    /// Get a numa node of device
    fn numa_node(&self) -> u32 {
        self.inner.numa_node()
    }

    /// Get a name of device
    fn name(&self) -> String {
        self.inner.name()
    }

    /// Get a serial of device
    fn serial(&self) -> String {
        self.inner.serial()
    }

    /// Get a uuid of device
    fn uuid(&self) -> String {
        self.inner.uuid()
    }

    /// Get a bdf of device
    fn bdf(&self) -> String {
        self.inner.bdf()
    }

    /// Get a major part of pci device
    fn major(&self) -> u16 {
        self.inner.major()
    }

    /// Get a minor part of pci device
    fn minor(&self) -> u16 {
        self.inner.minor()
    }

    /// Get a firmware version of device
    fn firmware_version(&self) -> VersionInfoPy {
        VersionInfoPy::new(self.inner.firmware_version())
    }

    /// Get a driver version of device
    fn driver_version(&self) -> VersionInfoPy {
        VersionInfoPy::new(self.inner.driver_version())
    }
}

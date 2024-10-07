use crate::core_status::CoreStatusPy;
use crate::device::DevicePy;
use crate::device_error_info::DeviceErrorInfoPy;
use crate::device_file::DeviceFilePy;
use crate::device_info::DeviceInfoPy;
use crate::error::to_py_err;
use crate::performance::{DeviceUtilizationPy, MemoryUtilizationPy, PeUtilizationPy};
use crate::types::{ArchPy, LinkTypePy};
use crate::version::VersionInfoPy;
use furiosa_smi_rs::list_devices;
use pyo3::prelude::*;

mod core_status;
mod device;
mod device_error_info;
mod device_file;
mod device_info;
mod error;
mod performance;
mod types;
mod version;

pub const VERSION: &str = env!("CARGO_PKG_VERSION");

#[pyfunction(name = "list_devices")]
/// List all Furiosa NPU devices in the system.
fn list_devices_python(_py: Python<'_>) -> PyResult<Vec<DevicePy>> {
    list_devices()
        .map(|vec| {
            vec.into_iter()
                .map(DevicePy::new)
                .collect::<Vec<DevicePy>>()
        })
        .map_err(to_py_err)
}

#[pymodule]
#[pyo3(name = "furiosa_smi_py")]
fn furiosa_device_python(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(list_devices_python, m)?)?;
    m.add_class::<DevicePy>()?;
    m.add_class::<CoreStatusPy>()?;
    m.add_class::<DeviceErrorInfoPy>()?;
    m.add_class::<DeviceFilePy>()?;
    m.add_class::<DeviceInfoPy>()?;
    m.add_class::<DeviceUtilizationPy>()?;
    m.add_class::<PeUtilizationPy>()?;
    m.add_class::<MemoryUtilizationPy>()?;
    m.add_class::<ArchPy>()?;
    m.add_class::<LinkTypePy>()?;
    m.add_class::<VersionInfoPy>()?;
    m.add("__version__", VERSION)?;
    Ok(())
}

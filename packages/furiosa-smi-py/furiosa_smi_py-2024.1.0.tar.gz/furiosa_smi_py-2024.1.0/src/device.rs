use crate::core_status::CoreStatusPy;
use crate::device_error_info::DeviceErrorInfoPy;
use crate::device_file::DeviceFilePy;
use crate::device_info::DeviceInfoPy;
use crate::error::to_py_err;
use crate::performance::{DeviceTemperaturePy, DeviceUtilizationPy};
use crate::types::LinkTypePy;
use furiosa_smi_rs::Device;
use pyo3::pyclass;
use pyo3::pymethods;
use pyo3::PyResult;
use std::collections::BTreeMap;
use std::sync::Arc;

#[pyclass(name = "Device", unsendable)]
#[derive(Clone)]
/// Abstraction for a single Furiosa NPU device.
pub struct DevicePy {
    pub inner: Arc<Device>,
}

#[allow(clippy::arc_with_non_send_sync)]
impl DevicePy {
    pub(crate) fn new(dev: Device) -> Self {
        Self {
            inner: Arc::new(dev),
        }
    }
}

#[pymethods]
impl DevicePy {
    /// Returns `DeviceInfo` which contains information about NPU device. (e.g. arch, serial, ...)
    fn device_info(&self) -> PyResult<DeviceInfoPy> {
        self.inner
            .device_info()
            .map(DeviceInfoPy::new)
            .map_err(to_py_err)
    }

    /// List device files under this device.
    fn device_files(&self) -> PyResult<Vec<DeviceFilePy>> {
        self.inner
            .device_files()
            .map_err(to_py_err)
            .map(|v| v.into_iter().map(DeviceFilePy::new).collect())
    }

    /// Examine each core of the device, whether it is available or not.
    fn core_status(&self) -> PyResult<BTreeMap<u32, CoreStatusPy>> {
        self.inner
            .core_status()
            .map_err(to_py_err)
            .map(|v| v.into_iter().map(|(k, v)| (k, v.into())).collect())
    }

    /// Returns error states of the device.
    fn device_error_info(&self) -> PyResult<DeviceErrorInfoPy> {
        self.inner
            .device_error_info()
            .map(DeviceErrorInfoPy::new)
            .map_err(to_py_err)
    }

    /// Returns a liveness state of the device.
    fn liveness(&self) -> PyResult<bool> {
        self.inner.liveness().map_err(to_py_err)
    }

    /// Returns a utilization of the device.
    fn device_utilization(&self) -> PyResult<DeviceUtilizationPy> {
        self.inner
            .device_utilization()
            .map(DeviceUtilizationPy::new)
            .map_err(to_py_err)
    }

    /// Returns a power consumption of the device.
    fn power_consumption(&self) -> PyResult<f64> {
        self.inner.power_consumption().map_err(to_py_err)
    }

    /// Returns a temperature of the device.
    fn device_temperature(&self) -> PyResult<DeviceTemperaturePy> {
        self.inner
            .device_temperature()
            .map(DeviceTemperaturePy::new)
            .map_err(to_py_err)
    }

    /// Returns a device link type between two devices.
    fn get_device_to_device_link_type(&self, target: &DevicePy) -> PyResult<LinkTypePy> {
        self.inner
            .get_device_to_device_link_type(&target.inner)
            .map(|l| l.into())
            .map_err(to_py_err)
    }
}

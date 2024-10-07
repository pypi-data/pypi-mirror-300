use furiosa_smi_rs::{DeviceTemperature, DeviceUtilization, MemoryUtilization, PeUtilization};
use pyo3::pyclass;
use pyo3::pymethods;
use std::sync::Arc;

#[pyclass(name = "DeviceUtilization")]
#[derive(Clone)]
/// A struct for device information
pub struct DeviceUtilizationPy {
    pub inner: Arc<DeviceUtilization>,
}

impl DeviceUtilizationPy {
    pub(crate) fn new(utilization: DeviceUtilization) -> Self {
        Self {
            inner: Arc::new(utilization),
        }
    }
}

#[pymethods]
impl DeviceUtilizationPy {
    /// Returns a utilization of PE cores of the device.
    fn pe_utilization(&self) -> Vec<PeUtilizationPy> {
        self.inner
            .pe_utilization()
            .into_iter()
            .map(PeUtilizationPy::new)
            .collect()
    }

    /// Returns a memory utilization of the device.
    fn memory_utilization(&self) -> MemoryUtilizationPy {
        MemoryUtilizationPy::new(self.inner.memory_utilization())
    }
}

#[pyclass(name = "PeUtilization")]
#[derive(Clone)]
/// A struct for device information
pub struct PeUtilizationPy {
    pub inner: Arc<PeUtilization>,
}

impl PeUtilizationPy {
    pub(crate) fn new(pe_utilization: PeUtilization) -> Self {
        Self {
            inner: Arc::new(pe_utilization),
        }
    }
}

#[pymethods]
impl PeUtilizationPy {
    /// Returns list of PE core index.
    fn core(&self) -> u32 {
        self.inner.core()
    }

    /// Returns time window for utilization.
    fn time_window_mill(&self) -> u32 {
        self.inner.time_window_mill()
    }
    /// Returns PE usage percentage.
    pub fn pe_usage_percentage(&self) -> f64 {
        self.inner.pe_usage_percentage()
    }
}

#[pyclass(name = "MemoryUtilization")]
#[derive(Clone)]
/// A struct for device information
pub struct MemoryUtilizationPy {
    pub inner: Arc<MemoryUtilization>,
}

impl MemoryUtilizationPy {
    pub(crate) fn new(mem_utilization: MemoryUtilization) -> Self {
        Self {
            inner: Arc::new(mem_utilization),
        }
    }
}

#[pymethods]
impl MemoryUtilizationPy {
    /// Returns the total bytes of memory.
    pub fn total_bytes(&self) -> u64 {
        self.inner.total_bytes()
    }

    /// Returns the memory bytes currently in use.
    pub fn in_use_bytes(&self) -> u64 {
        self.inner.in_use_bytes()
    }
}

#[pyclass(name = "DeviceTemperature")]
#[derive(Clone)]
/// A struct for a temperature information of the device
pub struct DeviceTemperaturePy {
    pub inner: Arc<DeviceTemperature>,
}

impl DeviceTemperaturePy {
    pub(crate) fn new(dev_temperature: DeviceTemperature) -> Self {
        Self {
            inner: Arc::new(dev_temperature),
        }
    }
}

#[pymethods]
impl DeviceTemperaturePy {
    /// Returns the highest temperature observed from SoC sensors.
    pub fn soc_peak(&self) -> f64 {
        self.inner.soc_peak()
    }

    /// Returns the temperature observed from sensors attached to the board
    pub fn ambient(&self) -> f64 {
        self.inner.ambient()
    }
}

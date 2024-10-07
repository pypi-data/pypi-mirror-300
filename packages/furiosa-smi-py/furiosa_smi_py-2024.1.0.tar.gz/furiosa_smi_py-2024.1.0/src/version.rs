use crate::types::ArchPy;
use furiosa_smi_rs::VersionInfo;
use pyo3::pyclass;
use pyo3::pymethods;
use std::sync::Arc;

#[pyclass(name = "VersionInfo")]
#[derive(Clone)]
/// A struct for version information
pub struct VersionInfoPy {
    pub inner: Arc<VersionInfo>,
}

impl VersionInfoPy {
    pub(crate) fn new(version_info: VersionInfo) -> Self {
        Self {
            inner: Arc::new(version_info),
        }
    }
}

#[pymethods]
impl VersionInfoPy {
    fn __str__(&self) -> String {
        self.inner.to_string()
    }

    /// Get a architecture of device
    fn arch(&self) -> ArchPy {
        self.inner.arch().into()
    }

    /// Get a major part of version
    fn major(&self) -> u32 {
        self.inner.major()
    }

    /// Get a minor part of version
    fn minor(&self) -> u32 {
        self.inner.minor()
    }

    /// Get a patch part of version
    fn patch(&self) -> u32 {
        self.inner.patch()
    }

    /// Get a metadata of version
    fn metadata(&self) -> String {
        self.inner.metadata()
    }
}

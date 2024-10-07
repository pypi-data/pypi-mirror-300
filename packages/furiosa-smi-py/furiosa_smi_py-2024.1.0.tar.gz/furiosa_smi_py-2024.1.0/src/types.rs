use furiosa_smi_rs::{Arch, LinkType};
use pyo3::{pyclass, pymethods};

#[pyclass(name = "Arch")]
#[derive(Clone)]
/// Represents a architecture type of device
pub enum ArchPy {
    /// Warboy architecture
    Warboy = Arch::Warboy as isize,
    /// RNGD architecture
    Rngd = Arch::Rngd as isize,
    /// RNGD-Max architecture
    RngdMax = Arch::RngdMax as isize,
    /// RNGD-S architecture
    RngdS = Arch::RngdS as isize,
}

impl From<Arch> for ArchPy {
    fn from(arch_family: Arch) -> Self {
        match arch_family {
            Arch::Warboy => ArchPy::Warboy,
            Arch::Rngd => ArchPy::Rngd,
            Arch::RngdMax => ArchPy::RngdMax,
            Arch::RngdS => ArchPy::RngdS,
        }
    }
}

#[pymethods]
impl ArchPy {
    fn __str__(&self) -> String {
        match self {
            ArchPy::Warboy => "warboy",
            ArchPy::Rngd => "rngd",
            ArchPy::RngdMax => "rngd_s",
            ArchPy::RngdS => "rngd_max",
        }
        .to_string()
    }
}

#[pyclass(name = "LinkType")]
#[derive(Clone)]
/// Represents a device link type
pub enum LinkTypePy {
    /// Unknown link type
    Unknown = LinkType::Unknown as isize,
    /// Link type under same machine
    Interconnect = LinkType::Interconnect as isize,
    /// Link type under same cpu
    Cpu = LinkType::Cpu as isize,
    /// Link type under same switch
    Bridge = LinkType::Bridge as isize,
    /// Link type under same socket
    Noc = LinkType::Noc as isize,
}

impl From<LinkType> for LinkTypePy {
    fn from(link_type: LinkType) -> Self {
        match link_type {
            LinkType::Unknown => LinkTypePy::Unknown,
            LinkType::Interconnect => LinkTypePy::Interconnect,
            LinkType::Cpu => LinkTypePy::Cpu,
            LinkType::Bridge => LinkTypePy::Bridge,
            LinkType::Noc => LinkTypePy::Noc,
        }
    }
}

#[pymethods]
impl LinkTypePy {
    fn __str__(&self) -> String {
        match self {
            LinkTypePy::Unknown => "Unknown",
            LinkTypePy::Interconnect => "Interconnect",
            LinkTypePy::Cpu => "Cpu",
            LinkTypePy::Bridge => "Bridge",
            LinkTypePy::Noc => "Noc",
        }
        .to_string()
    }
}

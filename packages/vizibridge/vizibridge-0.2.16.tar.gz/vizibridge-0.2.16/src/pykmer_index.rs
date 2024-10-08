use crate::pykmer::*;
use pyo3::exceptions::PyKeyError;
use pyo3::prelude::*;
use pyo3::types::{PyIterator, PyString, PyType};
use seq_macro::seq;
use std::path::Path;
use vizitig_lib::kmer_index::{IndexIterator, KmerIndex, KmerIndexEntry};
seq!(N in 0..=31{

#[pyclass]
#[derive(Clone)]
pub struct KmerIndexEntry~N{
    pub inner: KmerIndexEntry::<N, u64>,
}

#[pymethods]
impl KmerIndexEntry~N{
    #[new]
    fn new(kmer: PyKmer~N, nid: usize) -> Self{
        Self {
            inner: KmerIndexEntry::<N, u64>{
                kmer: kmer.content,
                nid: nid
            }
        }
    }

    #[staticmethod]
    fn size() -> PyResult<usize> {
        Ok(N)
    }

    #[getter]
    fn kmer(&self) -> PyResult<PyKmer~N>{
        Ok(PyKmer~N{
            content: self.inner.kmer
        })
    }

    #[getter]
    fn nid(&self) -> PyResult<usize>{
        Ok(self.inner.nid)
    }
}


#[pyclass]
#[derive(Clone)]
pub struct KmerIndex~N{
    pub index: KmerIndex<N, u64>,
}

#[pymethods]
impl KmerIndex~N{
    #[classmethod]
    pub fn build(_: &Bound<'_, PyType>, iterator: &Bound<'_, PyIterator>, index_path: &Bound<'_, PyString>, buffer_size: usize) -> PyResult<Self> {
        let path : &Path = Path::new(index_path.to_str()?);
        let kmer_entry_iter = iterator.iter()?.map(|i| i.and_then(|i|
            Ok(KmerIndexEntry::<N, u64>{
                kmer: i.getattr("kmer")?.extract::<PyKmer~N>().unwrap().content,
                nid: i.getattr("nid")?.extract::<usize>().unwrap()
            })));

        unsafe {

            Ok(Self{
                index: KmerIndex::<N, u64>::build_index(kmer_entry_iter.filter_map(|e| e.ok()), path, buffer_size).unwrap(),
            })
        }
    }
    fn __len__(&self) -> PyResult<usize>{
        Ok(self.index.len())
    }

    fn __getitem__(&self, kmer: PyKmer~N) -> PyResult<usize>{
        match self.index.get(kmer.content){
            Ok(nid) => Ok(nid),
            _ => Err(PyKeyError::new_err(kmer))
        }
    }

    #[new]
    fn new(index_path: &Bound<'_, PyString>) -> PyResult<Self>{
        let path : &Path = Path::new(index_path.to_str()?);
        unsafe {
            Ok(Self{
                index: KmerIndex::<N, u64>::load_index(path).unwrap()
            })
        }
    }


    fn __iter__(slf: PyRef<Self>) -> PyResult<Py<IndexIterator~N>> {
        let iter = IndexIterator~N {
            inner: slf.index.clone().into_iter(),
        };
        Py::new(slf.py(), iter)
    }

    #[staticmethod]
    fn size() -> PyResult<usize> {
        Ok(N)
    }

}



#[pyclass]
pub struct IndexIterator~N{
    pub inner: IndexIterator<N, u64>
}


#[pymethods]
impl IndexIterator~N {
    fn __iter__(slf: PyRef<Self>) -> PyRef<Self> {
        slf
    }

    fn __next__(mut slf: PyRefMut<Self>) -> Option<KmerIndexEntry~N> {
        match slf.inner.next(){
            Some(index_entry) => {
                Some(KmerIndexEntry~N {
                    inner: index_entry
                })
            },
            _ => None
        }
    }
}

});

// Long version

seq!(N in 0..=31{

#[pyclass]
#[derive(Clone)]
pub struct LongKmerIndexEntry~N{
    pub inner: KmerIndexEntry::<{ N+32 }, u128>,
}

#[pymethods]
impl LongKmerIndexEntry~N{
    #[new]
    fn new(kmer: PyLongKmer~N, nid: usize) -> Self{
        Self {
            inner: KmerIndexEntry::<{ N+32 }, u128>{
                kmer: kmer.content,
                nid: nid
            }
        }
    }

    #[staticmethod]
    fn size() -> PyResult<usize> {
        Ok(N+32)
    }

    #[getter]
    fn kmer(&self) -> PyResult<PyLongKmer~N>{
        Ok(PyLongKmer~N{
            content: self.inner.kmer
        })
    }

    #[getter]
    fn nid(&self) -> PyResult<usize>{
        Ok(self.inner.nid)
    }
}


#[pyclass]
#[derive(Clone)]
pub struct LongKmerIndex~N{
    pub index: KmerIndex<{N + 32}, u128>,
}

#[pymethods]
impl LongKmerIndex~N{
    #[classmethod]
    pub fn build(_: &Bound<'_, PyType>, iterator: &Bound<'_, PyIterator>, index_path: &Bound<'_, PyString>, buffer_size: usize) -> PyResult<Self> {
        let path : &Path = Path::new(index_path.to_str()?);
        let kmer_entry_iter = iterator.iter()?.map(|i| i.and_then(|i|
            Ok(KmerIndexEntry::<{N+32}, u128>{
                kmer: i.getattr("kmer")?.extract::<PyLongKmer~N>().unwrap().content,
                nid: i.getattr("nid")?.extract::<usize>().unwrap()
            })));

        unsafe {

            Ok(Self{
                index: KmerIndex::<{N +32}, u128>::build_index(kmer_entry_iter.filter_map(|e| e.ok()), path, buffer_size).unwrap(),
            })
        }
    }
    fn __len__(&self) -> PyResult<usize>{
        Ok(self.index.len())
    }

    fn __getitem__(&self, kmer: PyLongKmer~N) -> PyResult<usize>{
        Ok(self.index.get(kmer.content).unwrap())
    }

    #[staticmethod]
    fn size() -> PyResult<usize> {
        Ok(N+32)
    }
    #[new]
    fn new(index_path: &Bound<'_, PyString>) -> PyResult<Self>{
        let path : &Path = Path::new(index_path.to_str()?);
        unsafe {
            Ok(Self{
                index: KmerIndex::<{N + 32}, u128>::load_index(path).unwrap()
            })
        }
    }


    fn __iter__(slf: PyRef<Self>) -> PyResult<Py<LongIndexIterator~N>> {
        let iter = LongIndexIterator~N {
            inner: slf.index.clone().into_iter(),
        };
        Py::new(slf.py(), iter)
    }

}


#[pyclass]
pub struct LongIndexIterator~N{
    pub inner: IndexIterator<{N + 32}, u128>
}


#[pymethods]
impl LongIndexIterator~N {
    fn __iter__(slf: PyRef<Self>) -> PyRef<Self> {
        slf
    }

    fn __next__(mut slf: PyRefMut<Self>) -> Option<LongKmerIndexEntry~N> {
        match slf.inner.next(){
            Some(index_entry) => {
                Some(LongKmerIndexEntry~N {
                    inner: index_entry
                })
            },
            _ => None
        }
    }
}

});

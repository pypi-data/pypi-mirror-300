import logging
import multiprocessing

import h5py
import numpy as np
import torch
from torch.utils.data import DataLoader, IterableDataset


class HDF5LoaderGenerator:
    def __init__(
        self, file_path, dataset_name, chunk_size, processors, shape, chunks_idx, split_idx, worker_id, desc_dct=None
    ):
        self.file_path = file_path
        self.dataset_name = dataset_name
        self.chunk_size = chunk_size
        self.processors = processors

        self.shape = shape
        self.chunks_idx = chunks_idx
        self.split_idx = split_idx
        self.worker_id = worker_id

        if desc_dct is None:
            self.desc_dct = {}
        else:
            self.desc_dct = desc_dct

        self.n_chunks = self.shape[0] // self.chunk_size + 1
        self.current_chunk_idx = 0
        self.current_shape = self.chunks_idx[self.current_chunk_idx].shape

    def _make_report(self):
        report_dct = {
            "worker_id": self.worker_id,
            "file": self.file_path,
            "shape": self.shape,
            "n_chunks": self.n_chunks,
            "current_chunk_idx": self.current_chunk_idx,
            "current_shape": self.current_shape,
        }
        return report_dct | self.desc_dct

    def _load_chunk(self):
        if self.current_chunk_idx == self.n_chunks:
            raise StopIteration

        logging.debug(f"Loading chunk {self.current_chunk_idx}/{len(self.chunks_idx) - 1} on worker {self.worker_id}!")

        chunk_idx = self.chunks_idx[self.current_chunk_idx]

        with h5py.File(self.file_path, "r") as f:
            chunk_arrays = f[self.dataset_name][chunk_idx]

        self.current_chunk_idx += 1
        self.current_shape = chunk_arrays.shape

        return chunk_arrays

    def __iter__(self):
        return self

    def __next__(self):
        chunk_arrays = self._load_chunk()
        report_dct = self._make_report()

        if self.processors is not None:
            return self.processors.fit(chunk_arrays, report_dct)
        else:
            return chunk_arrays, report_dct


class HDF5IterableDataset(IterableDataset):
    def __init__(self, file_path, dataset_name, chunk_size, num_workers, processors=None, desc_dct=None):
        """Create an iterable dataset from an hdf5 file. The data is split into chunks of size `chunk_size`.

        Parameters
        ----------
        file_path : str
            Path to the hdf5 file.
        dataset_name : str
            Name of the dataset in the hdf5 file.
        chunk_size : int
            Size of the data chunks.
        num_workers : int
            Number of workers to use.
        processors : ProcessorsGraph
            Processors graph to apply to the data.
        desc_dct : dict
            Description dictionary for additional information.
        """
        super().__init__()
        self.file_path = file_path
        self.dataset_name = dataset_name
        self.chunk_size = chunk_size
        self.num_workers = num_workers
        self.desc_dct = desc_dct

        self.processors = processors
        if self.processors is not None:
            self.processors.copy_processors = True

        self.shape = self._get_shape()
        self.chunks_idx = self._setup_chunks()
        self.splits = self.chunks_idx

    def _get_shape(self):
        with h5py.File(self.file_path, "r") as f:
            shape = f[self.dataset_name].shape
        return shape

    def _setup_chunks(self):
        """Split the data in hdf5 into chunks of size `chunk_size`.

        Returns
        -------
        list of arrays
            Indices of the data chunks.
        """
        n_chunks = self.shape[0] // self.chunk_size + 1

        idx = np.arange(0, self.shape[0], 1)
        chunks_idx = np.array_split(idx, n_chunks)

        return chunks_idx

    def __iter__(self):
        worker_info = torch.utils.data.get_worker_info()
        worker_id = worker_info.id

        if worker_info is None:
            worker_id = 0

        worker_split_chunks_idx, worker_split_splits, worker_shape_splits = [], [], []

        if len(self.chunks_idx) < self.num_workers:
            raise ValueError(f"Number of chunks ({len(self.chunks_idx)}) must be < num_workers ({self.num_workers})!")

        for i in range(self.num_workers):
            worker_split_chunks_idx.append(self.chunks_idx[i :: self.num_workers])
            worker_split_splits.append(self.splits[i :: self.num_workers])
            worker_shape_splits.append((sum([s.shape[0] for s in worker_split_chunks_idx[-1]]), self.shape[1]))

        return HDF5LoaderGenerator(
            self.file_path,
            self.dataset_name,
            self.chunk_size,
            self.processors,
            shape=worker_shape_splits[worker_id],
            chunks_idx=worker_split_chunks_idx[worker_id],
            split_idx=worker_split_splits[worker_id],
            worker_id=worker_id,
            desc_dct=self.desc_dct,
        )


def get_hdf5_dataloader(
    file_path,
    dataset_name,
    chunk_size,  # this is effectively the batch size
    desc_dct=None,
    processors=None,
    num_workers=0,
    prefetch_factor=None,
    **kwargs,
):
    """Create a dataloader for a single hdf5 file."""
    if num_workers == -1:
        num_workers = multiprocessing.cpu_count()

    hdf5_dataset = HDF5IterableDataset(
        file_path,
        dataset_name=dataset_name,
        chunk_size=chunk_size,
        processors=processors,
        num_workers=num_workers,
        desc_dct=desc_dct,
    )

    hdf5_dataloader = DataLoader(
        hdf5_dataset,
        batch_size=None,
        num_workers=num_workers,
        prefetch_factor=prefetch_factor,
        collate_fn=lambda batch: batch,
        **kwargs,
    )

    return hdf5_dataloader, hdf5_dataset.shape[0]

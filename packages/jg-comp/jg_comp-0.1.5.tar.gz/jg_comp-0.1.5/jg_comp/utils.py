from typing import List


def split_data_for_parallel_processing(data: bytes, num_threads: int, overlap_size: int = 8) -> List[bytes]:
    chunk_size = len(data) // num_threads
    chunks = []

    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size
        if i < num_threads - 1:
            end += overlap_size
        if i == num_threads - 1:
            end = len(data)

        chunk = data[start:end]
        if chunk:
            chunks.append(chunk)

    return chunks
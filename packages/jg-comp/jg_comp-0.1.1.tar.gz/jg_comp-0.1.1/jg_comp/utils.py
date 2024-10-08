# jg_comp/utils.py
def split_data_for_parallel_processing(data: bytes, num_threads: int):
    chunk_size = len(data) // num_threads
    return [data[i * chunk_size:(i + 1) * chunk_size] for i in range(num_threads)]

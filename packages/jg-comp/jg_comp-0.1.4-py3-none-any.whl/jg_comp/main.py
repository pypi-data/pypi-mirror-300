import cProfile
import pstats
from jg_comp.compressor import Compressor

def main():
    from jg_comp.compressor import Compressor

    # Données à compresser et décompresser
    data = "Exemple de données à compresser et décompresser avec le composant Compressor."

    # Créer une instance de Compressor
    compressor = Compressor()

    # Compresser les données en parallèle
    compressed_data = compressor.parallel_compress(data)
    print("Données compressées:", compressed_data)

    # Décompresser les données en parallèle
    decompressed_data = compressor.parallel_decompress(compressed_data)
    print("Données décompressées:", decompressed_data)

    # Vérifier que les données décompressées sont identiques aux données originales
    assert decompressed_data == data
    
if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats()
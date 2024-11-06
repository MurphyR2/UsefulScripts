import os
import sys

def print_banner():
    banner = """
    ######################################################
    #                                                    #
    #                     Slider                         #
    #                                                    #
    #          Divide un archivo en partes por líneas     #
    #                                                    #
    ######################################################
    #                                                    #
    #                Hecho por Murphy                    #
    #                                                    #
    ######################################################
    """
    print(banner)

def split_file(input_file, lines_per_file):
    # Verifica si el archivo existe
    if not os.path.isfile(input_file):
        print(f"El archivo {input_file} no existe.")
        return

    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    total_lines = len(lines)
    print(f"Total de líneas en el archivo: {total_lines}")

    # Calcular cuántos archivos se generarán
    file_count = (total_lines // lines_per_file) + (1 if total_lines % lines_per_file != 0 else 0)

    for i in range(file_count):
        start_index = i * lines_per_file
        end_index = start_index + lines_per_file
        part_lines = lines[start_index:end_index]

        # Crear el nombre del nuevo archivo
        output_file = f"{os.path.splitext(input_file)[0]}_PART_{i + 1}.txt"
        with open(output_file, 'w') as outfile:
            outfile.writelines(part_lines)
        
        print(f"Creado: {output_file} con {len(part_lines)} líneas.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python slider.py <input_file> <lines_per_file>")
    else:
        input_file = sys.argv[1]
        lines_per_file = int(sys.argv[2])
        print_banner()
        split_file(input_file, lines_per_file)

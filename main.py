import os
import converter as conv

SOURCE_PATH = "./tdx_files"
OUTPUT_PATH = "./cvs_files"

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    input_files = [f for f in os.listdir(SOURCE_PATH)
                   if os.path.isfile(os.path.join(SOURCE_PATH, f))]
    output_files = [f[:-4] + ".csv" for f in input_files]

    input_paths = (os.path.join(SOURCE_PATH, f) for f in input_files)
    output_paths = (os.path.join(OUTPUT_PATH, f) for f in output_files)

    for in_path, out_path in zip(input_paths, output_paths):
        print("load: {}, output: {}".format(in_path, out_path))
        conv.output_csv(out_path, conv.load_tdx(in_path))
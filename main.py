import os
import sys

import converter as conv

input_path = "./tdx_files"
output_path = "./csv_files"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("必须提供K线类型，'d'代表日线, 'm'代表分钟线")

    try:
        output_idx = sys.argv.index("-o")
        output_path = sys.argv[output_idx + 1]
    except ValueError:
        pass

    try:
        input_idx = sys.argv.index("-i")
        input_path = sys.argv[input_idx + 1]
    except ValueError:
        pass

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    input_files = [f for f in os.listdir(input_path)
                   if os.path.isfile(os.path.join(input_path, f))]
    output_files = [f[:-4] + ".csv" for f in input_files]

    input_paths = (os.path.join(input_path, f) for f in input_files)
    output_paths = (os.path.join(output_path, f) for f in output_files)

    for in_path, out_path in zip(input_paths, output_paths):
        print("load: {}, output: {}".format(in_path, out_path),
              end=" ",
              flush=True)

        if sys.argv[1] == 'd':
            symbol, exchange, grid = conv.load_tdx(in_path)
            conv.output_csv_daily(out_path, grid, symbol, exchange)
        elif sys.argv[1] == 'm':
            try:
                sys.argv.index("--no-adjust-time")
                adjust_time = False
            except ValueError:
                adjust_time = True

            symbol, exchange, grid = conv.load_tdx(in_path)
            conv.output_csv_minute(out_path, grid, symbol, exchange,
                                   adjust_time)
        else:
            raise ValueError(
                "'{}' 不是有效的K线类型，'d'代表日线, 'm'代表分钟线".format(sys.argv[1]))

        print("Done")

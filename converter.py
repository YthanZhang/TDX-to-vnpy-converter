import pandas as pd


def load_tdx(path: str) -> list[list]:
    with open(path, mode="r", encoding="GBK") as f:
        text = f.read()
        lines = text.split("\n")[2:][:-2]

    grid = []
    for line in lines:
        grid.append(line.split())

    return grid


def output_csv(path: str, grid: list[list]):
    df_map = {"datetime": 0,
              "open": 1,
              "high": 2,
              "low": 3,
              "close": 4,
              "volume": 5,
              "open_interest": 6}

    df_dict = {}
    for key in df_map.keys():
        df_dict[key] = []

    for row in grid:
        for key in df_dict.keys():
            df_dict[key].append(row[df_map[key]])

    df = pd.DataFrame(df_dict)
    df.to_csv(path, index=False)


if __name__ == "__main__":
    tdx_grid = load_tdx("tdx_files/AGL9.txt")
    output_csv("AGL9.csv", tdx_grid)

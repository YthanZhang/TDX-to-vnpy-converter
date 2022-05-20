import pandas as pd


def load_tdx(path: str) -> (str, list[list]):
    with open(path, mode="r", encoding="GBK") as f:
        text = f.read()
        lines = text.split("\n")
        symbol_ = lines[0].split()[0]
        lines = lines[2:-2]

    grid = []
    for line in lines:
        grid.append(line.split())

    return symbol_, grid


def tdx_date_to_datetime(date: str) -> str:
    return date + " 09:00:00"


def output_csv_daily(path: str, grid: list[list], symbol_: str):
    # df_map maps column name to grid column index
    df_map = {"datetime": 0,
              "open": 1,
              "high": 2,
              "low": 3,
              "close": 4,
              "volume": 5,
              "open_interest": 6}

    # df_dict match pandas dataframe with dictionary
    df_dict = {}
    for key in df_map.keys():
        df_dict[key] = []

    # append data to df_dict from grid
    for row in grid:
        for key in df_dict.keys():
            if key == "datetime":
                df_dict[key].append(tdx_date_to_datetime(row[df_map[key]]))
            else:
                df_dict[key].append(row[df_map[key]])

    df_dict["symbol"] = [symbol_ for _ in range(len(df_dict["open"]))]

    # export csv file
    df = pd.DataFrame(df_dict)
    df.to_csv(path, index=False)


def tdx_date_time_to_datetime(date: str, time: str) -> str:
    return date + " " + time[:2] + ":" + time[2:] + ":00"


def output_csv_minute(path: str, grid: list[list], symbol_: str):
    # df_map maps column name to grid column index
    df_map = {
        "datetime": [0, 1],
        "open": 2,
        "high": 3,
        "low": 4,
        "close": 5,
        "volume": 6,
        "open_interest": 7,
    }

    # df_dict match pandas dataframe with dictionary
    df_dict = {}
    for key in df_map.keys():
        df_dict[key] = []

    # append data to df_dict from grid
    for row in grid:
        for key in df_dict.keys():
            if key == "datetime":
                date = row[df_map[key][0]]
                time = row[df_map[key][1]]
                df_dict[key].append(tdx_date_time_to_datetime(date, time))
            else:
                df_dict[key].append(row[df_map[key]])

    df_dict["symbol"] = [symbol_ for _ in range(len(df_dict["open"]))]

    # export csv file
    df = pd.DataFrame(df_dict)
    df.to_csv(path, index=False)


if __name__ == "__main__":
    symbol, tdx_grid = load_tdx("tdx_files/AGL9.txt")
    output_csv_daily("AGL9.csv", tdx_grid, symbol)

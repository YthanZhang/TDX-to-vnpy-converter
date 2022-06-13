from datetime import datetime, timedelta

import pandas as pd

exchange_df = pd.read_csv("exchange_list.csv", encoding="GBK")


def get_exchange_from_symbol(symbol: str) -> str:
    if symbol[-2:] == "L9":
        symbol = symbol[:-2]
    exchange_row = exchange_df.loc[exchange_df["交易代码"] == symbol]

    if not exchange_row.empty:
        return exchange_row.iloc[0, 2]
    else:
        return "None"


def load_tdx(path: str) -> (str, str, list[list]):
    with open(path, mode="r", encoding="GBK") as f:
        text = f.read()
        lines = text.split("\n")

    symbol = lines[0].split()[0]
    lines = lines[2:-2]

    exchange = get_exchange_from_symbol(symbol)

    grid = []
    for line in lines:
        grid.append(line.split())

    return symbol, exchange, grid


def tdx_date_to_datetime(date: str) -> str:
    return date + " 09:00:00"


def output_csv_daily(path: str, grid: list[list], symbol: str, exchange: str):
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

    df_dict["symbol"] = [symbol for _ in range(len(df_dict["open"]))]
    df_dict["exchange"] = [exchange for _ in range(len(df_dict["open"]))]

    # export csv file
    df = pd.DataFrame(df_dict)
    df.to_csv(path, index=False)


def tdx_date_time_to_datetime(date_str: str, time_str: str,
                              adjust_end_time=False) -> str:
    dt_str = date_str + " " + time_str[:2] + ":" + time_str[2:] + ":00"
    if not adjust_end_time:
        return dt_str
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    dt -= timedelta(minutes=1)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def output_csv_minute(path: str, grid: list[list], symbol: str, exchange: str,
                      time_adjust: bool):
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
                df_dict[key].append(
                    tdx_date_time_to_datetime(date, time, time_adjust))
            else:
                df_dict[key].append(row[df_map[key]])

    df_dict["symbol"] = [symbol for _ in range(len(df_dict["open"]))]
    df_dict["exchange"] = [exchange for _ in range(len(df_dict["open"]))]

    # export csv file
    df = pd.DataFrame(df_dict)
    df.to_csv(path, index=False)


if __name__ == "__main__":
    symbol_, exchange_, tdx_grid_ = load_tdx("tdx_files/AGL9.txt")
    output_csv_daily("AGL9.csv", tdx_grid_, symbol_, exchange_)

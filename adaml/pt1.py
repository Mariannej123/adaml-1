import typing
import argparse
import os

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

import helper


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("--data-path", required=True, help="Path to a file containing data.")
    parser.add_argument("--out-path", required=True, help="Path to an output folder.")
    parser.add_argument("--compression", default="gzip", help="Compression format.")

    args = parser.parse_args()
    return args


def find_ranges(df: pd.DataFrame) -> pd.DataFrame:
    mins, maxs = df.min(axis=0), df.max(axis=0)

    range_df = pd.concat([mins, maxs], axis=1).reset_index().rename({"index": "column", 0: "min", 1: "max"}, axis=1)
    print(range_df)


def plot_boxplots(df: pd.DataFrame, out_path: str) -> None:
    fig, axes = plt.subplots(2, 2)

    for ax, (col_name, col_data) in zip(axes.flat, df.iteritems()):
        sns.set_theme()
        sns_ax = sns.boxplot(ax=ax, data=col_data[col_data.notna()], showfliers=False)
        sns_ax.set(xticklabels=[], title=col_name)

    fig.savefig(os.path.join(out_path, "boxplots.pdf"))


if __name__ == "__main__":
    args = parse_arguments()
    
    os.makedirs(args.out_path, exist_ok=True)

    df = helper.load_data(args.data_path, args.compression)

    find_ranges(df)
    plot_boxplots(df[["temperature", "humidity", "light", "voltage"]], args.out_path)

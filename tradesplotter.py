#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# TradesPlotter.py
# ----------------
# A simple Python script that, by using the great Yahoo Finance APIs, downloads
# the data for a list of trades of your choice and draws the respective charts,
# plus a comparison chart for all the trades together.
#
# Coded by: Riccardo Mollo (riccardomollo84@gmail.com)
#

import argparse
import locale
import os
import random
import sys
import stdnum
import matplotlib.pyplot as plt
import pandas as pd
import stdnum.isin
import yfinance as yf
from termcolor import colored

DEBUG = True
CACHE = ".cache"  # custom cache location for YFinance data
DPI = 96  # DPI resolution of your monitor
IMG_FORMAT = "png"  # output format for chart images

yf.set_tz_cache_location(
    os.path.dirname(os.path.abspath(__file__)) + os.path.sep + CACHE
)


def print_error(message):
    print(colored("[ERROR]", "red", attrs=["reverse", "bold"]) + " " + message)


def print_debug(message):
    if DEBUG:
        print(colored("[DEBUG]", "yellow") + " " + message)


def check_file(file):
    if os.path.exists(file) and os.access(file, os.R_OK):
        print_debug('File "{}" exists and is readable.'.format(file))
    else:
        print_error('File "{}" does not exist or is not readable.'.format(file))
        sys.exit(1)


def check_and_create_directory(directory):
    if os.path.exists(directory) and os.access(directory, os.W_OK):
        print_debug('Directory "{}" exists and is writable.'.format(directory))
    else:
        print_debug('Directory "{} does not exist.'.format(directory))

        try:
            os.makedirs(directory, exist_ok=True)
            print_debug('Directory "{}" has been created.'.format(directory))
        except OSError as e:
            print_error('Error creating "{}" directory ({}).'.format(directory, e))
            sys.exit(1)


def isin_to_color(isin):
    base36 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base36_map = {char: i for i, char in enumerate(base36)}
    num_value = 0

    for char in isin:
        num_value = num_value * 36 + base36_map[char]

    r = (num_value >> 16) & 0xFF
    g = (num_value >> 8) & 0xFF
    b = num_value & 0xFF
    color = f"#{r:02X}{g:02X}{b:02X}"

    return color


def norm_minmax(isin_list, csv_output_dir):
    cnt = 0
    dfs = []
    norm_dfs = []

    for isin in isin_list:
        csv_input_file = csv_output_dir + os.path.sep + isin + ".csv"
        dfs.append(pd.read_csv(csv_input_file, parse_dates=["Date"]))

    combined_df = pd.concat(dfs, ignore_index=True)

    min_values = combined_df.min()
    max_values = combined_df.max()

    def min_max_normalize(df):
        return (df - min_values) / (max_values - min_values)

    plt.figure(figsize=(1920 / DPI, 1080 / DPI), dpi=DPI)

    for df in dfs:
        norm_dfs.append(min_max_normalize(df))
        norm_dfs[cnt].to_csv("/tmp/idx/" + str(cnt) + ".csv", index=False)
        plt.plot(norm_dfs[cnt]["Date"], norm_dfs[cnt]["Close"], label=str(cnt))
        cnt += 1

    plt.xlabel("Date")
    plt.ylabel("Normalized Close")
    plt.title("Normalized Close Prices")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def norm_zscore(isin_list, csv_output_dir):
    cnt = 0
    dfs = []
    norm_dfs = []

    for isin in isin_list:
        csv_input_file = csv_output_dir + os.path.sep + isin + ".csv"
        dfs.append(pd.read_csv(csv_input_file, parse_dates=["Date"]))

    combined_df = pd.concat(dfs, ignore_index=True)

    mean_values = combined_df.mean()
    std_values = combined_df.std()

    def z_score_standardize(df):
        return (df - mean_values) / std_values

    plt.figure(figsize=(1920 / DPI, 1080 / DPI), dpi=DPI)

    for df in dfs:
        norm_dfs.append(z_score_standardize(df))
        norm_dfs[cnt].to_csv("/tmp/idx/" + str(cnt) + "_z.csv", index=False)
        plt.plot(norm_dfs[cnt]["Date"], norm_dfs[cnt]["Close"], label=str(cnt))
        cnt += 1

    plt.xlabel("Date")
    plt.ylabel("Normalized Close")
    plt.title("Normalized Close Prices")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot(isin, title, csv_output_dir, img_output_dir):
    try:
        csv_input_file = csv_output_dir + os.path.sep + isin + ".csv"
        img_output_file = img_output_dir + os.path.sep + isin + "." + IMG_FORMAT
        df = pd.read_csv(csv_input_file, parse_dates=["Date"])

        plt.figure(figsize=(10, 5))
        plt.plot(df["Date"], df["Close"], marker=",", linestyle="-")
        plt.xlabel("Date")
        plt.ylabel("Close Price")
        plt.title(isin + " - " + title, fontsize=12, fontweight="bold")
        plt.suptitle("Close Price Over Time (Max)")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.savefig(img_output_file, format=IMG_FORMAT, dpi=300)

        print_debug('Image for {} saved to "{}" file'.format(isin, img_output_file))
    except Exception as e:  # TODO: too general exception
        print_error("Can not save image file for {} ({}).".format(isin, e))


def plot_all(isin_list, csv_output_dir, img_output_dir):
    try:
        cnt = 0
        dfs = []

        for isin in isin_list:
            csv_input_file = csv_output_dir + os.path.sep + isin + ".csv"
            dfs.append(pd.read_csv(csv_input_file, parse_dates=["Date"]))

        plt.figure(figsize=(1920 / DPI, 1080 / DPI), dpi=DPI)

        for df in dfs:
            random_color = isin_to_color(isin_list[cnt])
            plt.plot(
                df["Date"],
                df["Close"],
                marker=",",
                linestyle="-",
                color=random_color,
                label=isin_list[cnt],
            )
            cnt += 1

        plt.xlabel("Date")
        plt.ylabel("Close Price")
        plt.title("Close Price Comparison Over Time (Max)")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend()

        img_output_file = img_output_dir + os.path.sep + "ALL." + IMG_FORMAT

        plt.savefig(img_output_file, format=IMG_FORMAT, dpi=DPI)

        print_debug('Comparison image saved to "{}" file'.format(img_output_file))
    except Exception as e:  # TODO: too general exception
        print_error("Can not save comparison image file ({}).".format(e))


def main2():
    #isin_list = ["IE00B0M62Q58", "IE00B3VTMJ91", "US0378331005", "US88160R1014"]
    isin_list = ['IE00B0M62X26' ,'IE00B14X4Q57' ,'IE00B3DKXQ41' ,'IE00B3F81R35' ,'IE00B3VTMJ91' ,'IE00B4L5Y983' ,'IE00B53SZB19' ,'IE00B5BMR087' ,'IE00B9CQXS71' ,'IE00BDFL4P12' ,'IE00BF4G7076' ,'IE00BM67HN09' ,'IE00BM67HQ30' ,'IE00BYZK4669' ,'IE00BZCQB185' ,'IT0005285157' ,'IT0005423246' ,'LU0140636928' ,'LU0497415702' ,'LU0908500753' ,'LU1681041114' ,'LU1781541252' ,'LU2009201638' ,'LU2215044020']
    csv_output_dir = "out/csv"
    norm_minmax(isin_list, csv_output_dir)
    norm_zscore(isin_list, csv_output_dir)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-file", help="Input file with a list of ISIN codes", required=True
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        help="Output directory for saving CSV files and images",
        required=True,
    )
    args = parser.parse_args()

    input_file = args.input_file
    output_dir = args.output_dir
    csv_output_dir = output_dir + os.path.sep + "csv"
    img_output_dir = output_dir + os.path.sep + "img"

    check_file(input_file)
    check_and_create_directory(output_dir)
    check_and_create_directory(csv_output_dir)
    check_and_create_directory(img_output_dir)

    with open(input_file, mode="r", encoding=locale.getpreferredencoding()) as file:
        lines = file.readlines()
        isin_list = []
        cnt = 0

        for line in lines:
            cnt += 1
            isin = line.strip()

            if not stdnum.isin.is_valid(isin):
                print_error("ISIN code {} is not valid.".format(isin))
            else:
                try:
                    info = yf.Ticker(isin)
                    title = info.info["longName"]
                    # symbol = info.info['symbol']  # TODO: also use symbols in the comparison image
                    print_debug("Getting data for {} ({})...".format(isin, title))
                    data = yf.download(isin, period="max")

                    if len(data) == 0:
                        print_debug("No data for {}.".format(isin))
                    else:
                        csv_output_file = os.path.join(csv_output_dir, isin + ".csv")
                        data.to_csv(csv_output_file)

                        print_debug(
                            'Data for {} saved to "{}" file'.format(
                                isin, csv_output_file
                            )
                        )

                        plot(isin, title, csv_output_dir, img_output_dir)
                        isin_list.append(isin)
                except Exception as e:  # TODO: too general exception
                    print_error(
                        "Can not get data or save CSV file for {} ({}).".format(isin, e)
                    )

        plot_all(isin_list, csv_output_dir, img_output_dir)

    print_debug("Fetched data for {} out of {} trades.".format(len(isin_list), cnt))
    print()
    sys.exit(0)


if __name__ == "__main__":
    main()

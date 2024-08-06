#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# YFPlotter.py
# ------------
# A simple Python script that ...
#
# Coded by: Riccardo Mollo (riccardomollo84@gmail.com)
#

# https://medium.com/@kasperjuunge/yfinance-10-ways-to-get-stock-data-with-python-6677f49e8282

import contextlib
import csv
import locale
import os
import sys
import random as random
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from termcolor import colored

DEBUG = True
CACHE = ".cache"  # custom cache location for YFinance data
DPI = 96

yf.set_tz_cache_location(
    os.path.dirname(os.path.abspath(__file__)) + os.path.sep + CACHE
)


def print_error(message):
    print(colored("[ERROR]", "red", attrs=["reverse", "bold"]) + " " + message)


def print_debug(message):
    if DEBUG:
        print(colored("[DEBUG]", "yellow") + " " + message)


def plot(isin, title, csv_output_dir, img_output_dir):
    try:
        csv_input_file = csv_output_dir + os.path.sep + isin + ".csv"
        img_format = "png"
        img_output_file = img_output_dir + os.path.sep + isin + "." + img_format
        df = pd.read_csv(csv_input_file, parse_dates=["Date"])

        plt.figure(figsize=(10, 5))
        plt.plot(df["Date"], df["Close"], marker=",", linestyle="-")
        plt.xlabel("Date")
        plt.ylabel("Close Price")
        plt.title(isin + " - " + title, fontsize=12, fontweight="bold")
        plt.suptitle("Close Price Over Time (Max)")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.savefig(img_output_file, format=img_format, dpi=300)

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

        #plt.figure(figsize=(10, 5))
        plt.figure(figsize=(1920/DPI, 1080/DPI), dpi=300)

        for df in dfs:
            random_color = (random.random(), random.random(), random.random())
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

        img_format = "png"
        img_output_file = img_output_dir + os.path.sep + "ALL." + img_format

        plt.savefig(img_output_file, format=img_format, dpi=300)

        print_debug('Comparison image saved to "{}" file'.format(img_output_file))
    except Exception as e:  # TODO: too general exception
        print_error("Can not save comparison image file ({}).".format(isin, e))


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


def main():
    if len(sys.argv) != 3:
        script_name = os.path.basename(__file__)
        print_error(f"Usage: python {script_name} <input_csv> <output_dir>")
        sys.exit(1)

    csv_input_file = sys.argv[1]
    output_dir = sys.argv[2]
    csv_output_dir = output_dir + os.path.sep + "csv"
    img_output_dir = output_dir + os.path.sep + "img"

    if os.path.exists(csv_input_file) and os.access(csv_input_file, os.R_OK):
        print_debug('File "{}" exists and is readable.'.format(csv_input_file))
    else:
        print_error(
            'File "{}" does not exist or is not readable.'.format(csv_input_file)
        )
        sys.exit(1)

    check_and_create_directory(output_dir)
    check_and_create_directory(csv_output_dir)
    check_and_create_directory(img_output_dir)

    with open(csv_input_file, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)

        isin_list = []

        for row in reader:
            isin = row[0]
            title = row[1]

            print_debug("Getting data for {} ({})...".format(isin, title))

            try:
                # with open(os.devnull, "w", encoding=locale.getpreferredencoding()) as fnull, contextlib.redirect_stdout(fnull), contextlib.redirect_stderr(fnull):
                with open(os.devnull, "w", encoding=locale.getpreferredencoding()):
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
                    "Can not get data or safe CSV file for {} ({}).".format(isin, e)
                )

        plot_all(isin_list, csv_output_dir, img_output_dir)

    print()
    sys.exit(0)


if __name__ == "__main__":
    main()
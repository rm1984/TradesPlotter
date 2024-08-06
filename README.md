# TradesPlotter

**TradesPlotter** is a simple Python script that, by using the great Yahoo Finance APIs, downloads the data for a list of trades of your choice and draws the respective charts, plus a comparison chart for all the trades together.

**Usage:**
```
usage: python tradesplotter.py <input_csv> <output_dir>
```

**Example:**

First of all, prepare a CSV file (trades_example.csv) with the ISIN codes of all your trades, plus their names, like in this example:

```
US0378331005,Apple Inc.
US88160R1014,Tesla Inc.
IE00B0M62Q58,iShares MSCI World UCITS ETF (Dist)
JE00B1VS3770,WisdomTree Physical Gold
IE00B3VTMJ91,iShares Euro Government Bond 1-3yr UCITS ETF (Acc)
```

Then run the script like this:

```
$ ./tradesplotter.py trades_example.csv out
```

In the ```out/csv``` directory you will find, for each trade, a CSV file with all its closing prices of his entire lifespan to date.
In the ```out/img``` directory you will find, for each trade, the relative chart, plus a comparison chart for all the trades together, like in the following image.

<a href="https://ibb.co/kH36kN7"><img src="https://i.ibb.co/7YgN8sf/ALL.png" alt="TradesPlotter" border="0" /></a>

As you can see, the example subdirectories contain the following files:

```
$ ls -1 out/*

out/csv:
IE00B0M62Q58.csv
IE00B3VTMJ91.csv
US0378331005.csv
US88160R1014.csv

out/img:
ALL.png
IE00B0M62Q58.png
IE00B3VTMJ91.png
US0378331005.png
US88160R1014.png
```

# TradesPlotter

**TradesPlotter** is a simple Python script that, by using the great Yahoo Finance APIs, downloads the data for a list of trades of your choice and draws the respective charts, plus a comparison chart for all the trades together.

**Usage:**
```
usage: python tradesplotter.py [-h] -i INPUT_FILE -o OUTPUT_DIR
```

**Example:**

First of all, prepare a text file (for example, ```trades_example.txt```) with a list of the ISIN codes of all your trades, like in this example:

```
US0378331005
US88160R1014
IA00B1M62Q52
IE00B0M62Q58
JE00B1VS3770
IE00B3VTMJ91
```

Then run the script like this:

```
$ ./tradesplotter.py -i trades_example.txt -o out
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

Trades for which no information can be retrieved are automatically skipped.

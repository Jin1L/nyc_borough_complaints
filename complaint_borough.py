import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="the input csv file")
    parser.add_argument("-s", "--start", required=True, help="the start date")
    parser.add_argument("-e", "--end", required=True, help="the end date")
    parser.add_argument("-o", "--output", help="the output file")

    args = parser.parse_args()

    fileName = args.input
    outputFile = args.output
    start_date = pd.to_datetime(args.start, format='%m/%d/%Y')
    end_date = pd.to_datetime(args.end, format='%m/%d/%Y')

    count = 0
    df = pd.read_csv(fileName, header=None)
    # Convert the second column (column at index 1) to datetime
    df[1] = pd.to_datetime(df[1].str[:10], format='%m/%d/%Y')
    df = df[(df[1] >= start_date) & (df[1] <= end_date)]
    
    df = df.groupby([df[5], df[16]]).size().reset_index(name='count')
    df = df.rename(columns={5: "complaint type", 16: "borough"})

    if outputFile:
        df.to_csv(outputFile, index=False)
    else:
        print(df)


if __name__ == "__main__":
    main()



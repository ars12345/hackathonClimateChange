import pandas as pd


def main():
    for i in range(7, 9):
        for j in range(1, 12):
            df = pd.read_csv("data_input/fre-hourly-"+f"{j:02d}"+"01201"+str(i)+"-"+f"{j:02d}"+"31201"+str(i)+".csv")
            print(df+"\n")


if __name__ == "__main__":
    main()
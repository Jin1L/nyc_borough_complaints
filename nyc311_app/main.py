from bokeh.plotting import figure, curdoc, column
from bokeh.models import Dropdown
from pathlib import Path
import pandas as pd

def load_csv_path(fname):
    return Path(__file__).parent / fname

def load_csv_file(fname):
    csv_path = load_csv_path(fname)
    df = pd.read_csv(csv_path)

    return df

def update_plot1(event):
    global df, p

    zipcode = event.item
    filtered = df[df['Zipcode'] == float(zipcode)]

    p.line(filtered["Start Month"].unique().tolist(), df.loc[df['Zipcode'] == float(zipcode), 'Duration'].tolist(),
            legend_label=zipcode, line_width=2, line_color="blue")
    
def update_plot2(event):
    global df, p

    zipcode = event.item
    filtered = df[df['Zipcode'] == float(zipcode)]

    p.line(filtered["Start Month"].unique().tolist(), df.loc[df['Zipcode'] == float(zipcode), 'Duration'].tolist(),
            legend_label=zipcode, line_width=2, line_color="red")
    
    df = df.groupby("Start Month")["Duration"].mean().reset_index()

    p.line(df["Start Month"].tolist(), df["Duration"].tolist(), legend_label="total_mean", line_width=2, line_color="green")

def main():
    global df, p

    df = load_csv_file("nyc2020_finalData.csv")

    p = figure(title="Average incident create-to-closed time", x_axis_label='month', y_axis_label='hours')

    zipcode_column = [str(x) for x in df["Zipcode"].unique()]

    dropdown1 = Dropdown(label="Dropdown button", menu=zipcode_column)
    dropdown2 = Dropdown(label="Dropdown button", menu=zipcode_column)
    dropdown1.on_event("menu_item_click", update_plot1)
    dropdown2.on_event("menu_item_click", update_plot2)
    
    curdoc().add_root(column(p,dropdown1,dropdown2))

main()
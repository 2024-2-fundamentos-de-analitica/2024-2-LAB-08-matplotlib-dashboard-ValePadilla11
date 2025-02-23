# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""
import matplotlib.pyplot as plt
import pandas as pd
import os

def load_data():
    """
    Carga el archivo `files/input/shipping-data.csv` y retorna un DataFrame.
    """
    return pd.read_csv('files/input/shipping-data.csv')


def create_visual_for_shipping_per_warehouse(data):
    """
    Crea un gráfico de barras que muestre la cantidad de envios por cada
    bloque de almacén.
    """
    df = data.copy()
    plt.figure()
    counts = df.Warehouse_block.value_counts()
    counts.plot.bar(
        title='Shipping per Warehouse',
        xlabel='Warehouse block',
        ylabel='Record Count',
        color='tab:blue',
        fontsize=8,
    )

    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.savefig('docs/shipping_per_warehouse.png')

def create_visual_for_mode_of_shipment(data):
    df = data.copy()
    plt.figure()
    counts = df.Mode_of_Shipment.value_counts()
    counts.plot.pie(
        title='Mode of Shipment',
        ylabel='',
        wedgeprops=dict(width=0.35),
        colors=['tab:blue', 'tab:orange', 'tab:green'],
    )
    plt.savefig('docs/mode_of_shipment.png')

def create_visual_for_average_customer_rating(df):
    df = df.copy()
    plt.figure()
    df = (
        df[["Mode_of_Shipment", "Customer_rating"]]
        .groupby("Mode_of_Shipment")
        .describe()
    )
    df.columns = df.columns.droplevel()
    df = df[["mean", "min", "max"]]
    plt.barh(
        y=df.index.values,
        width=df["max"].values - 1,
        left=df["min"].values,
        height=0.9,
        color="lightgray",
        alpha=0.8,
    )

    colors = [
        "tab:green" if value >= 3.0 else "tab:orange" for value in df["mean"].values
    ]
    plt.barh(
        y=df.index.values,
        width=df["mean"].values - 1,
        left=df["min"],
        color=colors,
        height=0.5,
        alpha=1,
    )

    plt.title("Average Customer Rating")
    plt.gca().spines["left"].set_color("gray")
    plt.gca().spines["bottom"].set_color("gray")
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.savefig("docs/average_customer_rating.png")

def create_visual_for_weight_distribution(df):
    df = df.copy()
    plt.figure()
    df.Weight_in_gms.plot.hist(
        title='Shipped Weight Distribution',
        edgecolor='white',
        color='tab:orange',
    )
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.savefig('docs/weight_distribution.png')  

def pregunta_01():
    # Se crea la ruta en donde se guardan los archivos
    ruta = 'docs'
    if not os.path.exists(ruta):
        os.makedirs(ruta)
    
    # Se cargan los datos
    df = load_data()

    # Se crea la figura shipping_per_warehouse.png
    create_visual_for_shipping_per_warehouse(df)

    # Se crea la figura mode_of_shipment.png'
    create_visual_for_mode_of_shipment(df)

    # Se crea la figura average_customer_rating.png
    create_visual_for_average_customer_rating(df)

    # Se crea la figura weight_distribution.png
    create_visual_for_weight_distribution(df)

    # Se crea un archivo hmtl que sirva como dashboard
    html_content = """
    <!DOCTYPE html>
    <html>
        <body>
            <h1>Shippping dashboard example</h1>
            <div style="width:45%; float:left">
                <img src="shipping_per_warehouse.png" alt="Fig 1">
                <img src="mode_of_shipment.png" alt="Fig 2">
            </div>
            <div style="width:45%; float:left">
                <img src="average_customer_rating.png" alt="Fig 3">
                <img src="weight_distribution.png" alt="Fig 1">
            </div>  
        </body>
    </html>
    """
    # Crear y guardar el archivo HTML
    with open('docs/index.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

pregunta_01()
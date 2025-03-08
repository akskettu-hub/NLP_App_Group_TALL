import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as n


COLOR = '#34495e'
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR

def generate_chart(data, search_results=[]):
    plot_x = data.data.keys() # gets the years
    plot_y = [len(value.keys()) for key, value in data.data.items()] # gets the number of cases for each year
    # plot_y2 = search_results

    plt.figure(figsize=(10, 2))
    if len(search_results)>0: 
        plt.bar(plot_x, plot_y, color="#d6eaf7", width=0.2, align="center")
        plt.bar(plot_x, search_results, color="#3498db", width=0.2, align="center")
    else:
        plt.bar(plot_x, plot_y, color="#3498db", width=0.2, align="center")
    plt.xlabel("Year")
    plt.ylabel("Number of cases")

    ax = plt.gca()
    ax.set_facecolor("#f0f4f8")

    plt.savefig('./app/static/images/chart.png', dpi=300)
    plt.close()



if __name__ == "__main__":
    from document_loader import LexDatabase
    file_path = './data/database.json'
    db = LexDatabase(file_path)
    # docs = db.documents_dict()
    results = n.arange(1, 12, 1) # toy data
    generate_chart(db)
    
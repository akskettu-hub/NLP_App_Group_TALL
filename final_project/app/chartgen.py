import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as n
import re


COLOR = '#34495e'
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR

def case_distribution(data, results):
    results_per_year = dict.fromkeys(data.data.keys(), 0)
    for item in results:
        year = re.search(r'\d{4}', item['title']).group()
        results_per_year[year] += 1
    return results_per_year

def generate_chart(data, search_results={}):
    plot_x = data.data.keys() # gets the years
    plot_y = [len(value.keys()) for key, value in data.data.items()] # gets the number of cases for each year
    # plot_y2 = search_results

    plt.figure(figsize=(10, 2))
    if len(search_results.values())>0: 
        plt.suptitle('Distribution of relevant cases per year', fontsize=10)
        plt.bar(plot_x, plot_y, color="#d6eaf7", width=0.2, align="center")
        plt.bar(plot_x, search_results.values(), color="#3498db", width=0.2, align="center")
    else:
        plt.suptitle('Distribution of all cases per year', fontsize=10)
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
 
    sample_results = [{'rank': 1, 'title': 'KKO:2015:26', 'link': 'https://www.finlex.fi/fi/oikeus/kko/kko/2015/20150026', 'diaarinumero': 'S2013/660', 'antopaiva': '1.4.2015', 'description': 'A Oy oli tehnyt rahoitusyhtiö B Oyj:n kanssa vuokrasopimuksen puhelinjärjestelmän hankkimisesta rahoitusleasingjärjestelyllä. Puhelinjärjestelmän oli A Oy:lle toimittanut tilaussopimuksen perusteella C Oy. B Oyj vaati vuokrasopimuksen purkamisoikeute', 'score': 0.07337869703769684}, {'rank': 2, 'title': 'KKO:2021:9', 'link': 'https://www.finlex.fi/fi/oikeus/kko/kko/2021/20210009', 'diaarinumero': 'S2020/241', 'antopaiva': '10.2.2021', 'description': 'Työnantaja oli 13.5.2015 saanut tiedon työntekijän henkilöön liittyvästä irtisanomisperusteesta. Työnantaja oli 27.5.2015 ilmoittanut työntekijälle harkitsevansa irtisanomista ja varannut työntekijälle tilaisuuden tulla kuulluksi 1.6.2015 järjestettä', 'score': 0.07002493739128113}, {'rank': 3, 'title': 'KKO:2025:21', 'link': 'https://www.finlex.fi/fi/oikeus/kko/kko/2025/20250021', 'diaarinumero': 'S2023/599', 'antopaiva': '13.2.2025', 'description': 'Ulosottoviranomainen oli myynyt ulosottovelallisten omistaman kiinteistön 122 000 euron kauppahinnalla. Myyntiesitteestä oli puuttunut tieto siitä, että kiinteistöllä sijaitsevat maatalousrakennukset kuuluivat kauppaan, minkä vuoksi käräjäoikeus oli ', 'score': 0.06138148158788681}]
    generate_chart(db, case_distribution(db, sample_results)) # toy data
    print(case_distribution(db, sample_results)) # toy data

from data import ImdbData

import matplotlib.pyplot  as plt
import seaborn as sns

sns.set()  # Setting seaborn as default style even if use only matplotlib
sns.set_palette("Paired")  # set color palette

class ImdbViz:
    def __init__(self):
        self.__data = ImdbData()
        self.__df = self.__data.movies


    def show_something(self):
        print("viz1")


    def print_stat(self):
        """Function shows of min, max, mean and median of all numerical features in movies df."""
        df = self.__df
        numerical_features_list = self.__data.numerical_features
        for feature in numerical_features_list:
            print(
            """
            ** {} ** 
            ------------------------
            min:    {}  
            max:    {} 
            mean:   {:.1f} 
            median: {:.1f} 
            """.format(feature,
                    df[feature].min(), 
                    df[feature].max(), 
                    df[feature].mean(), 
                    df[feature].median()))
            
    def plot_numeric_features(self):

        df = self.__df
        numerical_features_list = self.__data.numerical_features
        fig, axes = plt.subplots(nrows=len(numerical_features_list),
                                ncols=2,
                                figsize=(10, 13))
        for i, feature in enumerate(numerical_features_list):
            sns.histplot(data=df, x=feature, kde=True, ax=axes[i, 0])
            sns.boxplot(data=df, x=feature, ax=axes[i, 1])
        plt.tight_layout()
        plt.show()


    def print_best_scores_movies(self):
        df = self.__df
        numeric_features = self.__data.numerical_features
        print("                              Movies with best scores".upper())
        print("""**************************************************************************************""")
        for feature in numeric_features:
            df.sort_values(by = feature, ascending=False, inplace=True, ignore_index= True)
            année = df.loc[0,'year']        
            titre = df.loc[0,'title']
            realisateur = df.loc[0,'directors']
            max_feature = df.loc[0,feature]
        
            print("""{:} ({:}) by {:} with  the highest {:} = {:,}\n""".format(titre, année, ', '.join(realisateur) , feature.replace('_', ' '), max_feature))

    def show_top_10_directors(self):
        barplot_top_N(self.__data.directors, 'directors', 10)

    def show_top_10_genres(self):
        barplot_top_N(self.__data.genre, 'genre', 10)

    def pieplot_genres(self):
        labels = self.__data.genre['genre']
        sizes = self.__data.genre['number_of_movies']
        
        fig1, ax1 = plt.subplots(figsize=(20,10))
        patches, texts, autotexts = ax1.pie(sizes, labels=labels, labeldistance=1.15, 
        autopct='%.0f%%', pctdistance=0.85,
        textprops={'size': 'smaller'},
        shadow=False, radius=0.5, wedgeprops= {'linewidth' : 3, 'edgecolor' : 'white' })
        ax1.axis('equal')
        plt.setp(autotexts, size='small')
        autotexts[0].set_color('white')
        ax1.set_title('Number of films by genre', fontsize=20)
        plt.show()


## Plot top 20 with the highest rate/recette/movie_duration
def barplot_top_N(df, label, n_top):
    """
    Function to make barblot of the top N realisateur with the highest value of feature
    df = data frame
    features = list of names of columns 
    n_top = number of names in final barblot    
    """
    features = list(df.columns)
    features = features[1:]
    num_rows = len(features) // 2
    if len(features) % 2 == 1: num_rows += 1
    f, axes = plt.subplots(nrows=num_rows, ncols=2, figsize=(18, 10))
    for i, feature in enumerate(features):
        df_sorted = df.sort_values(by=feature,
                                ascending=False,
                                inplace=False,
                                ignore_index=True)
        sns.barplot(data=df_sorted.head(n_top),
                    y=label,
                    x=feature,
                    ax=axes[i // 2, i % 2])
        min_rate = df_sorted[feature].min()
        max_rate = df_sorted[feature].max()
        # Add a legend and informative axis label
        axes[i // 2, i % 2].set(xlim=(min_rate, max_rate * 1.01),
                                xlabel=feature)  #, ylabel="",)
        sns.despine(left=True, bottom=True, ax=axes[i // 2, i % 2])
        axes[i // 2, i % 2].set_title(
            f"Top {n_top} {label} with the highest {feature} ", size=12)
    plt.subplots_adjust()
    plt.tight_layout()
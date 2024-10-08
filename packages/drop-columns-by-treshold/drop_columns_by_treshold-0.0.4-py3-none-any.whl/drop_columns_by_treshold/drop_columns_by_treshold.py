import pandas as pd
import seaborn as sns # data visualization library
import matplotlib.pyplot as plt # plotting library

#v0.0.4

# Find out the columns that need to be dropped for a given threshold:
def get_nan_cols(df, nan_percent):
    threshold = len(df.index) * nan_percent
    return [c for c in df.columns if df[c].isnull().sum() >= threshold]


def drop_columns_by_treshold(file_name, nan_percent):
    nan_percent = nan_percent/100

    df = pd.read_csv(file_name)
    sns.heatmap(df.isnull(), cbar=False, cmap='CMRmap')
    plt.title('before drop columns by treshold: missing values showing through heatmap')
    plt.show()

    # billing_subscriber.info()
    print("before delete columns count: ", len(df.columns.tolist()))
    print("before delete columns: ", df.columns.tolist())

    # Find out the columns that need to be dropped for a given threshold:
    cols_to_del = get_nan_cols(df, nan_percent)
    cols_to_del

    print("columns to delete: ", cols_to_del)

    # drop NA with threshold
    #billing_subscriber = billing_subscriber.dropna(thresh=10000 ,axis=1)

    #drop columns with too many NA empty values
    df = df.drop(cols_to_del, axis=1)
    print("remaining columns count: ", len(df.columns.tolist()))
    print("remaining columns: ", df.columns.tolist())
    print("\ntotal row count: ", df.shape[0])

    missing_info = df.isna().sum().to_frame()
    missing_info.columns = ["NA count"]

    print("missing_info: ", missing_info)

    sns.heatmap(df.isnull(), cbar=False, cmap='CMRmap')
    plt.title('after dropped columns by treshold: missing values showing through heatmap')
    plt.show()

    return df



# test
file_name = "billing_subscriber.csv"
threshold = 1 # NA percent 1%

#df = drop_columns_by_treshold(file_name, threshold)

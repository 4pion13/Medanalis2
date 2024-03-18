import argparse

import pandas as pd
from catboost import CatBoostClassifier, Pool
from sklearn.model_selection import train_test_split


def configure_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--savepath' , type=str, required=True)
    parser.add_argument('--train_csv_path' , type = str, required=True)
    return parser


def train(train_csv_path:str, savepath:str ):
    train_df = pd.read_csv(train_csv_path)

    train_df.drop('Unnamed: 0' , axis= 1 ,  inplace = True)


    X = train_df.iloc[:,1:].values
    y = train_df['Disease'].values


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.22 , random_state=42 ,shuffle=True )


    model = CatBoostClassifier()
    model.fit(X_train , y_train)
    model.save_model(savepath , format='cbm')


if __name__ == '__main__':
    args = configure_parser().parse_args()
    train(args.train_csv_path, args.savepath)

from pull_data import pull_data
from user_input import user_input

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    years = user_input()
    data = pull_data(years)
    print(data[(data["home_team"] == "KC")
               & (data["away_team"] == "SF")
               & (data["week"] == 21)].head(20))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

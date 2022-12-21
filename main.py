from pull_data import pull_data
from user_input import user_input

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    years = user_input()
    pull_data(years)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

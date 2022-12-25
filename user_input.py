import datetime

def user_input():
    current_year = datetime.date.today().year
    try:
        my_list = []
        n = int(input("Enter the number of years you'd like to query: "))
        print(f"Enter the years between 1999 and {current_year} to query play-by-play data for: ")

        for i in range(0, n):
            year = int(input())
            if year < 1999 or year > current_year:
                raise ValueError()
            else:
                my_list.append(year)
        return my_list
    except ValueError:
        print('Please input a valid year')



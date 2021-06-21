import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! \n')

    # create lists of cities, months, days to loop against
    cities = ['chicago', 'new york city', 'washington']
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Please specify the city you would like to explore: ' ).lower()
        if city.lower() not in cities:
            print('Sorry! We only have data for Chicago, New York City, and Washington, please try again. \n')
            continue
        else:
            print('Thanks! \n')
            #we're happy with the value given, exit the loop
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Please select a month from January to June that you would like to explore (you may select "all"): ').lower()
        if month.lower() not in months:
            print('Oops! We don\'t have data for this month, please try again. \n')
            continue
        else:
            print('Thanks! \n')
            # we're happy with the value given, exit the loop
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Please select a day of the week that you would like to explore (you may select "all"): ').lower()
        if day.lower() not in days:
            print('Oops! That\'s not a day of the week we\'re looking for, please try again. \n')
            continue
        else:
            print('Thanks! Let\'s calculate some descriptive statistics for you... \n')
            #we're happy with the value given, exit the loop
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most common month:', calendar.month_name[common_month])
    print()

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most common day of the week:', common_day)
    print()

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print('Most common start hour:', common_start_hour)
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Start Station: ', common_start_station)
    print()

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('End Station: ', common_end_station)
    print()

    # display most frequent combination of start station and end station trip
    df['Combo Station'] = df['Start Station'] + ' ' + '/' + ' ' + df['End Station']
    common_combo = df['Combo Station'].mode()[0]
    print('Trip: ', common_combo)
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time (minutes): ', (total_travel_time / 60))
    print()

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time (minutes): ', (mean_travel_time / 60))
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Type Count: \n', user_types)
    print()

    # Display counts of gender
    try:
        gender_types = df['Gender'].value_counts()
        print('Gender Type Counts: \n', gender_types)
    except Exception:
        print('No gender data available...')

    print()

    # Display earliest, most recent, and most common year of birth
    try:
        early_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]

        print('Earliest Birth Year: ', early_year)
        print()
        print('Most Recent Birth Year: ', recent_year)
        print()
        print('Most Common Birth Year:', common_year)
        print()
    except Exception:
        print('No birth year data available...')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Display 5 rows of raw data at the user's request"""
    # creating start and end rows to use as indices
    start_row = 0
    end_row = 5

    # create a while loop to continue providing rows of raw data if desired, and to handle invalid inputs
    while True:
        user_input = input('\nWould you like to see 5 rows of raw data? Enter yes or no.\n').lower()
        if user_input.lower() == 'yes':
            print('\nExtracting Raw Data...\n')
            # Display raw data from start row to end row
            print(df[start_row:end_row])
            # add 5 rows to start and end row to pull next 5 rows
            start_row += 5
            end_row += 5
            continue

        if user_input.lower() == 'no':
            break
            print('-'*40)

        else:
            print('Sorry we didn\'t get that, please enter yes or no if you would like to see some rows of raw data.\n')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

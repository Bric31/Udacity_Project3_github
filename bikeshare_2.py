import time
import pandas as pd
import numpy as np

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
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please, enter the city: ').lower()

    while city not in ['chicago', 'new york city', 'washington']:
        city = input ("Select one city (chicago, new york city OR washington): ").lower()

        if city not in ['chicago', 'new york city', 'washington']:
            print('Please, check your answer, it doesn\'t an accepted option')

    print('You have chosen: {}'.format(city))

    # get user input for month (all, january, february, ... , june)
    month = input('Please, enter the month: ').lower()

    while month not in ['all','january', 'february', 'march', 'april', 'may', 'june','july','august',\
    'september','november','december']:
        month = input('Select one month between january to june : ').lower()

        if month not in ['all','january', 'february', 'march', 'april', 'may', 'june','july','august',\
    'september','november','december']:
            print('Please, check your answer, it doesn\'t an accepted option')

    print('You have chosen: {}'.format(month))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please, enter the day : ').lower()

    while day not in ['all','monday','tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input('Select one day between monday to sunday : ').lower()

        if day not in ['all','monday','tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            print('Please, check your answer, it doesn\'t an accepted option')

    print('You have chosen: {}'.format(day))

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
    df['month'] = df["Start Time"].dt.month
    df['day_of_week'] = df["Start Time"].dt.strftime('%A')
    df['hour'] = df["Start Time"].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june','july','august',\
    'september','november','december']
        month = months.index(month) + 1
        
    
        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    months = ['january', 'february', 'march', 'april', 'may', 'june','july','august',\
    'september','november','december']
    month = [1,2,3,4,5,6]
    dict_month = dict(zip(month, months))
    common_month = dict_month[df['month'].mode()[0]].title()
    print('For the instruction, the month with the most travels is: {}'.format(common_month))

    # display the most common day of week

    common_day = df["day_of_week"].mode()[0]
    print('For the instruction, the day with the most travels is: {}'.format(common_day))

    # display the most common start hour

    common_hour = df["hour"].mode()[0]
    print('For the instruction, the hour with the most travels is: {}'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    common_start_station = df["Start Station"].value_counts().sort_values(ascending=False).reset_index().iloc[0][0]

    print('For the instruction, the common start station is: {}'.format(common_start_station))

    # display most commonly used end station

    common_end_station = df["End Station"].value_counts().sort_values(ascending=False).reset_index().iloc[0][0]

    print('For the instruction, the common end station is: {}'.format(common_end_station))

    # display most frequent combination of start station and end station trip

    common_start_station = df["Start Station"].value_counts().sort_values(ascending=False).reset_index()
    common_end_station = df["End Station"].value_counts().sort_values(ascending=False).reset_index()
    comb_station= common_start_station.merge(common_end_station)
    comb_station["Total"] = comb_station["Start Station"] + comb_station["End Station"]
    common_comb_station = comb_station.sort_values(by=['Total'],ascending=False).iloc[0][0]

    print('For the instruction, the common start-end combination station is: {}'.format(common_comb_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_time_duration = df['Trip Duration'].sum() #In seconds
    t_hours_time_duration = total_time_duration // 3600
    t_minutes_time_duration =  (total_time_duration % 3600) // 60
    t_seconds_time_duration =  (total_time_duration % 3600) % 60

    total_time_duration = "hours: " + str(t_hours_time_duration) + ", " + "minutes: " + str(t_minutes_time_duration) + ", " +\
        "second: " + str(t_seconds_time_duration)

    print('For the instruction, the total trip time duration is: {}'.format(total_time_duration))

    # display mean travel time

    mean_time_duration = df['Trip Duration'].mean() #In seconds
    m_hours_time_duration = mean_time_duration // 3600
    m_minutes_time_duration =  (mean_time_duration % 3600) // 60
    m_seconds_time_duration =  round((mean_time_duration % 3600) % 60,2)

    mean_time_duration = "hours: " + str(m_hours_time_duration) + ", " + "minutes: " + str(m_minutes_time_duration) + ", " +\
        "second: " + str(m_seconds_time_duration)

    print('For the instruction, the mean trip time duration is: {}'.format(mean_time_duration))

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_types_count = df['User Type'].value_counts()
    print("The user type counts is: \n",
    user_types_count)

    print("")

    # Display counts of gender

    col_dataframe = df.columns
    if "Gender" in col_dataframe:
        gender_count = df["Gender"].value_counts()
        print("The user gender counts is: {} ".format(gender_count))
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe')

    print("")
    # Display earliest, most recent, and most common year of birth

    if "Birth Year" in col_dataframe:
        oldest_person = df['Birth Year'].min()
        print("The earliest year of birth is: ", str(oldest_person))
        print("")
        youngest_person = df['Birth Year'].max()
        print("The most recent year of birth is: ", str(youngest_person))
        print("")
        common_year_birth = df['Birth Year'].mode()
        print("The most common year of birth is: ", str(common_year_birth[0]) )

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

    else:
        print('Birth year stats cannot be calculated because Gender does not appear in the dataframe')

def raw_data (df):
    """Show five rows of data, if the user want to see more information, he/she must to indicate "no" to skip """
    print('If you want to see more data, press "no" to skip')
    x = 0
    while (input()!= 'no'):
        x = x+5
        print(df.head(x))


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
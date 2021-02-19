from os import close
import time
from asyncore import ExitNow

import numpy as np
import pandas as pd
from pandas import DataFrame

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#########################################################################################################################
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    #while True :
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = str(input('write Which city you like to see its data (chicago ,new york city ,washington):')).lower()
    while city  not in CITY_DATA :
        print('pleas enter right informations')
        city = str(input('write Which city you like to see its data (chicago ,new york city ,washington):')).lower()
    else: 
        city = city.lower()

    with_filter=str(input('Would you like to filter the data by date or by weekday or No for without filters(date or weekday or no) :'))
    with_filter=with_filter.lower()

    while  with_filter  not in ['date', 'weekday', 'no', ] :
        print('pleas enter right informations')
        with_filter=str(input('Would you like to filter the data by daynumber or by weekday or No for without filters :'))

    if with_filter == 'date':
    
        # get user input for month (all, january, february, ... , june)
        month =str(input('Which month you like to see its data  (all, january, february, ... , june):'))
        while month  not in ['january', 'february', 'march', 'april', 'may', 'june'  , 'all'] :
            print('pleas enter right informations')
            month =str(input('Which month you like to see its data  (all, january, february, ... , june):'))
        else: 
            month =month.lower()
        ## day_of_month = input('Which day of month you like to see its data  (all, or number from (1-31))')
        day = int(input('Which day you like to see its data  (all, 1>>>30):'))
        
 
        print(day )
            
    
    elif with_filter == 'weekday':
        # get user input for month (all, january, february, ... , june)
        month =str(input('Which month you like to see its data  (all, january, february, ... , june):'))
        while month  not in ['january', 'february', 'march', 'april', 'may', 'june'  , 'all'] :
            print('pleas enter right informations')
            month =str(input('Which month you like to see its data  (all, january, february, ... , june):'))
        else: 
            month =month.lower()
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day =str(input('Which day you like to see its data  (all, monday, tuesday, ... sunday):'))
        while day  not in ['all','wednesday', 'thursday', 'friday', 'sturday', 'sunday', 'monday', 'tuesday']:
            print('pleas enter right informations')
            day =str(input('Which day you like to see its data  (all, monday, tuesday, ... sunday)'))
        else:
            day=day.lower()
    elif with_filter == 'no':
        month = 'all'
        day = 'all'

    print('-'*40)
    return city, month, day  
#########################################################################################################################
def load_data(city, month,  day):
    #Loads data for the specified city and filters by month and day if applicable.
    df = pd.read_csv(CITY_DATA[city])
    #print(df)
    # convert the Start Time column to datetime
    df['Start Time'] =pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['trip'] = df['Start Station'] + ' to '+df['End Station']
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        #elif day_of_month != 'all':
        #df = df[df['day'] == day_of_month]
        #day = months.index(month) + 1
    # filter by day of week if applicable
    if day != 'all':
        try:
        # filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day.title()]
        except:
            month_df = df[df['month'] == month]
            df=month_df[df['day'] == day]
    return df
#########################################################################################################################
def time_stats(df):
    """  ."""
    print('This sellectionpart of your data ' , df  )
    start_time = time.time()
    # display the most common month
    popular_month = df['month'].mode()[0]
    print('\nMost Frequent Start month:', popular_month)
    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('\nMost Frequent Start day:', popular_day)
    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#########################################################################################################################
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    print('\nMost Frequent start_station:', df['Start Station'].mode()[0] ,'with count ', len(df['Start Station'].mode()[0]))
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\nMost Frequent end_station:', popular_end_station ,'with count ', len( popular_end_station))
    # display most frequent combination of start station and end station trip
    popular_trip = df['trip'].mode()[0]
    print('\nMost Frequent  trip:', popular_trip,'with count ', len( popular_trip))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#########################################################################################################################
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    travel_sum=df['Trip Duration'].sum()
    travel_mean=df['Trip Duration'].mean()
    travel_count=df['Trip Duration'].count()+1
    # display total travel time
    print('\ntotal travel_sum:', travel_sum)
    print('\ntotal travel_count:', travel_count)
    print('\naverage travel time:', travel_mean)
    # display mean travel time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#########################################################################################################################
def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    print(' The counts of user types is',df['User Type'].value_counts())
    # Display counts of gender
    try:
        print(' Thecounts of user types is n\\', df['Gender'].value_counts())
        # Display earliest, most recent, and most common year of birth
        print('The Users earliest year of birth=',df['Birth Year'].min())
        print('The Users most recent year of birth=',df['Birth Year'].max())
        print('The Users  most common year of birth=',df['Birth Year'].mode())
    except:
        pass
    print("\nThis took %s seconds." % (time.time() - start_time))

    print(df.head())
    see_more_data =str(input('Do you want to see more raw  data ? (yes or no):')).lower()
    x , y = 5 , 10
    while see_more_data not in ['yes' , "no"]  :
        print('pleas choose ')
        see_more_data =str(input('Do you want to see more raw  data ? (yes or no):')).lower()
    while see_more_data == '' or see_more_data == 'yes':
        print(df.iloc[x:y])
        x +=5 
        y +=5
        see_more_data =str(input('Do you want to see more raw  data ? ((yes or no ) (press Enter to speed process):')).lower()
    print('-'*40)
#########################################################################################################################
def steps ():
    #while True:
    city, month, day = get_filters()
    df = load_data(city, month, day)
    time_stats(df)
    print('\nCalculating The Most Frequent Times of Travel...\n')
    check =str(input('Is  sellection right  (yes to complete , no to resellection n\\)'))
    while check not in ['yes' , 'no']:
        check =str(input('"pleas only yes or no "Is  sellection right  (yes to complete , no to resellection n\\)'))
    if check.lower() != 'yes':
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df) 
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        restart = str(input('\nWould you like to restart? Enter yes or no.\n'))
        if restart.lower() != 'yes':
            exit()
    elif check.lower() == 'yes':
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        restart = str(input('\nWould you like to restart? Enter yes or no.\n'))
        if restart.lower() != 'yes':
           exit()
    else:
        restart = str(input('\nWould you like to restart? Enter yes or no.\n'))
        if restart.lower() != 'yes':
            exit()
#########################################################################################################################
def main():
    while True:
        steps ()
if __name__ == "__main__":
    main()

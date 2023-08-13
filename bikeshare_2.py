# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 16:58:19 2023

@author: dimopoulosp
"""

import time
import datetime
import calendar
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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please enter a city (Chicago, New York City, Washington): ").lower()

    # Define a list of valid cities
    valid_cities = ['chicago', 'new york city', 'washington']
    
    # Define a list of valid months
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june']
    
    # Define a list of valid days
    valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    # Use a while loop to handle invalid inputs
    while city.lower() not in valid_cities:
        print("Invalid input. Please try again.")
        city = input("Please enter a city (Chicago, New York City, Washington): ").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Please enter a month (all, january, february, ... , june): ').lower()
    if month not in valid_months:
        month = 'all'

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please enter a day of week (all, monday, tuesday, ... sunday): ').lower()
    if day not in valid_days:
        day = 'all'

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
    file_name = CITY_DATA[city]
    df = pd.read_csv(file_name)
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        df['day_of_week'] = df['day_of_week'].apply(lambda x: calendar.day_name[x])
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month from the Start Time column to create an month column
    df['month'] = df['Start Time'].dt.month 
    
    # TO DO: display the most common month
    common_month = df['month'].value_counts().idxmax()

    print("The most common month is:", common_month)

    # extract day from the Start Time column to create a day column
    df['day'] = df['Start Time'].dt.dayofweek 
    
    # TO DO: display the most common day of week
    common_day = df['day'].value_counts().idxmax()

    print("The most common day is:", common_day)

    # Extract hour from the Start Time column
    df['hour'] = df['Start Time'].dt.hour
    
    # TO DO: display the most common start hour
    most_common_hour = df['hour'].value_counts().idxmax()
    
    print("The most common start hour is:", most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station is:", most_common_start_station)

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station is:", most_common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    # Create a new column for the combination of start and end stations
    df['Start-End Combo'] = df['Start Station'] + ' - ' + df['End Station']
    
    most_frequent_combo = df['Start-End Combo'].value_counts().idxmax()
    print("The most frequent combination of start station and end station trip is:", most_frequent_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    # Calculate the total travel time
    df['Trip Duration'] = df['Trip Duration'].fillna(0).astype(int)
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time is:", total_travel_time, "seconds")
    
    total_travel_time_hours = total_travel_time / 3600
    print("The total travel time in hours is:", total_travel_time_hours)

    # TO DO: display mean travel time
    mean_travel_time = total_travel_time / len(df)
    print("The mean travel time is:", mean_travel_time, "seconds")

    mean_travel_time_readable = str(datetime.timedelta(seconds=mean_travel_time))
    print("The mean travel time in hours is:", mean_travel_time_readable)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_counts = df['User Type'].value_counts()

    print("Counts of user types:")
    print(user_type_counts)

    # TO DO: Display counts of gender
    # Check if 'Gender' column exists
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("Counts of gender:")
        print(gender_counts)
    else:
        print("No gender data available for this city.")

    # TO DO: Display earliest, most recent, and most common year of birth
    # Calculate the earliest year of birth
    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        print("Earliest year of birth:", earliest_year)
        
        # Calculate the most recent year of birth
        most_recent_year = df['Birth Year'].max()
        print("Most recent year of birth:", most_recent_year)
        
        # Calculate the most common year of birth
        most_common_year = df['Birth Year'].mode()[0]
        print("Most common year of birth:", most_common_year)
        
    else:
        print("No Birth Year data available for this city.")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_raw_data(df):
    # Read the data from the CSV file
    #data = pd.read_csv(file_name)

    # Initialize variables
    start_index = 0
    end_index = 5

    while True:
        # Prompt the user if they want to see 5 lines of raw data
        show_data = input("Do you want to see 5 lines of raw data? Enter 'yes' or 'no': ").lower()

        if show_data == 'yes':
            # Display the next 5 lines of raw data
            print(df[start_index:end_index])
            start_index += 5
            end_index += 5
        elif show_data == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

        # Check if there is no more raw data to display
        if start_index >= len(df):
            print("No more raw data to display.")
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        print_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

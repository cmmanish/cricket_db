import fnmatch
import os
from datetime import datetime
import pandas as pd
import mysql
import mysql.connector
import yaml

from db_scripts.mysql_connect import create_connection_mysql

good_team_list = ["Australia", "India", "New Zealand", "Pakistan", "England", "Sri Lanka", "West Indies",
                  "South Africa", "Bangladesh"]


def hasTwoInnings(yaml_dictionary):
    try:
        if yaml_dictionary['innings'][1]:
            print("Normal ODI")
            return True
    except:
        print("Truncated ODI")
        return False
    pass


def convert_yaml_2_list(yaml_file_dir, file_name):
    cricsheet_id = file_name.split(".")[0];
    file = yaml_file_dir + file_name
    with open(file, 'r') as f:

        yaml_dictionary = yaml.load(f)

        if yaml_dictionary['info']['teams']:
            team1 = yaml_dictionary['info']['teams'][0]
            team2 = yaml_dictionary['info']['teams'][1]

            if team1 and team2 not in good_team_list:
                return []
        if yaml_dictionary['info']['match_type'] != 'ODI':
            return []
        if yaml_dictionary['info']['gender'] != 'male':
            return []
        try:
            year = int(str(yaml_dictionary['info']['dates'][0]).split("-")[0])
            print(year)
        except:
            print("yaml_dictionary['info']['dates'][0].year Missing")
            year = 0000
        try:
            venue = str(yaml_dictionary['info']['city'])
            # print(yaml_dictionary)
        except:
            print("yaml_dictionary['info']['city'] Missing")
            venue = str(yaml_dictionary['info']['venue'])
        db_row_list = []

        bat_first = str(yaml_dictionary['innings'][0]['1st innings']['team'])
        bat_second = ""
        try:
            if yaml_dictionary['innings'][1]:
                bat_second = str(yaml_dictionary['innings'][1]['2nd innings']['team'])
        except:
            bat_second = ""
        delivery_list_1 = yaml_dictionary['innings'][0]['1st innings']['deliveries']

        for delivery_dict in delivery_list_1:

            for key, value in delivery_dict.items():
                ball_number = float(key)
                bowler_name = str(value['bowler'])
                batsman_name = str(value['batsman'])
                non_striker_name = str(value['non_striker'])
                run_batsman = int(value['runs']['batsman'])
                run_extras = int(value['runs']['extras'])
                runs_total = int(value['runs']['total'])

                try:
                    if value['wicket']:
                        wicket = 1
                        player_out = str(value['wicket']['player_out'])
                        wicket_type = str(value['wicket']['kind'])
                except:
                    wicket = 0
                    player_out = ""
                    wicket_type = ""
                row_tuple = (cricsheet_id,
                             venue, year, bat_first, bat_second, ball_number, bowler_name, batsman_name,
                             non_striker_name, run_batsman, run_extras, runs_total,wicket, player_out, wicket_type)

                db_row_list.append(row_tuple)

        if hasTwoInnings(yaml_dictionary):
            delivery_list_2 = yaml_dictionary['innings'][1]['2nd innings']['deliveries']

            for delivery_dict in delivery_list_2:
                for key, value in delivery_dict.items():
                    ball_number = float(key)
                    bowler_name = str(value['bowler'])
                    batsman_name = str(value['batsman'])
                    non_striker_name = str(value['non_striker'])
                    run_batsman = int(value['runs']['batsman'])
                    run_extras = int(value['runs']['extras'])
                    runs_total = int(value['runs']['total'])

                    try:
                        if value['wicket']:
                            wicket = 1
                            player_out = str(value['wicket']['player_out'])
                            wicket_type = str(value['wicket']['kind'])
                    except:
                        wicket = 0
                        player_out = ""
                        wicket_type = ""
                    row_tuple = (cricsheet_id,
                                 venue, year, bat_first, bat_second, ball_number, bowler_name, batsman_name,
                                 non_striker_name, run_batsman, run_extras, runs_total, wicket, player_out, wicket_type)

                    db_row_list.append(row_tuple)
    return db_row_list


def insert_multiple_row_to_db(records_to_insert):
    row_count = len(records_to_insert)
    print("Total row to insert: " + str(row_count))
    try:
        connection = create_connection_mysql()
        mySQL_insert_query = '''INSERT INTO odi_ball_by_ball (cricsheet_id, venue, year, ball_team, bat_team, ball_number,
                        bowler_name, batsman_name, non_striker_name, runs_batsman, runs_extras, runs_total, wicket, player_out, wicket_type)
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s, %s, %s, %s) '''

        cursor = connection.cursor()
        cursor.executemany(mySQL_insert_query, records_to_insert)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into Laptop table")

    except mysql.connector.Error as error:
        print("Failed to insert record into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def list_all_files(yaml_file_dir):
    yaml_file_list = []
    listOfFiles = os.listdir(yaml_file_dir)
    pattern = "*.yaml"
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
            yaml_file_list.append(entry)
    return yaml_file_list


# def main1():
#     # year_array = ["2019", "2018", "2018", "2017", "2016", "2016", "2015"]
#     year_array = ["2020"]
#     for year in year_array:
#         yaml_file_dir = "../../BuildMatchDB/yaml_dump/" + year + "_male/"
#         yaml_file_list = list_all_files(yaml_file_dir)
#         print(str(len(yaml_file_list)) + " YAML files one per match for year " + year)
#
#         start = datetime.now()
#         for each_yaml_file in yaml_file_list:
#             print("Now reading " + str(each_yaml_file))
#             #
#             db_row_list = convert_yaml_2_list(yaml_file_dir, each_yaml_file)
#             for each_row in db_row_list:
#                 insertOneRowToDb(each_row)
#                 print('Insert to db took ' + str(datetime.now() - start))

def main():
    # year_array = ["2018", "2018", "2017", "2016", "2016", "2015","2014", "2013", "2012", "2011", "2010", "2009", "2008", "2007", "2006"]
    year_array = ["2019", "2020", "2021"]
    # year_array = ["2005"]
    for year in year_array:
        yaml_file_dir = "../../BuildMatchDB/yaml_dump/" + year + "_male/"
        yaml_file_list = list_all_files(yaml_file_dir)
        print(str(len(yaml_file_list)) + " YAML files one per match for year " + year)

        start = datetime.now()
        for each_yaml_file in yaml_file_list:
            print("Now reading " + str(each_yaml_file))

            db_row_list = convert_yaml_2_list(yaml_file_dir, each_yaml_file)
            if db_row_list != []:
                insert_multiple_row_to_db(db_row_list)
                print('Insert to db took ' + str(datetime.now() - start))

if __name__ == '__main__':
    main()

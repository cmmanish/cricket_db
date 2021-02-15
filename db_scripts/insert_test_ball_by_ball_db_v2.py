import fnmatch
import os
from datetime import datetime
import yaml
import pymysql

yaml_file_dir = '/Users/manish/Documents/yaml_dump/2021_male/'
database_name="CricketDb"
user_name="root"
password="gofundme1"
def hasTwoInnings(yaml_dictionary):
    try:
        if yaml_dictionary['innings'][1]:
            print("Normal ODI")
            return True
    except:
        print("Truncated ODI")
        return False
    pass


def yaml2list(file_name):
    cricsheet_id = file_name.split(".")[0];
    file = yaml_file_dir + file_name
    with open(file, 'r') as f:

        yaml_dictionary = yaml.load(f)

        if yaml_dictionary['info']['match_type'] != 'ODI':
            return []
        try:
            year = int(file.split("_male")[0].split("/")[2])
            print(year)
        except:
            print("yaml_dictionary['info']['dates'][0].year Missing")
            year = 0000

        if yaml_dictionary['info']['gender'] != 'male':
            return []
        try:
            year = int(file.split("_male")[0].split("/")[2])
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
                run_extras = int(value['runs']['extras'])
                run_batsman = int(value['runs']['batsman'])
                runs_total = int(value['runs']['total'])

                row_tuple = (cricsheet_id,
                             venue, year, bat_first, bat_second, ball_number, bowler_name,
                             batsman_name,
                             non_striker_name, run_batsman, run_extras, runs_total)

                db_row_list.append(row_tuple)

        if hasTwoInnings(yaml_dictionary):
            delivery_list_2 = yaml_dictionary['innings'][1]['2nd innings']['deliveries']

            for delivery_dict in delivery_list_2:
                for key, value in delivery_dict.items():
                    ball_number = float(key)
                    bowler_name = str(value['bowler'])
                    batsman_name = str(value['batsman'])
                    non_striker_name = str(value['non_striker'])
                    run_extras = int(value['runs']['extras'])
                    run_batsman = int(value['runs']['batsman'])
                    runs_total = int(value['runs']['total'])

                    row_tuple = (
                    cricsheet_id, venue, year, bat_second, bat_first, ball_number, bowler_name,
                    batsman_name, non_striker_name, run_batsman, run_extras, runs_total)

                    db_row_list.append(row_tuple)

    return db_row_list


pass


def create_connection_mysql():
    """ create a database connection to a SQLite database """
    try:
        connection = pymysql.connect(host='127.0.0.1', database=database_name, user=user_name, password=password)
        print("connect successful!!")
        return connection
    except pymysql.Error as e:
        print(e)
    return None


def insertOneRowToDb(each_row):
    connection = create_connection_mysql()
    try:
        print("Going to insert " + str(each_row))
        with connection.cursor() as cursor:

            sql = '''INSERT INTO odi_ball_by_ball_v2 (cricsheet_id, venue, year, ball_team, bat_team, ball_number,
                bowler_name, batsman_name, non_striker_name, runs_batsman, runs_extras, runs_total)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s) '''
            print(sql)
            cursor.execute(sql, each_row)
            connection.commit()
            print(str(each_row[0]) + ' inserted to db')

    except pymysql.Error as e:
        # Rolling back in case of error
        connection.rollback()
        print(e)
    # Closing the connection
    print("Data inserted")
    connection.close()


def list_all_files():
    yaml_file_list = []
    listOfFiles = os.listdir(yaml_file_dir)
    pattern = "*.yaml"
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
            yaml_file_list.append(entry)
    return yaml_file_list


def main():
    yaml_file_list = list_all_files()
    print(str(len(yaml_file_list)) + " YAML files one per ODI's")

    start = datetime.now()
    for each_yaml_file in yaml_file_list:
        print("Now serving " + str(each_yaml_file))
    #
        db_row_list = yaml2list(each_yaml_file)
        for each_row in db_row_list:
            insertOneRowToDb(each_row)
            print('Insert to db took ' + str(datetime.now() - start))


if __name__ == '__main__':
    main()

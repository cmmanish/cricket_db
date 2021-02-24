Log into Db:
`docker exec -it docker-tutorial_mysql_db_1 mysql -u root -ppassword`
Create user
`CREATE USER 'user'@'%' IDENTIFIED BY 'password';`
Grant Perm
`GRANT ALL PRIVILEGES ON cricketdb.* to 'user'@'%';`


`select count(runs_batsman) from odi_ball_by_ball where  batsman_name like'%Kohli%' and year=2019`

`select count(runs_batsman) from odi_ball_by_ball where  batsman_name like'%Kohli%' and year=2019`
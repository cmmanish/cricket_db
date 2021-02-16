Log into Db:
`docker exec -it docker-tutorial_db_1 mysql -u root -ppassword`
Create user
`CREATE USER 'user'@'%' IDENTIFIED BY 'password';`
Grant Perm
`GRANT ALL PRIVILEGES ON cricketdb.* to 'user'@'%';`
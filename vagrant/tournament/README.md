# Swiss-System Tournament 

### Prerequisites
This is the project from the course: Intro to Database  at Udacity: https://www.udacity.com/course/viewer#!/c-ud197-nd/

### Project Description
This program will simulate the first two rounds of a Swiss Tournament. In the first round each player will be randomly assigned to another and a win or loss will be recorded. In the second round, those players who have one win will play one another and those with one loss will play one another.

Develop a database schema to store details of a games matches between players. Then write a Python module to rank the players and pair them up in matches in a tournament.

### Files include:

 * tournament.py: Contains the implementation for the Swiss tournament
 * tournament.sql: Contains the SQL queries to create the database, tables and views
 * tournament_test.py: Contains the test cases for tournament.py
 * tournament_script.py: Contains the scripts to add some players and simulate the tournament result


### How to start

 1. Install Vagrant and Virtualbox
 	* VirtualBox: https://www.virtualbox.org/wiki/Downloads
 	* Vagrant: https://www.vagrantup.com/downloads
 2. Start Vagrant
 	* open Terminal or cmd
    * browse to the vagrant folder `cd vagrant`
	* turn on the virtual machine: Type `vagrant up`
 3. login to VM
 	* login to the virtual machine: Type `vagrant ssh`
 	* Type `cd /vagrant/tournament`
 4. Open PSQL
 	* type `psql'
 	* copy and paste the content from "tournament.sql" into the terminal
 	* type `\q` to quit the PSQL
 5. Runn the application
 	* type python `tournament_test.py` in the path `vagrant/tournament`

### Test Pass Result
Success! All tests pass!
vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ python tournament_test.py
1. Old matches can be deleted.
2. Player records can be deleted.
3. After deleting, countPlayers() returns zero.
4. After registering a player, countPlayers() returns 1.
5. Players can be registered and deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After one match, players with one win are paired.
Success! All tests pass!

### Extra Credit

If the top two players have the same won match count, and have won more than 0 games, then the standings is ordered by total number of wins by games played in descending order.
#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
# A Swiss-System tournament is a kind of game or sports tournament in which players 
# are not eliminated when they are lose a match, but are paired in each round with opponents
# having approximately the same win-loss record.

import psycopg2

def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db,cursor
    except:
        print ("<error message>")


def deleteMatches():
    """Remove all the match records from the database."""
    db, db_cursor = connect()
    query = "DELETE FROM matches"
    db_cursor.execute(query)
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db, db_cursor = connect()
    query = "TRUNCATE players"
    db_cursor.execute(query)
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db, db_cursor = connect()
    query = "SELECT COUNT(id) AS num FROM players"
    db_cursor.execute(query)
    results = db_cursor.fetchone()
    db.close()
    if results:
        return results[0];
    else:
        return '0'

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db, db_cursor = connect()
    query = "INSERT INTO players (name) VALUES (%s)"
    parameter = (name,)
    db_cursor.execute(query, parameter)
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, db_cursor = connect()
    query = "SELECT * FROM total_wins;"
    db_cursor.execute(query)
    results = db_cursor.fetchall()

    db.close()
    return results 

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, db_cursor = connect()
    query = "INSERT INTO matches (winner, loser) VALUES (%s, %s)"
    parameter = (winner, loser,)
    db_cursor.execute(query, parameter)
    db.commit()
    db.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db, db_cursor = connect()
    results = playerStandings()
    pairings = []
    count = len(results)

    for x in range (0, count-1, 2):
        paired_list = (results[x][0], results[x][1], results[x+1][0],results[x+1][1])
        pairings.append(paired_list)

    db.close()
    return pairings




#!/usr/bin/python
# Allow Display of elements in HTML

import COREMatchSchedule
import COREDependencies


class ColorTeam:

    """ Determines the label color for each team cell in order for the user to better understand what data
        is submitted and when to generate reports """

    def __init__(self):

        """ Connects to database and populates dictionaries and arrays with team and match data """

        self._schedule = COREMatchSchedule.SCHEDULE
        self._teams_in_db = []
        self._team_matches_in_db = {}
        self._my_team = COREDependencies.COREConstants.TEAM_NUMBER

        self._db_connection = COREDependencies.pymysql.connect(host=COREDependencies.COREDatabaseCredentials.DB_HOST,
                                                               user=COREDependencies.COREDatabaseCredentials.DB_USER,
                                                               password=COREDependencies.COREDatabaseCredentials.DB_PASS,
                                                               db=COREDependencies.COREConstants.COMPETITION_NAME,
                                                               charset='utf8mb4',
                                                               cursorclass=COREDependencies.pymysql.cursors.DictCursor)

        try:
            with self._db_connection.cursor() as cursor:
                cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE" +
                               " TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='" +
                               str(COREDependencies.COREConstants.COMPETITION_NAME) + "'")
                table_name = cursor.fetchone()
                while table_name is not None:
                    self._teams_in_db.append(table_name['TABLE_NAME'])
                    table_name = cursor.fetchone()

                for team in self._teams_in_db:
                    count = 0
                    cursor.execute(("SELECT " + COREDependencies.COREConstants.MATCH_NUMBER['match_number'] +
                                    " FROM `" + str(team) + "` ORDER BY `match_id`"))
                    matches = cursor.fetchone()

                    while matches is not None:
                        values = matches.values()
                        if count == 0:
                            for value in values:
                                self._team_matches_in_db[team] = (value,)
                            count = 1
                        else:
                            for value in values:
                                self._team_matches_in_db[team] += (value,)
                        matches = cursor.fetchone()
                    # Goal is to create dictionary with key team number and value: tuple of all match submitions
        finally:
            self._db_connection.close()

    def _find_team_from_schedule(self, team_number):

        """ Searches the match schedule for all instances where the desired team_number is present
            - team_number: team that is to be searched for
            - returns: list of all match numbers where team_number exists """

        match_num = 1
        instances = []
        for match in COREDependencies.COREMatchSchedule.SCHEDULE:
            for team in match:
                if team == team_number:
                    instances.append(match_num)
            match_num += 1
        return instances

    def _find_highest_match(self):

        """ Finds the most recent match number submitted
            - returns: int """
        highest = 1
        for team in self._team_matches_in_db:
            for match in self._team_matches_in_db[team]:
                if match > highest:
                    highest = match
        return highest

    def find_color(self, team_number, match_number):

        """ Uses data from the match schedule and what is available in the database to color code cells
            the teams cells to return the following:
                Grey - Not Submitted post match
                Blue - Submitted data
                Green - Ready to Generate Report
                Red - Not Ready to Generate Report
                orange - My Team
            - team_number: Team number that is available in the schedule
            - match_number: Valid match number the team in question has """

        if team_number == self._my_team:
            return 'orange'
        exists = False
        team_matches = self._find_team_from_schedule(team_number)

        """Validate Existance"""
        for match in team_matches:
            if match == match_number:
                # -- makes sure team exists in schedule
                exists = True
        if exists == False:
            # -- print some error or something that team is not in schedule placeholder error 'color'
            return 'error'

        """Blue"""
        for teamz in self._team_matches_in_db:
            if teamz == str(team_number):
                exists = True
                for matches in self._team_matches_in_db[teamz]:
                    if matches == match_number:
                        return 'blue'

        """Grey"""
        if exists is True:
            if self._find_highest_match() >= match_number:
                return 'grey'

        """Green / Red"""
        if exists is False:
            if match_number == team_matches[0]:
                return 'green'
            else:
                return 'red'

        if exists is True:
            highest_in_db = 1
            theo_latest_in_db = 1
            latest_in_db = 1
            for teamaz in self._team_matches_in_db:
                for each in self._team_matches_in_db[teamaz]:
                    if each > theo_latest_in_db:
                        latest_in_db = each
                if teamaz == str(team_number):
                    # -- finds team in db
                    for matches in self._team_matches_in_db[teamaz]:
                        if matches > highest_in_db:
                            highest_in_db = matches
            round_num = 1
            for round in self._schedule:
                if round_num < match_number:
                    for buddie in round:
                        if buddie == team_number:
                            theo_latest_in_db = round_num
                round_num += 1
            flag = False
            if theo_latest_in_db == highest_in_db:
                for matchez in team_matches:
                    if flag is True:
                        if matchez == match_number:
                            return 'green'
                    if matchez == theo_latest_in_db:
                        flag = True
        return 'red'

    def header_color(self, match_number, teams):

        """ Uses data from the match schedule and what is available in the database to color code
            the match headers to return the following:
                Grey - Past Match
                Green - Ready to Generate Report
                Red - Not Ready to Generate Report
            - teams: tuple of all team numbers in the desired match
            - match_number: Valid match number the teams in question have """

        red_count = 0
        green_count = 0
        blue_count = 0
        grey_count = 0
        orange_count = 0
        for team in teams:
            color = self.find_color(team, match_number)
            if color == 'green':
                green_count += 1
            if color == 'red':
                red_count += 1
            if color == 'blue':
                blue_count += 1
            if color == 'grey':
                grey_count += 1
            if color == 'orange':
                orange_count += 1
        if (green_count == 6) or (orange_count == 1 and green_count == 5):
            return 'green'
        if (blue_count > 0) or (grey_count == 5 and orange_count == 1):
            return 'grey'
        return 'red'

print("Content-type:text/html\r\n\r\n")
print('<html>')
print('<head>')
print('<title>Team 2062s Scouting Match Table Report</title>')
print('</head>')
print('<body>')
print('<link href="css/app.css" rel="stylesheet" type="text/css" />')

cellColorizer = ColorTeam()
print('<table>')
print('<tr>')
print('<td> CORE MATCH SCHEDULE </td>')
for i in range(1, 7):
    if i <= 3:
        print('<td> RED' + str(i) + '</td>')
    else:
        print('<td> RED' + str((i-3)) + '</td>')
print('</tr>')
match_num = 1
for match in COREDependencies.COREMatchSchedule.SCHEDULE:
    print('<tr>')
    print('<td class ="' + cellColorizer.header_color(match_num, match) +
          '"><a href="COREMatchReport.py?RedTeam1=' + str(match[0]) +
          '&RedTeam2=' + str(match[1]) + '&RedTeam3=' + str(match[2]) +
          '&BlueTeam1=' + str(match[3]) + '&BlueTeam2=' + str(match[4]) +
          '&BlueTeam3=' + str(match[5]) + '&MatchNumber=' + str(match_num) +
          '">' + str(match_num) + '</td>')
    for team in match:
        print('<td class ="' + cellColorizer.find_color(team, match_num) + '"> ' + str(team) + ' </td>')
    print('</tr>')
    match_num += 1

print('</table>')
print('</body>')
print('</html>')

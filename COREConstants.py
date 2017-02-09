
""" Various constants used throughout the program that are intended primarily to map form fields,
    but also for key names
        - form dependency:
            Needs to be the same names as those given by the html form.
            It is important that these names appear EXACTLY the same as those supplied by the front end!
        - no dependency:
            Names that will be visually displayed on output tables.
            Should be named in accordance of which they are displaying, but the name is not dependant on any
            other input or variable names"""

"""===========================================
Scout HTML input field names (form dependency)
-------------------------------------------"""

CHECKBOX_NAMES = [
    'hasAuto'
]
RADIO_NAMES = [
    'defenceType',
    'hasDefender'
]
NUMBER_NAMES = [
    'numhighgoals',
    'numlowgoals'
]
TEXT_NAMES = [
    'comments'
]

RADIO_VALUES = {
    'defenceType': ('Moat', 'Rockwall', 'RoughTerrain'),
    'hasDefender': ('Yes', 'No')
}

ALL_NAMES = []

for checkbox in CHECKBOX_NAMES:
    ALL_NAMES.append(checkbox)
for number in NUMBER_NAMES:
    ALL_NAMES.append(number)
for text in TEXT_NAMES:
    ALL_NAMES.append(text)
for radio in RADIO_NAMES:
    ALL_NAMES.append(radio)

#irrelevant field that will hopefully be deleted after reframing of the report interface

TEAM_NUMBER_FIELDS = [
    'RedTeam1',
    'RedTeam2',
    'RedTeam3',
    'BlueTeam1',
    'BlueTeam2',
    'BlueTeam3'
]

MATCH_NUMBER = 'matchNum'

"""=====================================
Match Report Row Headers (no dependency)
-------------------------------------"""

REPORT_HEADER = [
    'High Goal Accuracy',
    'Auto pts'
]

"""=============================================
Match Report input field names (form dependency)
---------------------------------------------"""

RANK_REPORT_FIELD_NAMES = {
    'CSV': 'CSV',
    'ranking_options': 'ranking_types'
}

""" RANK_OPTIONS:
        - Tuple of the following data (IN ORDER):
            + Name of statistic to rank by from REPORT_HEADER
            + Order in which teams should be ranked. The following are accepted
                'descending' - Ranking from best to worst
                'ascending' - Ranks from worst to best
                'category' - Ranks based on multiple strings given a 3'd argument.
            + (ORDER SPECIFIC ARGUMENT) Should only be supplied if order is 'category'.
            A tuple of all possible submission data for the supplied rank_statistic
            category corresponding to the statistic's RADIO_VALUES values in order of
            which should be displayed first, best -> worst.
            Intended to be used for ranking based on a priority of strings.
    EX: 'High Goal Accuracy': ('high_goal_accuracy', 'descending')
    EX: 'Highest Auto Type': ('highest_auto_type', 'category', ('breach', 'reach', 'no_interaction')) """

RANK_OPTIONS = [
    ('High Goal Accuracy', 'descending')
]
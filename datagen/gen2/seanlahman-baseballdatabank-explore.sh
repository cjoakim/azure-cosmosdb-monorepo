#!/bin/bash

# Explore the size and shape of the seanlahman/baseballdatabank csv files.
# Chris Joakim, Microsoft

# ./seanlahman-baseballdatabank-explore.sh > seanlahman-baseballdatabank-explore.txt

find . | grep sourcedata/seanlahman/baseballdatabank | grep csv$ > seanlahman-baseballdatabank-files-list.txt

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/core/Managers.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/core/Managers.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/core/Fielding.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/core/Fielding.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/core/Parks.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/core/Parks.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/core/People.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/core/People.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/core/PitchingPost.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/core/PitchingPost.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/core/Teams.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/core/Teams.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/core/Appearances.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/core/Appearances.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/core/TeamsFranchises.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/core/TeamsFranchises.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/core/Batting.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/core/Batting.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/core/ManagersHalf.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/core/ManagersHalf.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/core/FieldingOF.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/core/FieldingOF.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/core/Pitching.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/core/Pitching.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/core/HomeGames.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/core/HomeGames.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/core/BattingPost.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/core/BattingPost.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/core/TeamsHalf.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/core/TeamsHalf.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/core/SeriesPost.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/core/SeriesPost.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/core/FieldingPost.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/core/FieldingPost.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/core/AllstarFull.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/core/AllstarFull.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/core/FieldingOFsplit.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/core/FieldingOFsplit.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/contrib/AwardsManagers.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/contrib/AwardsManagers.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/contrib/AwardsPlayers.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/contrib/AwardsPlayers.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/contrib/Salaries.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/contrib/Salaries.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/contrib/Schools.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/contrib/Schools.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/contrib/AwardsSharePlayers.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/contrib/AwardsSharePlayers.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/contrib/CollegePlaying.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/contrib/CollegePlaying.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/contrib/HallOfFame.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/contrib/HallOfFame.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/contrib/AwardsShareManagers.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/contrib/AwardsShareManagers.csv

echo '-'
wc ./sourcedata/seanlahman/baseballdatabank-2022.2/upstream/Teams.csv
head -3 ./sourcedata/seanlahman/baseballdatabank-2022.2/upstream/Teams.csv
echo '-'

# cat sourcedata/seanlahman/baseballdatabank-2022.2/files-list.txt

echo 'done'

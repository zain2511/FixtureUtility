from Generate_fixture import Generate_Fixture
from Umpiring_Assignment import Umpiring_Assignment
from Post_Schedule import Post_Schedule
import sys
import datetime

# object creation for used classes
gnrt = Generate_Fixture()
assign = Umpiring_Assignment()
schedule = Post_Schedule()

print("Enter number of games per team: ",end="")
game_per_team = int(input())

print("Enter games per week: ", end="")
game_per_week = int(input())

team_info, final_fixture_list = gnrt.generate(game_per_team, game_per_week)
num_team = len(team_info)
if(game_per_team >= num_team):
	sys.exit("Game per team should be less than number of teams.")

home_game_list,home_game_count_dict,umpiring_list,umpiring_count_dict = assign.assign_umpiring(final_fixture_list, team_info, num_team, game_per_team)

print("Enter tournament start date(mm/dd/yyyy): ", end="")
start_date = datetime.datetime.strptime(input(),'%m/%d/%Y')

schedule.post_schedule_excel(final_fixture_list, start_date, umpiring_list, umpiring_count_dict, home_game_list, home_game_count_dict, team_info, game_per_week, game_per_team)







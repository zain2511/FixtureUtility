import xlrd
import itertools
import random
import math
import time

class Generate_Fixture:

	def organize_fixture(self, created_fixture_list, num_team, game_per_week, no_of_week, team_name):

		# Keep track of number of games per week
		week_dictionary = {x:0 for x in team_name} 
		week_list = []
		final_fixture = []
		
		# loop to create weekly fixtures 
		for j in range(no_of_week):
			i = 0

			if len(created_fixture_list) < game_per_week:
				while i < len(created_fixture_list):
					week_list.append(created_fixture_list.pop(0))

			else:
				start_time = time.time()
				# Loop to organize fixtures for a week with no clash
				while i < game_per_week:
					picked_game = created_fixture_list[0]
			
					if (picked_game not in week_list) and (week_dictionary[picked_game[0]] <= j) and (week_dictionary[picked_game[1]] <= j):
						week_list.append(picked_game)
						week_dictionary[picked_game[0]] += 1
						week_dictionary[picked_game[1]] += 1
						created_fixture_list.pop(0)
						i += 1
						
					else:
						created_fixture_list.append(created_fixture_list.pop(0))
					
					
					if time.time() - start_time > 1:
						break

			final_fixture.append(week_list)
			week_list = []

		# add unassigned games to the end
		if created_fixture_list != []:
			final_fixture.append(created_fixture_list)

		return final_fixture


	def fixture_generation(self, team_info, team_count, game_per_team, game_per_week):

		# create a list with all team name
		team_name = [name[0] for name in team_info]

		#create a cartesian product for all the elements in list
		fixture_list = list(itertools.combinations(team_name,2))

		# Find top teams and bottom teams based on ranking
		top_teams = [x[0] for x in team_info if x[3] < (team_count - game_per_team)]
		bottom_teams = [x[0] for x in team_info if x[3] > (game_per_team + 1)]


		# Alter fixtures for no game between top and bottom team
		for game in fixture_list:
			if game[0] in top_teams and game[1] in bottom_teams:
				fixture_list.remove(game)
			elif game[0] in bottom_teams and game[1] in top_teams:
				fixture_list.remove(game)

		# dictionary to keep track of games a team is playing		
		team_count_dict = {x:0 for x in team_name}
		unorganized_list = []

		# Add must play games for top and bottom teams
		i = 0
		while i < (len(fixture_list)):
			if fixture_list[i][0] in top_teams or fixture_list[i][1] in top_teams or fixture_list[i][0] in bottom_teams or fixture_list[i][1] in bottom_teams:
				unorganized_list.append(fixture_list[i])
				team_count_dict[fixture_list[i][0]] += 1
				team_count_dict[fixture_list[i][1]] += 1
				fixture_list.remove(fixture_list[i])
			else:
				i += 1

		# Generating remaining fixtures randomly. it will keep generating untill each team has required games
		temp_dict = team_count_dict.copy()
		temp_list = fixture_list.copy()
		temp_unorganized = unorganized_list.copy()
		flag = True
		while flag:
			for key in team_count_dict:
				if team_count_dict[key] != game_per_team:
					team_count_dict = temp_dict.copy()
					fixture_list = temp_list.copy()
					unorganized_list = temp_unorganized.copy()
					random.shuffle(fixture_list)
					j = 0
					while j < len(fixture_list):
						if team_count_dict[fixture_list[j][0]] < game_per_team and team_count_dict[fixture_list[j][1]] < game_per_team:
							unorganized_list.append(fixture_list[j])
							team_count_dict[fixture_list[j][0]] += 1
							team_count_dict[fixture_list[j][1]] += 1
							fixture_list.remove(fixture_list[j])
						else:
							j += 1
					flag = True
					break

				flag = False

		#print(team_count_dict)
		#print(len(unorganized_list))

		no_of_week = int(math.ceil(len(unorganized_list) / game_per_week))
		random.shuffle(unorganized_list)

		return self.organize_fixture(unorganized_list, team_count, game_per_week, no_of_week, team_name)

		


	def generate(self, game_per_team, game_per_week):
		team_workbook = xlrd.open_workbook("Team_Info.xlsx")
		sheet = team_workbook.sheet_by_index(0)

		team_info = [(sheet.cell_value(row, 0), sheet.cell_value(row, 1), sheet.cell_value(row, 2), 
					int(sheet.cell_value(row, 3))) for row in range(1, sheet.nrows)]

		team_count = len(team_info)
		

		#team_workbook.close()

		#print(team_info)
		final_fixture_list = self.fixture_generation(team_info, team_count, game_per_team, game_per_week)		

		return team_info, final_fixture_list

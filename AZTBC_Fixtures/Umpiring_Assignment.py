import math
import random

class Umpiring_Assignment:

	def assign_umpiring(self, final_fixture_list, team_info, num_team, game_per_team):
		
		
		# distinct team on the basis of region
		north_list = [x[0] for x in team_info if x[2] == "North"]
		south_list = [x[0] for x in team_info if x[2] == "South"]
		
		# temporary list to be used
		home_game_list = []
		umpiring_list = []
		north_list_copy = north_list.copy()
		south_list_copy = south_list.copy()

		# Dictionaries to keep the count of umpiring and home game
		umpiring_count_dict = {x[0]: math.ceil(game_per_team/2) for x in team_info}
		#home_game_count_dict = {x[0]: math.ceil(game_per_team/2) for x in team_info}
		home_game_count_dict = {x[0]: 0 for x in team_info}
		travelled_nort_dict = {x:len(north_list) - 1 for x in south_list}
		#print(home_game_count_dict)

		for game_list in final_fixture_list:

			temp_list = []
			home_temp = []
			# Divide List as per saturday and sunday games
			list1 = [x for tupl in game_list[:(num_team//4)] for x in tupl]
			list2 = [x for tupl in game_list[(num_team//4):] for x in tupl]


			# Assign the Home Team
			for i,game in enumerate(game_list):

				if game[0] in north_list:
					if game[1] in north_list:
						if home_game_count_dict[game[0]] <= home_game_count_dict[game[1]]:
							home_temp.append((game[0], "North"))
							home_game_count_dict[game[0]] += 1
						else:
							home_temp.append((game[1], "North"))
							home_game_count_dict[game[1]] += 1
					else:
						if travelled_nort_dict[game[1]] > 0 and home_game_count_dict[game[0]] < (game_per_team // 2):
							home_temp.append((game[0], "North"))
							home_game_count_dict[game[0]] += 1
							travelled_nort_dict[game[1]] -= 1
						else:
							home_temp.append((game[1],"South"))
							home_game_count_dict[game[1]] += 1

				else:
					if game[1] in south_list:
						if home_game_count_dict[game[0]] <= home_game_count_dict[game[1]]:
							home_temp.append((game[0],"South"))
							home_game_count_dict[game[0]] += 1
						else:
							home_temp.append((game[1],"South"))
							home_game_count_dict[game[1]] += 1
					else:
						if travelled_nort_dict[game[0]] > 0  and home_game_count_dict[game[1]] < (game_per_team // 2):
							home_temp.append((game[1],"North"))
							home_game_count_dict[game[1]] += 1
							travelled_nort_dict[game[0]] -= 1
						else:
							home_temp.append((game[0],"South"))
							home_game_count_dict[game[0]] += 1

			home_game_list.append(home_temp)

			# Assign umpiring

			new_south_list = south_list_copy.copy()
			new_north_list = north_list_copy.copy() 
			random.shuffle(new_south_list)
			random.shuffle(new_north_list)
			i = 0
			count_l1 = len(list1) // 2
			count_l2 = len(list2) // 2

			while i < len(game_list):

			
				try:
					if home_temp[i][1] == "South":
						if i < len(game_list) // 2:
							for k in range(len(new_south_list)):

								if new_south_list[k] not in list1:
									temp_list.append(new_south_list[k])
									i += 1
									umpiring_count_dict[new_south_list[k]] -= 1

									if umpiring_count_dict[new_south_list[k]] == 0:
										south_list_copy.remove(new_south_list[k])
									new_south_list.pop(k)
									break
								else:
									if k == len(new_south_list) - 1:
										temp_list.append("Error")
										i += 1
						else:
							if new_south_list == []:
								temp_list.append("Error")
								i += 1
								break

							for k in range(len(new_south_list)):

								if new_south_list[k] not in list2:
									temp_list.append(new_south_list[k])
									i += 1
									umpiring_count_dict[new_south_list[k]] -= 1

									if umpiring_count_dict[new_south_list[k]] == 0:
										south_list_copy.remove(new_south_list[k])
									new_south_list.pop(k)
									break
								else:
									if k == len(new_south_list) - 1:
										temp_list.append("Error")
										i += 1

					else:
						if i < len(game_list)//2:
							for k in range(len(new_north_list)):

								if new_north_list[k] not in list1:
									temp_list.append(new_north_list[k])
									i += 1
									umpiring_count_dict[new_north_list[k]] -= 1

									if umpiring_count_dict[new_north_list[k]] == 0:
										north_list_copy.remove(new_north_list[k])
									new_north_list.pop(k)
									break
								else:
									if k == len(new_north_list) - 1:
										temp_list.append("Error")
										i += 1
						else:
							#print(len(new_north_list))
							if new_north_list == []:
								temp_list.append("Error")
								i += 1
								break
							for k in range(len(new_north_list)):

								if new_north_list[k] not in list2:
									temp_list.append(new_north_list[k])
									i += 1
									umpiring_count_dict[new_north_list[k]] -= 1

									if umpiring_count_dict[new_north_list[k]] == 0:
										north_list_copy.remove(new_north_list[k])
									new_north_list.pop(k)
									break
								else:
									if k == len(new_north_list) - 1:
										temp_list.append("Error")
										i += 1
					#print(temp_list)
					#print("Inside Try", i)

				except IndexError:
					
					temp_list.append("Error")
					i += 1
			umpiring_list.append(temp_list)

		
		return home_game_list,home_game_count_dict,umpiring_list,umpiring_count_dict

			






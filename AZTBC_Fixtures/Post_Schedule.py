from pandas.tseries.holiday import USFederalHolidayCalendar
import math
import datetime
import xlsxwriter

class Post_Schedule:

	def post_schedule_excel(self, final_fixture_list, start_date, umpiring_list, umpiring_count_dict, home_game_list, home_game_count_dict, team_info, game_per_week, game_per_team):
		
		no_of_week = int(math.ceil(len(final_fixture_list) / game_per_week))

		# First saturday of the start date
		final_date = start_date + datetime.timedelta(days = (5 - start_date.weekday()))

		# Dictionary for playing ground
		playing_ground_dict = {x[0]:x[1] for x in team_info}

		# Excel object
		workbook = xlsxwriter.Workbook('FinalizedSchedule.xlsx')
		sheet = workbook.add_worksheet()
		row = 1
		col = 0
		bold_format = workbook.add_format({'bold': True, 'align': 'center'})
		date_format = workbook.add_format({'num_format': 'mm/dd/yy'})

		# for extended weekend detection
		cal = USFederalHolidayCalendar()
		holidays = cal.holidays(start=start_date, end=start_date.replace(year = start_date.year + 1)).to_pydatetime()
		

		# Adjust column width
		sheet.set_column('B:F', 18)
		# sheet.set_column('C:C', 15)
		# sheet.set_column('D:D', 15)
		# sheet.set_column('E:E', 15)
		# sheet.set_column('E:E', 15)

		sheet.write('A1',"Day", bold_format)
		sheet.write('B1',"Date", bold_format)
		sheet.write('C1',"Home Team", bold_format)
		sheet.write('D1',"Away Team", bold_format)
		sheet.write('E1',"Ground", bold_format)
		sheet.write('F1',"Umpires", bold_format)

		# Print fixtures and dates on excel
		for i, fix in enumerate(final_fixture_list):
			sat_check = final_date + datetime.timedelta(days = (i*7))
			if sat_check - datetime.timedelta(days = 1) in holidays or sat_check + datetime.timedelta(days = 2) in holidays:
				final_date = final_date + datetime.timedelta(days = 7)

			for j in range(len(fix)):
				if home_game_list[i][j][0] == fix[j][0]:
					away = fix[j][1]
				else:
					away = fix[j][0]

				if j < len(fix) // 2:
					sheet.write(row, col, "Sat")
					#print("1 ", final_date + datetime.timedelta(days = (i*7)))
					sheet.write(row, col + 1, final_date + datetime.timedelta(days = (i*7)), date_format)
					# sheet.write(row, col + 2, home_game_list[i][j][0])
					# sheet.write(row, col + 3, away)
					# sheet.write(row, col + 4, playing_ground_dict[home_game_list[i][j][0]])
					# sheet.write(row, col + 5, umpiring_list[i][j])
				else:
					sheet.write(row, col, "Sun")
					#print("2 ", final_date + datetime.timedelta(days = (i*7 + 1)))
					sheet.write(row, col + 1, final_date + datetime.timedelta(days = (i*7 + 1)), date_format)
				sheet.write(row, col + 2, home_game_list[i][j][0])
				sheet.write(row, col + 3, away)
				sheet.write(row, col + 4, playing_ground_dict[home_game_list[i][j][0]])
				sheet.write(row, col + 5, umpiring_list[i][j])
				row += 1

		# Print analytics stats on excel
		sheet.set_column('J:O', 18)

		sheet.write('J1',"Team Name", bold_format)
		sheet.write('K1',"Home Ground", bold_format)
		sheet.write('L1',"Region", bold_format)
		sheet.write('M1',"Home", bold_format)
		sheet.write('N1',"Away", bold_format)
		sheet.write('O1',"Umpiring", bold_format)

		row = 1
		col = 9

		for j, team in enumerate(team_info):
			sheet.write(row, col, team[0])
			sheet.write(row, col + 1, team[1])
			sheet.write(row, col + 2, team[2])
			sheet.write(row, col + 3, home_game_count_dict[team[0]])
			sheet.write(row, col + 4, game_per_team - home_game_count_dict[team[0]])
			sheet.write(row, col + 5, (game_per_team // 2) - umpiring_count_dict[team[0]])

			row += 1

		workbook.close()		




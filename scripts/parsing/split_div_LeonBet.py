# block_name_list = ['Катар\nЭквадор\n20.11 19:00\n3.57\n3.25\n2.17\n+326\nАнглия\nИран\n21.11 16:00\n1.32\n4.87\n11.40\n+320\nСенегал\nНидерланды\n21.11 19:00\n6.30\n3.90\n1.57\n+339\nСША\nУэльс\n21.11 22:00\n2.59\n3.09\n2.94\n+323\nАргентина\nСаудовская Аравия\n22.11 13:00\n1.16\n7.50\n19.00\n+328\nДания\nТунис\n22.11 16:00\n1.46\n4.17\n8.00\n+333\nМексика\nПольша\n22.11 19:00\n2.73\n3.14\n2.74\n+322\nФранция\nАвстралия\n22.11 22:00\n1.23\n6.30\n13.40\n+343\nМарокко\nХорватия\n23.11 13:00\n4.58\n3.34\n1.88\n+340\nГермания\nЯпония\n23.11 16:00\n1.43\n4.58\n7.60\n+358\nИспания\nКоста-Рика\n23.11 19:00\n1.20\n6.30\n16.30\n+335\nБельгия\nКанада\n23.11 22:00\n1.36\n4.94\n8.90\n+347\nШвейцария\nКамерун\n24.11 13:00\n1.73\n3.50\n5.30\n+325\nУругвай\nРеспублика Корея\n24.11 16:00\n1.79\n3.51\n4.87\n+335\nПортугалия\nГана\n24.11 19:00\n1.40\n4.40\n9.10\n+329\nБразилия\nСербия\n24.11 22:00\n1.46\n4.37\n7.40\n+349\nУэльс\nИран\n25.11 13:00\n2.23\n3.07\n3.62\n+331\nКатар\nСенегал\n25.11 16:00\n3.75\n3.19\n2.13\n+340\nНидерланды\nЭквадор\n25.11 19:00\n1.63\n3.95\n5.40\n+349\nАнглия\nСША\n25.11 22:00\n1.66\n3.85\n5.30\n+347\nТунис\nАвстралия\n26.11 13:00\n2.82\n3.03\n2.74\n+328\nПольша\nСаудовская Аравия\n26.11 16:00\n1.63\n3.80\n5.80\n+348\nФранция\nДания\n26.11 19:00\n1.99\n3.34\n4.04\n+345\nАргентина\nМексика\n26.11 22:00\n1.57\n3.88\n6.40\n+336\nЯпония\nКоста-Рика\n27.11 13:00\n1.87\n3.35\n4.64\n+338\nБельгия\nМарокко\n27.11 16:00\n1.54\n4.18\n6.20\n+349\nХорватия\nКанада\n27.11 19:00\n1.78\n3.71\n4.55\n+344\nИспания\nГермания\n27.11 22:00\n2.55\n3.36\n2.78\n+357\nКамерун\nСербия\n28.11 13:00\n4.60\n3.40\n1.86\n+331\nРеспублика Корея\nГана\n28.11 16:00\n2.66\n2.99\n2.94\n+329\nБразилия\nШвейцария\n28.11 19:00\n1.50\n4.15\n7.00\n+352\nПортугалия\nУругвай\n28.11 22:00\n2.05\n3.38\n3.76\n+349\nНидерланды\nКатар\n29.11 18:00\n1.34\n5.00\n9.50\n+224\nЭквадор\nСенегал\n29.11 18:00\n2.93\n3.20\n2.53\n+209\nИран\nСША\n29.11 22:00\n3.53\n3.43\n2.10\n+220\nУэльс\nАнглия\n29.11 22:00\n6.00\n4.00\n1.58\n+219\nАвстралия\nДания\n30.11 18:00\n6.60\n3.73\n1.59\n+211\nТунис\nФранция\n30.11 18:00\n13.60\n5.50\n1.26\n+214\nПольша\nАргентина\n30.11 22:00\n4.84\n4.04\n1.68\n+218\nСаудовская Аравия\nМексика\n30.11 22:00\n6.50\n4.05\n1.54\n+218\nКанада\nМарокко\n01.12 18:00\n3.24\n3.41\n2.23\n+211\nХорватия\nБельгия\n01.12 18:00\n4.07\n3.72\n1.87\n+223\nКоста-Рика\nГермания\n01.12 22:00\n12.50\n5.50\n1.27\n+227\nЯпония\nИспания\n01.12 22:00\n9.30\n5.50\n1.31\n+228\nГана\nУругвай\n02.12 18:00\n4.85\n3.64\n1.76\n+218\nРеспублика Корея\nПортугалия\n02.12 18:00\n9.30\n4.98\n1.35\n+214\nКамерун\nБразилия\n02.12 22:00\n10.50\n5.10\n1.32\n+226\nСербия\nШвейцария\n02.12 22:00\n2.81\n3.34\n2.53\n+215']

def split_list(list, parsing_date):
    result = []
    for count, value in enumerate(list):
        splitted = value.split('\\n')
        splitted = value.split('\n')
        # print(f'splitted:\n{splitted}')
        separator = ':'        
        
        how_many_games = [x for x in splitted if separator in x]
        # print(f'\n\nhow_many_games: {how_many_games}')
        # print(f'\n\nlen(how_many_games): {len(how_many_games)}')
        start_search = 0 
        # print(f'len(splitted): {len(splitted)}')
        for x in range(len(how_many_games)):
            current_position = splitted.index(how_many_games[x], start_search)
            # print(f'\nx: {x}')
            # print(f'how_many_games[x]: {how_many_games[x]}')
            # print(f'start_search: {start_search}')
            # print(f'current_position: {current_position}')  
            index_of_date = splitted[current_position].index(':')  
            date_of_game = splitted[current_position][:index_of_date-3]
            time_of_game = splitted[current_position][index_of_date-2:]
            team_A = splitted[current_position - 2]
            team_B = splitted[current_position - 1]
            if splitted[current_position + 1].find('МАРЖА') >= 0:
                w1 = splitted[current_position + 2]
                draw = splitted[current_position + 3]
                w2 = splitted[current_position + 4]
            else:
                w1 = splitted[current_position + 1]
                draw = splitted[current_position + 2]
                w2 = splitted[current_position + 3]
            result.append(['LeonBet',\
                            'World cup 2022',\
                            date_of_game,\
                            time_of_game,\
                            team_A,\
                            team_B,\
                            w1,\
                            draw,\
                            w2,\
                            parsing_date
                            ])
            start_search = current_position + 1
        
    # print(f'\nresult:\n {result}')
    return result
    
# split_list(block_name_list)
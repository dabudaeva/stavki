# block_name_list = ['.\nП1 X П2 Б Тотал М 1 Фора 2\n17:00\n20.11\nКатар\nЭквадор\n3.7\n3.25\n2.13\n1.75\n2.0\n2.1\n2.55\n0\n1.52\n14:00\n21.11\nАнглия\nИран\n1.3\n4.9\n12.5\n2.05\n2.5\n1.78\n2.02\n-1.5+\n1.82\n17:00\n21.11\nСенегал\nНидерланды\n6.6\n3.8\n1.58\n2.08\n2.5\n1.77\n1.82\n+1-\n2\n20:00\n21.11\nСША\nУэльс\n2.6\n3.05\n3\n1.87\n2.0\n1.93\n1.8\n0\n2.05\n11:00\n22.11\nАргентина\nСаудовская Аравия\n1.16\n7.4\n21\n1.97\n3.0\n1.83\n1.83\n-2+\n1.97\n14:00\n22.11\nДания\nТунис\n1.45\n4.2\n8\n2.1\n2.5\n1.75\n1.78\n-1+\n2.05\n17:00\n22.11\nМексика\nПольша\n2.75\n3.15\n2.75\n1.85\n2.0\n1.95\n1.9\n0\n1.9\n20:00\n22.11\nФранция\nАвстралия\n1.22\n6.3\n15\n2\n3.0\n1.8\n1.7\n-1.5+\n2.18\n11:00\n23.11\nМарокко\nХорватия\n4.7\n3.3\n1.88\n1.78\n2.0\n2.05\n1.43\n+1-\n2.85\n14:00\n23.11\nГермания\nЯпония\n1.43\n4.7\n7.5\n2.12\n3.0\n1.72\n2.2\n-1.5+\n1.7\n17:00\n23.11\nИспания\nКоста-Рика\n1.2\n6.3\n17\n1.77\n2.5\n2.08\n1.67\n-1.5+\n2.25\n20:00\n23.11\nБельгия\nКанада\n1.37\n4.9\n9\n1.75\n2.5\n2.1\n2.05\n-1.5+\n1.8\n11:00\n24.11\nШвейцария\nКамерун\n1.72\n3.55\n5.5\n1.78\n2.0\n2.03\n2.45\n-1+\n1.55\n14:00\n24.11\nУругвай\nЮжная Корея\n1.75\n3.55\n5.3\n1.7\n2.0\n2.15\n2.55\n-1+\n1.55\n17:00\n24.11\nПортугалия\nГана\n1.4\n4.4\n9\n2.1\n2.5\n1.75\n1.67\n-1+\n2.25\n20:00\n24.11\nБразилия\nСербия\n1.45\n4.4\n7.6\n1.85\n2.5\n2\n1.75\n-1+\n2.1\n11:00\n25.11\nУэльс\nИран\n2.25\n3.05\n3.65\n1.83\n2.0\n1.97\n1.55\n0\n2.5\n14:00\n25.11\nКатар\nСенегал\n3.8\n3.15\n2.15\n1.7\n2.0\n2.15\n2.6\n0\n1.52\n17:00\n25.11\nНидерланды\nЭквадор\n1.65\n3.95\n5.4\n1.82\n2.5\n2\n2.12\n-1+\n1.75\n20:00\n25.11\nАнглия\nСША\n1.65\n3.9\n5.6\n2.02\n2.5\n1.8\n2.15\n-1+\n1.72']

def split_list(list):
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
            result.append(['SportBet',\
                            'World cup 2022',\
                            splitted[current_position + 1],\
                            splitted[current_position],\
                            splitted[current_position + 2],\
                            splitted[current_position + 3],\
                            splitted[current_position + 4],\
                            splitted[current_position + 5],\
                            splitted[current_position + 6]
                            ])
            start_search = current_position + 1
        
    # print(f'\nresult:\n {result}')
    return result
    
# split_list(block_name_list)
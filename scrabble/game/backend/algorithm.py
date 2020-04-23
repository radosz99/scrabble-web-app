from .anagram import find_anagrams

class Algorithm:
    def __init__(self, letters, board):
        self.letters = [x.lower() for x in letters]
        self.board = board
        self.create_patterns()

    def algorithm_engine(self,trie):
        sorted_list_of_valid_words=self.get_valid_words(trie)
        if(len(sorted_list_of_valid_words)!=0):
            info_result = sorted_list_of_valid_words[len(sorted_list_of_valid_words)-1]
            points = info_result[1]
            best = info_result[0][0]
            coords = info_result[0][1]

            letters_not_used = self.letters_not_used(best, coords[0])

            self.update_board(coords,best)

        
        else:
            best=''
            points=0
            letters_not_used=self.letters

        return self.board,points,letters_not_used, best.upper()

    def letters_not_used(self,word, pattern_letters):
        for char in pattern_letters:
            position = word.find(char)
            help_word = word[0 : position ] + word[position + 1 : len(word)]
            word=help_word
        
        for char in word:
            self.letters.remove(char)

        letters_not_used=self.letters
        return letters_not_used

    def get_valid_words(self, trie):
        info = self.get_letters_for_anagram()
        board_letters = info[0]
        brigdes=info[1]
        #znajdowanie wszystkich anagramow
        anagrams = find_anagrams(str(self.letters)+board_letters,trie)
        #wybor wszystkich anagramow mogacych pasowac do patternow, wstepna selekcja
        valid_anagrams = self.find_probably_valid_words(anagrams=anagrams, letters=str(self.letters), board_letters=board_letters, brigdes=brigdes)
        #znajdowanie wyrazow rzeczywiscie pasujacych do patternow, ostateczna selekcja
        list_of_valid_words = self.find_certainly_valid_words(valid_anagrams)
        #sortowanie listy od najlepszych ruchow (najwiecej punktowanych)
        sorted_list_of_valid_words = sorted(list_of_valid_words, key=lambda tup: tup[1])

        return sorted_list_of_valid_words

    def check_if_valid(self,word):
        list_of_possible_patterns=[]
        _word = word
        for char in self.letters:
            position = _word.find(char)
            if(position!=-1):
                help_word = _word[0 : position ] + _word[position + 1 : len(_word)]
                _word = help_word
        positions=[]
        if(len(_word)!=0):
            for char in _word:
                index = word.find(char)
                positions.append(index)
        else:
            return ''

        for pattern in self.pattern_board:
            if(str(pattern[0])==_word):
                if(len(_word)==2):
                    if(pattern[3]>=positions[0] and len(word)<=9):
                        if(pattern[4]>=(len(word)-positions[1]-1)):
                            list_of_possible_patterns.append((word, (pattern[0],pattern[1],pattern[2],positions[0], pattern[4], pattern[5], pattern[6])))
                if(len(_word)==1):
                    if(pattern[3]==positions[0]):
                        if(pattern[4]>=(len(word)-positions[0]-1)):
                            list_of_possible_patterns.append((word, pattern))
 
        if(len(list_of_possible_patterns)!=0):
            return list_of_possible_patterns
        else:
            return ''

    def find_certainly_valid_words(self, sorted_by_length):
        word=''
        list_of_valid_words=[]
        counter=1
        #ewaluacja ruchow i zapis do listy
        while(counter!=len(sorted_by_length)+1):
            word_to_check=sorted_by_length[len(sorted_by_length)-counter]
            words = self.check_if_valid(word_to_check) 
            for word in words:
                if(word!=''):
                    result = self.evaluate_move(word)
                    list_of_valid_words.append((word,result))
            counter=counter+1

        return list_of_valid_words

    def find_probably_valid_words(self, anagrams, letters, board_letters, brigdes):
        max_letters_from_board_to_connect = 2 #maksymalny most, czyli przewiduje max 2
        new_anagrams = []

        for anagram in anagrams:
            new_anagram=anagram
            _board_letters=board_letters
            whether_letter=False
            help_counter=0
            letters_find_in_both_place=[]
            for char in letters:
                index = new_anagram.find(char)
                #sprawdzenie czy znak znajduje sie w literach uzytkownika
                if(index!=-1): 
                    whether_letter=True
                    index_board = _board_letters.find(char)
                    #sprawdzenie czy znak znajduje sie w literach dostepnych na planszy, jesli tak to usuwany jest z dostepnych liter na planszy
                    if(index_board==-1):
                        help_anagram = new_anagram[0 : index ] + new_anagram[index + 1 : len(new_anagram)]
                        new_anagram = help_anagram
                    else:
                        letters_find_in_both_place.append(char)
                        help_counter=help_counter+1
                        help_board_letters = _board_letters[0 : index_board ] + _board_letters[index_board + 1 : len(_board_letters)]
                        _board_letters = help_board_letters
            #pierwszy warunek to, sprawdzenie czy w slowie jest wiecej niz 2 znaki spoza liter uzytkownika, czyli z planszy (mostek = 2 litery, kat prosty = 1 litera)
            #drugi warunek to sprawdzenie czy w slowie znajduja sie litery z planszy (jesli nie to string mialby dlugosc 0, czyli zawieral jedynie litery uzytkownika, co jest niedopuszczalne)
            #trzeci warunek to sprawdzenie czy zostala usunieta chociaz jedna literka (czyli, ze slowo zawiera chociaz jedna litere uzytkownika)
            if(len(new_anagram)<=max_letters_from_board_to_connect+help_counter and len(new_anagram)>0 and whether_letter==True):
                #usuniecie tych co znalazly sie w obu miejscach w celach walidacji
                for ch in letters_find_in_both_place:
                    index = new_anagram.find(ch)
                    if(index!=-1):
                        help_new_anagram = new_anagram[0 : index ] + new_anagram[index + 1 : len(new_anagram)]
                        new_anagram = help_new_anagram
                #sprawdzenie czy pasuje do mostkow
                if(len(new_anagram)==2):
                    for key in brigdes:
                        if(new_anagram==key):
                            position1 = anagram.find(str(key)[0])
                            position2 = anagram.find(str(key)[1])
                            if(position2-position1==brigdes[key]):
                                new_anagrams.append(anagram)
                                break
                elif(len(new_anagram)<2):
                    new_anagrams.append(anagram)

        sorted_by_length = sorted(new_anagrams, key=len)
        return sorted_by_length
    
    def get_string_with_others_best(self,sorted_list_of_valid_words):
        #string z pozostalymi slowami
        str_other_best_valid=''
        for i in range (6):
            if(len(sorted_list_of_valid_words)>i+1):
                info_other = sorted_list_of_valid_words[len(sorted_list_of_valid_words)-2-i]
                str_other_best_valid=str_other_best_valid+info_other[0][0]+' - '+str(info_other[1]) + " pts., "
        str_other_best_valid = str_other_best_valid[0:len(str_other_best_valid)-2]
        return str_other_best_valid+' Total: ' + str(len(sorted_list_of_valid_words))+ ' words.'

    def update_board(self,coords, best):
        if(coords[5]=='v'):
            for x in range (len(best)):
                if(x!=coords[3]):
                    self.board[coords[1]+x-coords[3]][coords[2]]=best[x].upper()
        if(coords[5]=='h'):
            for x in range (len(best)):
                if(x!=coords[3]):
                    self.board[coords[1]][coords[2]+x-coords[3]]=best[x].upper()

    def create_patterns(self):
        self.pattern_board=[]
    
        pattern_h_board = self.get_right_angle_patterns(self.board, 'h')
        pattern_v_board = self.get_right_angle_patterns(self.transpose_board(self.board),'v')
        pattern_v_bridges = self.get_bridge_patterns(pattern_v_board)
        pattern_h_bridges = self.get_bridge_patterns(pattern_h_board)
        for pattern in pattern_h_board:
            self.pattern_board.append(pattern)
        for pattern in pattern_v_board:
            self.pattern_board.append(pattern)
        for pattern in pattern_v_bridges:
            self.pattern_board.append(pattern)
        for pattern in pattern_h_bridges:
            self.pattern_board.append(pattern)
        

    def evaluate_move(self, word_with_pattern):
        coords = word_with_pattern[1]
        word = word_with_pattern[0]
        sum=0
        bonus=0
        if(len(word)-len(coords[0])==7):
            bonus=50
        multiplier=1
        if(coords[5]=='v'):
            for x in range (len(word)):
                if(len(coords[0])==2):
                    if(x!=coords[3] and x!=(coords[3]+coords[6])):
                        info = self.get_field_value(word[x], coords[1]+x-coords[3],coords[2])
                        sum=sum+int(info[0])
                        multiplier=int(multiplier*int(info[1]))
                else:
                    if(x!=coords[3]):
                        info = self.get_field_value(word[x], coords[1]+x-coords[3],coords[2])
                        sum=sum+int(info[0])
                        multiplier=int(multiplier*int(info[1]))

        if(coords[5]=='h'):
            for x in range (len(word)):
                if(len(coords[0])==2):
                    if(x!=coords[3] and x!=(coords[3]+coords[6])):
                        info = self.get_field_value(word[x], coords[1],coords[2]+x-coords[3])
                        sum=sum+int(info[0])
                        multiplier=int(multiplier*int(info[1]))
                else:
                    if(x!=coords[3]):
                        info = self.get_field_value(word[x], coords[1],coords[2]+x-coords[3])
                        sum=sum+int(info[0])
                        multiplier=int(multiplier*int(info[1]))
        return sum*multiplier+bonus
                        


    def get_field_value(self, char, x,y):
        word_multiplier=1
        letter_multiplier=1
        letter_value = self.get_char_value(char)
        if(((x==1 or x==13)and (y==1 or y==13)) or ((x==2 or x==12) and (y==2 or y==12)) or ((x==3  or x==11) and (y==3 or y==11)) or ((x==4 or x==10) and (y==4 or y==10))):
            word_multiplier=2
        if(((x==0 or x==14) and (y==0 or y==7 or y==14)) or (x==7 and (y==0 or y==14))):
            word_multiplier=3

        if(((x==5 or x==9) and (y==1 or y==5 or y==9 or y==13)) or ((x==1 or x==13) and (y==5 or y==9))):
            letter_multiplier=3
        if(((x==0 or x==7 or x==14) and (y==3 or y==11)) or ((x==3 or x==11) and (y==0 or y==7 or y==14))
            or((x==2 or x==6 or x==8 or x==12) and (y==6 or y==8)) or((y==2 or y==6 or y==8 or y==12) and (x==6 or x==8))):
            letter_multiplier=2
        if(x==7 and y==7):
            letter_multiplier=1
            word_multiplier=1

        return letter_multiplier*letter_value, word_multiplier

    def get_char_value(self,char):
        #PL
        # if(char=='a' or char=='e' or char=='i' or char=='n' or char=='o' or char=='r' or char=='s' or char=='w' or char=='z'):
        #     return 1
        # if(char=='c' or char=='d' or char=='k' or char=='l' or char=='m' or char=='p' or char=='t' or char=='y'):
        #     return 2
        # if(char=='b' or char=='g' or char=='h' or char=='j' or char=='ł' or char=='u'):
        #     return 3
        # if(char=='ą' or char=='ę' or char=='f' or char=='ó' or char=='ś' or char=='ż'):
        #     return 5
        # if(char=='ć'):
        #     return 6
        # if(char=='ń'):
        #     return 7
        # if(char=='ź'):
        #     return 9
        #ENG
        if(char=='a' or char=='e' or char=='i' or char=='n' or char=='o' or char=='r' or char=='s' or char=='t' or char=='u' or char=='l'):
            return 1
        if(char=='g' or char=='d'):
            return 2
        if(char=='b' or char=='c' or char=='m' or char=='p'):
            return 3
        if(char=='h' or char=='v' or char=='w' or char=='y' or char=='f'):
            return 4
        if(char=='k'):
            return 5
        if(char=='j' or char=='x'):
            return 8
        if(char=='q' or char=='z'):
            return 10
        return 1


    def transpose_board(self,board):
        transposed_board =[]

        for x in range(15):
            new_line=[]
            for y in range(15):
                new_line.append(board[y][14-x])
            transposed_board.append(new_line)
        return transposed_board    

    def get_right_angle_patterns(self,board, node_orient):
        pattern_board=[]
        for x in range(15):
            for y in range(15):
                if(board[x][y]!=''):
                    left=False
                    right=False
                    empty_left_side=0
                    empty_right_side=0
                    check=False
                    if(y+1>14):
                        check=True
                    elif(board[x][y+1]==''):
                        check=True
                    if((board[x][y-1]=='' or y==0)and check):
                        left = self.check_whether_left_is_possible(x,y,board)
                        right = self.check_whether_right_is_possible(x,y,board)
                        
                        if(left==True):
                            empty_left_side=1
                        if(right==True):
                            empty_right_side=1

                        if(empty_left_side!=1 and empty_right_side!=1):
                            continue

                        if(empty_left_side==1):
                            empty_left_side = self.get_empty_fields_on_the_left(x,y,board)

                        if(empty_right_side==1):
                            empty_right_side = self.get_empty_fields_on_the_right(x,y,board)

                        help_index_right = empty_right_side
                        help_index_left = empty_left_side
                        #maksymalnie 7 liter mozna wlozyc nawet jesli bedzie wiecej miejsca
                        if(empty_right_side>7):
                            help_index_right=7
                        if(empty_left_side>7):
                            help_index_left=7
                        
                        patterns = self.make_patterns(help_index_left, help_index_right, node_orient, board, x,y)
                        for pattern in patterns:
                            pattern_board.append(pattern)

        return pattern_board

    def check_whether_left_is_possible(self, x, y, board):
        if(x!=14 and x!=0):
            if(board[x-1][y-1]=='' and board[x+1][y-1]==''):
                if(board[x][y-2]=='' or y-1==0):
                    return True
        elif(x==14):
            if(y-1>=0):
                if(board[x-1][y-1]==''):
                    if(board[x][y-2]=='' or y-1==0):
                        return True
        elif(x==0):
            if(board[x+1][y-1]==''):
                if(board[x][y-2]=='' or y-1==0):
                    return True
        return False

    def check_whether_right_is_possible(self,x,y,board):
        if(x!=14 and x!=0 and y!=14):
            if(board[x-1][y+1]=='' and board[x+1][y+1]==''):
                if(y+1==14):
                    return True
                elif(board[x][y+2]==''):
                    return True
        elif(x==14):
            if(y<14):
                if(board[x-1][y+1]==''):
                    if(y+1==14):
                        return True
                    elif(board[x][y+2]==''):
                        return True
        elif(x==0 and y!=14):
            if(board[x+1][y+1]==''):
                if(y+1==14):
                    return True
                elif(board[x][y+2]==''):
                    return True
        return False

    def get_empty_fields_on_the_left(self,x,y,board):
        left=True
        index_left=1
        while(left==True and y-index_left!=0):
            down_empty=False
            if(x==14):
                down_empty = True
            elif(board[x+1][y-1-index_left]==''):
                down_empty = True

            up_empty=False
            if(x==0):
                up_empty=True
            elif(board[x-1][y-1-index_left]==''):
                up_empty=True

            if(up_empty and down_empty):
                #czy doszlo sie do poczatku planszy
                if(y-1-index_left==0):
                    index_left=index_left+1
                elif(board[x][y-2-index_left]==''):
                    index_left=index_left+1
                else:
                    left=False
            else:
                left=False
        return index_left

    def get_empty_fields_on_the_right(self,x,y,board):
        index_right=1
        right=True
        while(right==True and y+index_right!=14):
            state=False
            if(x==14):
                state = True
            elif(y+index_right==14):
                state=True
            elif(board[x+1][y+1+index_right]==''):
                state = True
            state2=False
            if(x==0):
                state2=True
            elif(board[x-1][y+1+index_right]==''):
                state2=True
            if(state2 and state):
                if(y+1+index_right==14):
                    index_right=index_right+1
                elif(board[x][y+2+index_right]==''):
                    index_right=index_right+1
                else:
                    right=False
            else:
                right=False
        return index_right

    def make_patterns(self, empty_left, empty_right, node_orient, board, x,y):
        pattern_board=[]
        for i in range (empty_left+1):
            right_shift=empty_right
            if(i==0 and empty_right==0):
                continue
            if(node_orient=='h'):
                coord_x=x
                coord_y=y
            elif(node_orient=='v'):
                coord_x=y
                coord_y=14-x

            if(i+empty_right>7):
                right_shift = right_shift-(i+empty_right-7)

            if(right_shift<0):
                right_shift=0
            if(y==0):
                pattern = (board[x][y].lower(),coord_x,coord_y,0,right_shift,node_orient)
            else:
                pattern = (board[x][y].lower(),coord_x,coord_y,i,right_shift,node_orient)
            pattern_board.append(pattern)
        return pattern_board

    def get_bridge_patterns(self,pattern_board):
        bridge_patterns=[]
        for pattern in pattern_board:
            char = pattern[0]

            for sub_pattern in pattern_board:
                row=pattern[1]
                col=pattern[2]
                sub_row=sub_pattern[1]
                sub_col=sub_pattern[2]
                if(sub_row>row+1 and sub_col==col and sub_pattern[5]=='v' and ((sub_pattern[3]+pattern[4]>=sub_row-row-1)or(sub_row==row+2))):
                    cont=True
                    if(sub_row==row+2):
                        if(self.board[row+1][col-1]!=''):
                            cont=False
                        elif(col+1<15):
                            if(self.board[row+1][col+1]!=''):
                                cont=False   
                    for i in range(sub_row-row-1):
                        if(self.board[row+1+i][col]!=''):
                            cont=False
                    if(cont==False):
                        continue
                    difference = sub_row-row
                    if(pattern[3]<=7-(difference-1)):
                        left_shift=pattern[3]
                        right_shift=7-(difference-1)-left_shift
                        if(right_shift>sub_pattern[4]):
                            right_shift=sub_pattern[4]   
                        bridge_pattern=(char+sub_pattern[0],row,col,left_shift,right_shift,'v',difference)
                        bridge_patterns.append(bridge_pattern)

                if(sub_col>col+1 and sub_row==row and sub_pattern[5]=='h' and ((sub_pattern[3]+pattern[4]>=sub_col-col-1) or(sub_col==col+2))):
                    cont=True
                    if(sub_col==col+2):
                        if(self.board[row-1][col+1]!=''):
                            cont=False
                        elif(row+1<15):
                            if(self.board[row+1][col+1]!=''):
                                cont=False                           
                    for i in range(sub_col-col-1):
                        if(self.board[row][col+1+i]!=''):
                            cont=False
                    if(cont==False):
                        continue
                    difference = sub_col-col
                    if(pattern[3]<=7-(difference-1)):
                        left_shift=pattern[3]
                        right_shift=7-(difference-1)-left_shift
                        if(right_shift>sub_pattern[4]):
                            right_shift=sub_pattern[4]   
                        bridge_pattern=(char+sub_pattern[0],row,col,left_shift,right_shift,'h',difference)
                        bridge_patterns.append(bridge_pattern)

        return list(set(bridge_patterns))


    def get_letters_for_anagram(self):
        board_letters=''
        bridges={}
        for pattern in self.pattern_board:
            if(len(pattern[0])==2):
                bridges[pattern[0]]=pattern[6]
            elif(len(pattern[0])==1):
                board_letters=board_letters+pattern[0]

        letters = "".join(set(board_letters)) 
        for key in bridges:
            position1 = letters.find(key[0])
            position2 = letters.find(key[1])
            if(position1==-1 and position2==-1):
                letters.join(key[0])
                letters.join(key[1])
            elif(position1==-1):
                letters.join(key[0])
            elif(position2==-1):
                letters.join(key[1])
        return letters, bridges
        
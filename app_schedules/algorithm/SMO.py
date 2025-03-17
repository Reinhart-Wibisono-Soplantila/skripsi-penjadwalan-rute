from django.contrib.staticfiles import finders
class SpiderMonkeyAlgorithm:
    def __init__(self):
        try:
            import pandas as pd
            import numpy as np
            import math
            import random
            import copy
            import time
            
            self.np = np
            self.pd = pd
            self.time = time
            self.random = random
            self.copy = copy
            
            # file_path = finders.find('files/DistanceMatriks.xlsx')
            file_path = finders.find('files/distanceMatrix_Saturday.xlsx')
            self.distance_df = pd.read_excel(file_path, engine='openpyxl', index_col=0)
            self.start = time.time()
        except ImportError:
            print("Libary belum terimpor")

    # pd.set_option('display.max_rows', None)
    # pd.set_option('display.max_columns', None)
    def main(self, outlets):
        run = 1
        max_runs = 1
        TARGET=100000000000
        TARGET_Counter = 0
        Repeat = True
        try:
            while(run <= max_runs):
                SM = []                                                                     # The list that stores all the spider monkeys
                nSM = 100                                                                  # Number of spider monkeys
                number_of_groups = 1                                                        # Current Number of groups
                MG = 10                                                                     # Maximum number of groups
                pr = 0.2                                                                    # Perturbation rate
                LLL = 10                                                                 # Local Leader Limit
                GLL = 10                                                                  # Global Leader Limit
                LLLc = {0:0}                                                                 # Local Leader Limit Count
                GLLc = 0                                                                    # Global Leader Limit Count
                LL = []                                                                     # List that stores the local leaders of all groups
                GL = [0,0]                                                                  # List that stores the group number and index of global leader
                
                def generate_TSP_tours(n, outlets): # where n is the number of spider monkeys             #generates TSP tours
                    temp = []
                    for i in range(n):
                        l = self.random.sample(outlets,len(outlets))
                        temp.append(l)
                    SM.append(temp)

                generate_TSP_tours(nSM, outlets)
                def fitness(sm):
                    fit = 0
                    for j in range(len(sm)-1):
                        if j == 0:
                            loc_source = '15000000000000000000000000'
                            loc_1 = sm[j]
                            loc_2 = sm[j+1]
                            fit += self.distance_df[loc_source][loc_1]
                            fit += self.distance_df[loc_1][loc_2]
                        else:
                            loc_1 = sm[j]
                            loc_2 = sm[j+1]
                            fit += self.distance_df[loc_1][loc_2]
                    return fit
        
                def SS(T2,T1):                                                      #returns Swap sequence list with its element in a tuple e.g [(1,3),(3,4),...]
                    swap_operator_list = []

                    for i in range(len(T1)-1):
                        if T1[i] != T2[i]:

                            first = T1[i]
                            second = T2[i]

                            v = T1.index(second)

                            # T1[i] = second
                            # T1[v] = first

                            t = (i+1,v+1)

                            swap_operator_list.append(t)
                    return swap_operator_list

                def SS_merge(ss1,ss2):                                              #performs ⊗ merging operation and returns list of SS
                    for i in ss2:
                        if i not in ss1:
                            ss1.append(i)
                    return ss1

                def Cal_BasicSS(SS):                                                #performs Equation 7 operation and returns Basic SS list
                    size = len(SS)
                    i = 0

                    while(i!=size):
                        if (SS[i][1],SS[i][0]) in SS[i:]:
                            SS.remove((SS[i][1],SS[i][0]))
                            SS.remove(SS[i])
                            size-=2
                        else:
                            i+=1
                    return SS

                def apply_BSS(sm,BSS):                                              #Performs Equation 8 and returns updated SM

                    for i in BSS:
                        a = i[0]-1
                        b = i[1]-1
                        copy_sm = self.copy.deepcopy(sm)
                        copy_sm[b],copy_sm[a] = copy_sm[a],copy_sm[b]
                        if fitness(copy_sm) < fitness(sm):
                            sm[b],sm[a] = sm[a],sm[b]
                    return sm

                def random_subsequence(ss):
                    temp = []
                    for i in ss:
                        u = self.random.randint(0,1)
                        if u == 1:
                            temp.append(i)
                    return temp
                
                LL = []
                for k in range(len(SM)):            #mencari nilai terbaik sebagai GL dan LL pada pencarian pertama kali
                    LLLc[k] = 0
                    max_fit = 1000000000
                    max_fit_index = 0
                    for i in range(len(SM[k])):
                        if fitness(SM[k][i]) < max_fit:
                            max_fit = fitness(SM[k][i])
                            max_fit_index = i
                            print(f'max_fit ={max_fit}')
                            print(f'max_fit_index ={max_fit_index } ')
                    LL.append(max_fit_index)
                GL[1] = LL[0]

                print(f'LL[0] = {LL[0]}')
                print(f'GL[1] = {GL[1]}')
                print(SM[GL[0]][GL[1]])
                while Repeat <= True:
                    print('*'*20)
                    """
                    Algorithm 2.1 Starts
                    """
                    print(f"best LL = {LL}")
                    for k in range(len(SM)):  # len SM = 1
                        print(f"k={k}")
                        print(f'SM = {len(SM)}')
                        print(f'SMk= {len(SM[k])}')
                        print(f'LLk = {len([LL[k]])}')
                        print(f'SMKLLk = {len(SM[k][LL[k]])}')
                        for i in range(len(SM[k])):    # len SM[k][i] = 100 (i = 0, 1, 2, 3, ...)
                            u = self.random.uniform(0,1)
                            if u >= pr:
                                copy_smi = self.copy.deepcopy(SM[k][i])   # copy urutan lokasi yang ada
                                ss1 = SS(SM[k][LL[k]], SM[k][i])   # hitung swap sequence LL terhadap SM
                                u_ss1 = random_subsequence(ss1)    # setiap ss yang ditemukan dikalikan 1 (jika dapat angka  secara random dari 0 dan 1)
                                
                                rnd = self.random.randint(0, len(SM[k])-1)    # hitung swap sequence  rnd terhadap  SM
                                ss2 = SS(SM[k][rnd], SM[k][i])
                                u_ss2 = random_subsequence(ss2)
                                
                                ssi = SS_merge(u_ss1, u_ss2)                # gabungkan ss atau SO dari ss1 dan ss2
                                bss_i = Cal_BasicSS(ssi)              # kalau misal ada SO yang ternyata kebalikan dari SO lain, (2,1) merupakan kebalikan dari (1,2) pada indeks 0 maka (2,1) dihapus
                                sm_new = apply_BSS(copy_smi, bss_i) #ganti copy SM[k][i] dengan SO yang jadi]
                                if fitness(sm_new) < fitness(SM[k][i]):
                                    SM[k][i] = self.copy.deepcopy(sm_new)

                    for k in range(len(SM)):
                        for i in range(len(SM[k])):
                            prob = 0.9 * (fitness(SM[GL[0]][GL[1]])/fitness(SM[k][i])) + 0.1
                            u = self.random.uniform(0,1)
                            # print(f"{i}, prob = {prob}, u={u}")

                            if u <= prob:
                                # print(f'ok, {i}')
                                copy_smi = self.copy.deepcopy(SM[k][i])
                                ss1 = SS(SM[GL[0]][GL[1]], SM[k][i])
                                u_ss1 = random_subsequence(ss1)
                                rnd = self.random.randint(0, len(SM[k])-1)
                                ss2 = SS(SM[k][rnd], SM[k][i])
                                u_ss2 = random_subsequence(ss2)
                                ssi = SS_merge(u_ss1, u_ss2)
                                bss_i = Cal_BasicSS(ssi)
                                sm_new = apply_BSS(copy_smi, bss_i)
                                if fitness(sm_new) < fitness(SM[k][i]):
                                    
                                    SM[k][i] = self.copy.deepcopy(sm_new)

                    """
                    Algorithm 2.2 Starts
                    """
                    best_LL_group = GL[0]
                    best_LL_index = GL[1]
                    best_LL_fitness = fitness(SM[GL[0]][GL[1]])
                    print(f"best LL = {LL}")
                    print(f"best LL fitness = {best_LL_fitness}")
                    for k in range(len(SM)):
                        LLk_fitness = fitness(SM[k][LL[k]])
                        current_LL_maximum = LLk_fitness
                        new_LL_index = LL[k]
                        old_LL_index = LL[k]
                        for i in range(len(SM[k])):
                            fit = fitness(SM[k][i])
                            if fit < current_LL_maximum:
                                current_LL_maximum = fit
                                new_LL_index = i
                                # print(f"new Local Leader, i-{i} = {fit}-{current_LL_maximum}, group- {k}, idx-{new_LL_index}")
                            # else:
                                # print(f"same Local Leader, i-{i} = {fit}-{current_LL_maximum}, group- {k}, idx-{new_LL_index}")
                        
                        print(f"Before Checking : LLLc[k] = {LLLc[k]}")
                        
                        print(f"After Checking : LLLc[k] = {LLLc[k]}")
                        if new_LL_index == old_LL_index:
                            LLLc[k] += 1
                            print(f"LLLc[k] = {LLLc[k]}")
                        else:
                            LLLc[k] = 0
                            LL[k] = new_LL_index
                            LLk_fitness = current_LL_maximum
                            print(f"LLLc[k] = {LLLc[k]}")

                        if LLk_fitness < best_LL_fitness:
                            best_LL_group = k
                            best_LL_index = LL[k]
                            best_LL_fitness = LLk_fitness

                            print(f"best LL = {best_LL_index}")
                            print(f"best_LL_fitness = {best_LL_fitness}")

                    if best_LL_group != GL[0] or best_LL_index != GL[1]:
                            GL[0] = best_LL_group
                            GL[1] = best_LL_index
                            print(f"Best Group = {GL[0]}")
                            print(f"Best SM in Group (GL) = {GL[1]}")
                            
                            print(f"Best Fitness in Group (GL) = {fitness(SM[GL[0]][GL[1]])}")
                            # print(f"SM[GL[0]][GL[1]] = {SM[GL[0]][GL[1]]}")
                        
                            print(f"GLLc - atas = {GLLc}")
                            print()
                            GLLc = 0
                    else:
                        print(f"Best Group = {GL[0]}")
                        print(f"Best SM in Group (GL) = {GL[1]}")
                        
                        # print(f"SM[GL[0]][GL[1]] = {SM[GL[0]][GL[1]]}")
                        print(f"GLLc - tengah = {GLLc}")
                        GLLc += 1

                    """
                    Algorithm 2.3 Starts
                    """

                    # if LLC reach LLL
                    #   print(f'number_of_groups = {number_of_groups}')
                    for k in range(len(SM)):
                        #   print(f"LLLc = {LLLc}")
                        if LLLc[k] > LLL:

                            print('LLLc - '*5)
                            LLLc[k] = 0
                            #   print('LLL reach LLC')
                            for i in range(len(SM[k])):
                                u = self.random.uniform(0,1)
                                if u >= pr:
                                    l = self.random.sample(outlets,len(outlets))
                                    print(f'k={k}, i={i}, u={u}, l={l}')
                                    SM[k][i] = l
                                else:
                                    copy_smi = self.copy.deepcopy(SM[k][i])
                                    # print(f"copy_smi {copy_smi}")
                                    ss1 = SS(SM[k][LL[k]], SM[k][i])
                                    u_ss1 = random_subsequence(ss1)

                                    ss2 = SS(SM[GL[0]][GL[1]], SM[k][i])
                                    u_ss2 = random_subsequence(ss2)

                                    sm_new = apply_BSS(copy_smi, u_ss2)
                                    sm_new2 = apply_BSS(sm_new, u_ss1)
                                    
                                    SM[k][i] = sm_new2
                                    print(f"SM[k][i] = {SM[k][i]}")


                    print(f"GLLc - bawah = {GLLc}")
                    print(f"number_of_groups = {number_of_groups}")
                    if GLLc > GLL:
                        print('GLLc - '*5)
                        GLLc = 0

                        if number_of_groups  < MG:
                            lis = []
                            for k in range(len(SM)):
                                for i in range(len(SM[k])):
                                    lis.append(SM[k][i])
                            number_of_groups += 1
                            SM = []
                            k = 0
                            x = nSM//number_of_groups
                            temp = []
                            for i in range(nSM):
                                if (i % x== 0) and (k != number_of_groups - 1) and (i != 0):
                                    SM.append(temp)
                                    temp = []
                                    k += 1
                                temp.append(lis[i])
                            SM.append(temp)

                        else:
                            lis = []
                            for k in range(len(SM)):
                                for i in range(len(SM[k])):
                                    lis.append(SM[k][i])
                            SM = []
                            SM.append(lis)
                            number_of_groups = 1

                        LL = []
                        LLLc = {}
                        for k in range(len(SM)):
                            LLLc[k] = 0
                            max_fit = 10000000000000
                            max_fit_index = 0
                            print('**********')
                            print(f'max_fit_index = {max_fit_index}')
                            print(f'max_fit = {max_fit}')
                            print('####################')
                            print(f"k={k}")
                            print(len(SM))
                            print(len(SM[k]))
                            print('########################')
                            
                            for i in range(len(SM[k])):
                                if fitness(SM[k][i]) < max_fit:
                                    print()
                                    print('making new LL')
                                    max_fit = fitness(SM[k][i])
                                    max_fit_index = i
                                    print(f'max_fit_index = {max_fit_index}')
                                    print(f'max_fit = {max_fit}')
                            LL.append(max_fit_index)
                        print(LL)
                        #   print('LLLc')
                        print(f"LLLc = {LLLc}")
                        print()
                        GL = [0,0]
                        for k in range(len(SM)):
                            if fitness(SM[k][LL[k]]) < fitness(SM[GL[0]][GL[1]]):
                                GL[0] = k
                                GL[1] = LL[k]
                    print('*'*20)
                    print('')
                    
                    print(SM[GL[0]][GL[1]])
                    
                    print(f"Algo 2.3 LL = {LL}")
                    if TARGET_Counter > 5:
                        answer_index = GL[1]
                        answer_location = SM[GL[0]][GL[1]]
                        answer_fitness = fitness(answer_location)
                        
                        print(answer_index)
                        # print(answer_location)
                        print(answer_fitness)
                        Repeat = False
                        break
                    else:
                        if TARGET <= fitness(SM[GL[0]][GL[1]]):
                            TARGET_Counter +=1
                            print('TARGET_Counter', TARGET_Counter)
                        else:
                            print("TARGET SEBELUMNYA",TARGET)
                            TARGET = fitness(SM[GL[0]][GL[1]])
                            print('TARGET SEKARANG',TARGET)
                            TARGET_Counter = 0
                        
                        end = self.time.time()
                        execution_time = end-self.start    
                        count = 5

                run += 1
                print(f"Best Group = {GL[0]}")
                print(f"Best SM in Group (GL) = {GL[1]}")
                print(f'lokasi: ', answer_location)
                print(f'Fitness', answer_fitness)
            # print(SM[GL[0]][GL[1]])    
        except ImportError:
            print("ERROR!!!")
        return answer_location, answer_fitness

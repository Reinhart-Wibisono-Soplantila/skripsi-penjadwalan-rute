from django.contrib.staticfiles import finders
class GeneticAlgorithm:
    def __init__(self):
        try:    
            import pandas as pd
            import numpy as np
            import math
            import random
            import string
            import copy
            # import matplotlib.pyplot as plt
            import json
            import time
            self.np = np
            self.pd = pd
            self.random = random
            self.copy = copy
            self.time = time

            file_path = finders.find('files/distanceMatrix_Saturday.xlsx')
            self.distance_df = pd.read_excel(file_path, engine='openpyxl', index_col=0)
            self.start = time.time()
            print("library sudah terimpor")
        except ImportError:
            print("Libary belum terimpor")

    def calcDistance(self, items):
        fit = 0
        for j in range(len(items)-1):
            if j == 0:
                loc_source = '15000000000000000000000000'
                loc_1 = items[j]
                loc_2 = items[j+1]
                fit += self.distance_df[loc_source][loc_1]
                fit += self.distance_df[loc_1][loc_2]
            else:
                loc_1 = items[j]
                loc_2 = items[j+1]
                fit += self.distance_df[loc_1][loc_2]
        return fit

    # selecting the population
    def selectPopulation(self, outlets, size):
        population = []
        for i in range(size):
            c = outlets.copy()
            self.random.shuffle(c)
            distance = self.calcDistance(c)
            population.append([distance, c])
        # print(population)
        fitest = sorted(population)[0]

        return population, fitest


    # the genetic algorithm
    def geneticAlgorithm(
        self,
        population,
        lenCities,
        TOURNAMENT_SELECTION_SIZE,
        MUTATION_RATE,
        CROSSOVER_RATE,
        TARGET
    ):
        # max_gen = 200
        stop_iteration = False
        targetCounter = 0
        gen_number = 0
        bestAnswer=0
        is_best = False
        while(stop_iteration == False):
            new_population = []
            temp_population = []
            print('gen number:', gen_number)
            # selecting two of the best options we have (elitism)
            firstElitism = sorted(population, key=lambda x: x[0])[0]
            firstElitism = self.copy.deepcopy(firstElitism)
            distFirstElitism = self.calcDistance(firstElitism[1])
            
            secondElitism = sorted(population, key=lambda x: x[0])[1]
            secondElitism  =self.copy.deepcopy(secondElitism)
            distSecondElitism = self.calcDistance(secondElitism[1])
            
            print(f"ELITISIM1 = {firstElitism[0]} -- {distFirstElitism}")
            print(f"ELITISIM2 = {secondElitism[0]} -- {distSecondElitism}")
            
            new_population.append([distFirstElitism, firstElitism[1]])
            new_population.append([distSecondElitism, secondElitism[1]])
           
            print('')
            print(f'new_population[0] : {self.calcDistance(new_population[0][1])}')
            print(f'new_population[1] : {self.calcDistance(new_population[1][1])}')
            print('')
            print('NEW POPULATION')
            for k in range(int((len(population) - 2) / 2)):
                # CROSSOVER
                random_number = self.random.random()
                if random_number <= CROSSOVER_RATE:
                    # print('cross')
                    parent_chromosome1 = sorted(
                        self.random.choices(population, k=TOURNAMENT_SELECTION_SIZE), key=lambda x: x[0]
                    )[0]
                    parent_chromosome1 = self.copy.deepcopy(parent_chromosome1)
                    parent_chromosome2 = sorted(
                        self.random.choices(population, k=TOURNAMENT_SELECTION_SIZE), key=lambda x: x[0]
                    )[0]
                    
                    parent_chromosome2 = self.copy.deepcopy(parent_chromosome2)
                    point = self.random.randint(0, lenCities - 1)

                    child_chromosome1 = parent_chromosome1[1][0:point]
                    for j in parent_chromosome2[1]:
                        if (j in child_chromosome1) == False:
                            child_chromosome1.append(j)
                    
                    child_chromosome2 = parent_chromosome2[1][0:point]
                    for j in parent_chromosome1[1]:
                        if (j in child_chromosome2) == False:
                            child_chromosome2.append(j)
                # If crossover not happen
                else:
                    child_chromosome1 = self.random.choices(population)[0][1]
                    child_chromosome2 = self.random.choices(population)[0][1]
                    
                child_chromosome1 = self.copy.deepcopy(child_chromosome1)
                child_chromosome2 = self.copy.deepcopy(child_chromosome2)
                
                # MUTATION
                if self.random.random() >= MUTATION_RATE:
                    point1 = self.random.randint(0, lenCities - 1)
                    point2 = self.random.randint(0, lenCities - 1)
                    child_chromosome1[point1], child_chromosome1[point2] = (
                        child_chromosome1[point2],
                        child_chromosome1[point1],
                    )

                    point1 = self.random.randint(0, lenCities - 1)
                    point2 = self.random.randint(0, lenCities - 1)
                    child_chromosome2[point1], child_chromosome2[point2] = (
                        child_chromosome2[point2],
                        child_chromosome2[point1],
                    )
                temp_population.append([self.calcDistance(child_chromosome1), child_chromosome1])
                temp_population.append([self.calcDistance(child_chromosome2), child_chromosome2])
                for i in range(len(temp_population)):
                    cekl = self.calcDistance(temp_population[i][1])
                    orrri = temp_population[i][0]
                    if cekl != orrri:
                        print(f"{k}=={cekl} -- {orrri} -- TIDAK SAMA")
            # print(len(new_population))
            for item in range(len(temp_population)):
                new_population.append(temp_population[item])
            # print(len(new_population))
            # print('')
            # print('NEW POPULATION')
            # for i in range(len(new_population)):
            #     cek= self.calcDistance(new_population[i][1])
            #     ori = new_population[i][0]
            #     if ori != cek:
            #         print(f"{i} == {ori} -- {cek}")
            #         print("TIDAK SAMAAAA")
            population = new_population
            gen_number += 1
            # print('')
            # print('POPULATION')
            # for i in range(len(population)):
            #     cek= self.calcDistance(population[i][1])
            #     ori = population[i][0]
            #     if ori != cek:
            #         print(f"{i} == {ori} -- {cek}")
            #         print("TIDAK SAMAAAA")
            # print('')
            # print('')
            # print('after len(population): ', len(population))
            population = sorted(population, key=lambda x: x[0])
            tempBestanswer = population[0]
            # print(f" temp = ", tempBestanswer)
            # tempBestanswer = sortedlist[0]
            
            if targetCounter == 10:
                stop_iteration == True
                if is_best == True:
                    print('It was Stoped')
                    
                    print('jarak', self.calcDistance(bestAnswer[1]))
                    print('best: ', bestAnswer)
                break
            else:
                if tempBestanswer[0] < TARGET:
                    print('Change Best ANswer')
                    TARGET = tempBestanswer[0]
                    bestAnswer = tempBestanswer
                    print('HITUNG:', self.calcDistance(bestAnswer[1]))
                    print('bestAnswer:', bestAnswer[0])
                    is_best=True
                    targetCounter=0
                else:
                    print('')
                    print('TARGETCOUNTERRR')
                    for i in range(len(population)):
                        cek= self.calcDistance(population[i][1])
                        ori = population[i][0]
                        if ori != cek:
                            print(f"{i} == {ori} -- {cek} -- TIDAK SAMA")
                        else:
                            print(f"{i} == {ori} -- {cek}")
                    print('')
                    print('best Answer still')
                    targetCounter+=1
                    print('targetCounter: ', targetCounter)
        answer = bestAnswer
        return answer, gen_number, is_best 

    def main(self, outlets):
        count=1
        while count <=1:
            # initial values
            POPULATION_SIZE =100
            TOURNAMENT_SELECTION_SIZE = 4
            MUTATION_RATE = 0.8
            CROSSOVER_RATE = 0.8

            firstPopulation, firstFitest = self.selectPopulation(outlets, POPULATION_SIZE)
            # print('len:  ',firstPopulation[0][1])
            TARGET = firstFitest[0]# tessspopulation = copy.deepcopy(firstPopulation)
            print('Target = ', TARGET)
            answer, genNumber, is_best = self.geneticAlgorithm(
                firstPopulation,
                len(outlets),
                TOURNAMENT_SELECTION_SIZE,
                MUTATION_RATE,
                CROSSOVER_RATE,
                TARGET,
            )
            if(is_best == False):
                answer = firstFitest
                print('best answer still the fisrt fittest')
                print(answer[0])
            print("\n----------------------------------------------------------------")
            # print('Count:' + str(count))
            # print("Generation: " + str(genNumber))
            # print("Population : " + str(POPULATION_SIZE))
            # print("Fittest chromosome distance before training: " + str(firstFitest[0]))
            # print("Fittest chromosome distance after training: " + str(answer[0]))
            # print("The location: " + str(answer[1]))
            # print("Target distance: " + str(TARGET))
            print("----------------------------------------------------------------\n")
            # valll = self.calcDistance1(answer[1])
                
            end = self.time.time()
            execution_time = end-self.start
            print( 'Time: ',execution_time)
            return  answer, genNumber 
            count +=1

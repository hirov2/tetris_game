#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
import pprint
import random
import copy

class Block_Controller(object):

    # init parameter
    board_backboard = 0
    board_data_width = 0
    board_data_height = 0
    board_status = 0
    ShapeNone_index = 0
    CurrentShape_class = 0
    CurrentShape_index = 0
    CurrentDirection = 0
    NextShape_class = 0

    # GetNextMove is main function.
    # input
    #    GameStatus : this data include all field status, 
    #                 in detail see the internal GameStatus data.
    # output
    #    nextMove : this data include next shape position and the other,
    #               if return None, do nothing to nextMove.
    def GetNextMove(self, nextMove, GameStatus):

        t1 = datetime.now()

        # print GameStatus
        print("=================================================>")
#        pprint.pprint(GameStatus, width = 61, compact = True)
#        print("GameStatus[field_info][backboard] =", GameStatus["field_info"]["backboard"])
	
	
	# current board info
        self.board_backboard = GameStatus["field_info"]["backboard"]
        # current Shape info
        CurrentShapeDirectionRange = GameStatus["block_info"]["currentShape"]["direction_range"]
        self.CurrentShape_index = GameStatus["block_info"]["currentShape"]["index"]
        self.CurrentDirection = GameStatus["block_info"]["currentDirection"]
        
        print("Direction = ", self.CurrentDirection)
	
        # search best nextMove -->
        # random sample (Initialize)
        nextMove["strategy"]["direction"] = random.randint(0,3)
        nextMove["strategy"]["x"] = random.randint(0,9)
        nextMove["strategy"]["y_operation"] = 1
        nextMove["strategy"]["y_moveblocknum"] = 0
        
        self.board_status = self.GetBackboardStatus(self.board_backboard)
        pprint.pprint(self.board_status, width = 61, compact = True);
        
        # search with current block Shape
        LatestEvalSpace = 100000
        LatestEvalAverageHeight = 0
        LatestEvalMaxHeight = 0
        LatestEvalMinHeight = 100000
        LatestEvalMaxMinHeight = 100000
        LatestEvalEraceCount = 0
        LatestBackboardStatus = copy.deepcopy(self.board_status)
        for direction0 in CurrentShapeDirectionRange:
            # search with x
            for x0 in range(10):
                BackboardStatus = self.GetSimulationOfBackboardStatus(self.board_status,
                                                                      self.CurrentShape_index,
                                                                      direction0,
                                                                      x0)
                EvalSpace = self.GetNumOfSpace(BackboardStatus)
                EvalEraceCount = self.GetEraceCountInBackboard(BackboardStatus)
                EvalAverageHeight = self.GetYOfAverageBlock(BackboardStatus)
                EvalMaxHeight = self.GetYOfMaxBlock(BackboardStatus)
                EvalMinHeight = self.GetYOfMinBlock(BackboardStatus)
                EvalMaxMinHeight = EvalMinHeight - EvalMaxHeight
                print(EvalSpace, EvalEraceCount, EvalAverageHeight, EvalMaxHeight)

                if( EvalSpace < LatestEvalSpace ):
                    LatestEvalSpace = EvalSpace
                    LatestEvalEraceCount = EvalEraceCount
                    LatestEvalAverageHeight = EvalAverageHeight
                    LatestEvalMaxHeight = EvalMaxHeight
                    LatestEvalMinHeight = EvalMinHeight
                    LatestEvalMaxMinHeight = EvalMaxMinHeight
                    LatestBackboardStatus = copy.deepcopy(BackboardStatus)
                    nextMove["strategy"]["direction"] = direction0
                    nextMove["strategy"]["x"] = x0
                elif( EvalSpace == LatestEvalSpace ):
                    if( EvalEraceCount > 2 ):
                        LatestEvalSpace = EvalSpace
                        LatestEvalEraceCount = EvalEraceCount
                        LatestEvalAverageHeight = EvalAverageHeight
                        LatestEvalMaxHeight = EvalMaxHeight
                        LatestEvalMinHeight = EvalMinHeight
                        LatestEvalMaxMinHeight = EvalMaxMinHeight
                        LatestBackboardStatus = copy.deepcopy(BackboardStatus)
                        nextMove["strategy"]["direction"] = direction0
                        nextMove["strategy"]["x"] = x0
                    elif( EvalMaxMinHeight < LatestEvalMaxMinHeight ):
                        LatestEvalSpace = EvalSpace
                        LatestEvalEraceCount = EvalEraceCount
                        LatestEvalAverageHeight = EvalAverageHeight
                        LatestEvalMaxHeight = EvalMaxHeight
                        LatestEvalMinHeight = EvalMinHeight
                        LatestEvalMaxMinHeight = EvalMaxMinHeight
                        LatestBackboardStatus = copy.deepcopy(BackboardStatus)
                        nextMove["strategy"]["direction"] = direction0
                        nextMove["strategy"]["x"] = x0
                    elif( EvalMaxHeight > LatestEvalMaxHeight ):
                        LatestEvalSpace = EvalSpace
                        LatestEvalEraceCount = EvalEraceCount
                        LatestEvalAverageHeight = EvalAverageHeight
                        LatestEvalMaxHeight = EvalMaxHeight
                        LatestEvalMinHeight = EvalMinHeight
                        LatestEvalMaxMinHeight = EvalMaxMinHeight
                        LatestBackboardStatus = copy.deepcopy(BackboardStatus)
                        nextMove["strategy"]["direction"] = direction0
                        nextMove["strategy"]["x"] = x0
                    elif( EvalAverageHeight > LatestEvalAverageHeight ):
                        LatestEvalSpace = EvalSpace
                        LatestEvalEraceCount = EvalEraceCount
                        LatestEvalAverageHeight = EvalAverageHeight
                        LatestEvalMaxHeight = EvalMaxHeight
                        LatestEvalMinHeight = EvalMinHeight
                        LatestEvalMaxMinHeight = EvalMaxMinHeight
                        LatestBackboardStatus = copy.deepcopy(BackboardStatus)
                        nextMove["strategy"]["direction"] = direction0
                        nextMove["strategy"]["x"] = x0                    
        
        print(self.CurrentShape_index, LatestEvalSpace, LatestEvalEraceCount, LatestEvalAverageHeight, LatestEvalMaxHeight)
        pprint.pprint(LatestBackboardStatus, width = 61, compact = True)
        print(nextMove)

        
        
        # search best nextMove <--

        # return nextMove
        print("===", datetime.now() - t1)
        print(nextMove)
        return nextMove

    def GetBackboardStatus(self, board_backboard):
        #
        # get Backboard Status by 0/1.
        # in two-dimensional array
        #

        BackboardStatus = self.convert_1d_to_2d(board_backboard, 10)
        
        for y in range(22):
            for x in range(10):
                if BackboardStatus[y][x] > 0:
                    BackboardStatus[y][x] = 1;
        
        return BackboardStatus

    def convert_1d_to_2d(self, l, cols):
        return [l[i:i + cols] for i in range(0, len(l), cols)]

    def GetNumOfSpace(self, board_status):
        # 
        # Get Space Num. 
        # Count Space Under First Block.
        #
        
        count = 0
        for x in range(10):
            first_block = 0
            for y in range(22):
                if board_status[y][x] == 0 and first_block == 1:
                    count = count + 1
                elif board_status[y][x] > 0 and first_block == 0:
                    first_block = 1
        return count

    def AddBlock(self, board_status, x, y, index):
    
        BackboardStatus = board_status
        if BackboardStatus[y][x] == 0:
            BackboardStatus[y][x] = index
        elif BackboardStatus[y][x] > 0:
            print("ERR:AddBlock", x, y)
            pprint.pprint(BackboardStatus, width = 61, compact = True);
        
        return BackboardStatus

    def GetYOfTopBlock(self, board_status, x):
        # 指定X座標の中で最も高いY座標を返す
        return_y = 22
        for y in range(22):
            if board_status[y][x] > 0:
                return_y = y
                break
        return return_y

    def GetYOfAverageBlock(self, board_status):
        average = 0;
        for x in range(10):
            average = average + self.GetYOfTopBlock(board_status, x)
                
        return average/10

    def GetYOfMaxBlock(self, board_status):
        max_y = 22
        for x in range(10):
            if self.GetYOfTopBlock(board_status, x) < max_y:
                max_y = self.GetYOfTopBlock(board_status, x)

        return max_y

    def GetYOfMinBlock(self, board_status):
        min_y = 0
        for x in range(10):
            if self.GetYOfTopBlock(board_status, x) > min_y:
                min_y = self.GetYOfTopBlock(board_status, x)

        return min_y

    def GetMinYOfBlock(self, y1, y2, y3, y4):
    
        y = y1
        if y > y2:
          y = y2
        if y > y3:
          y = y3
        if y > y4:
          y = y4
    
        return y

    def GetSimulationOfBackboardStatusWithShapeI(self, board_status,
                                                 Shape_direction, Shape_x):
        #
        # Shape I
        #
        #
        BackboardStatus = board_status
        Shape_pattern = 0
        x = Shape_x
        y = 0
        Candidate_y = [0, 0, 0, 0]
        
        Shape_pattern = (self.CurrentDirection + Shape_direction)%2

        if 0 == Shape_pattern:
            y = self.GetYOfTopBlock(board_status, x)
            BackboardStatus = self.AddBlock(BackboardStatus, x, y-4, 8)
            BackboardStatus = self.AddBlock(BackboardStatus, x, y-3, 8)
            BackboardStatus = self.AddBlock(BackboardStatus, x, y-2, 8)
            BackboardStatus = self.AddBlock(BackboardStatus, x, y-1, 8)

        elif 1 == Shape_pattern:
            if x < 2:
                print("ERR:GetSimulationOfBackboardStatusWithShapeI", x)
                x = 2
            elif x > 8:
                print("ERR:GetSimulationOfBackboardStatusWithShapeI", x)
                x = 8
            Candidate_y[0] = self.GetYOfTopBlock(BackboardStatus, x - 2)
            Candidate_y[1] = self.GetYOfTopBlock(BackboardStatus, x - 1)
            Candidate_y[2] = self.GetYOfTopBlock(BackboardStatus, x)
            Candidate_y[3] = self.GetYOfTopBlock(BackboardStatus, x + 1)
            
            y = self.GetMinYOfBlock(Candidate_y[0], Candidate_y[1],
                                    Candidate_y[2], Candidate_y[3])
            
            BackboardStatus = self.AddBlock(BackboardStatus, x-2, y-1, 8)
            BackboardStatus = self.AddBlock(BackboardStatus, x-1, y-1, 8)
            BackboardStatus = self.AddBlock(BackboardStatus, x,   y-1, 8)
            BackboardStatus = self.AddBlock(BackboardStatus, x+1, y-1, 8)
        
        return BackboardStatus
        
    def GetSimulationOfBackboardStatusWithShapeL(self, board_status,
                                                 Shape_direction, Shape_x):
        BackboardStatus = board_status
        Shape_pattern = 0
        x = Shape_x
        y = 0
        Candidate_y = [0, 0, 0]
        
        Shape_pattern = (self.CurrentDirection + Shape_direction)%4
        
        if 0 == Shape_pattern:
            if x > 8:
                print("ERR:GetSimulationOfBackboardStatusWithShapeL", x)
                x = 8
            Candidate_y[0] = self.GetYOfTopBlock(BackboardStatus, x)
            Candidate_y[1] = self.GetYOfTopBlock(BackboardStatus, x + 1)
            
            y = self.GetMinYOfBlock(Candidate_y[0], Candidate_y[1], 22, 22)
            
            BackboardStatus = self.AddBlock(BackboardStatus, x, y-3, 2)
            BackboardStatus = self.AddBlock(BackboardStatus, x, y-2, 2)
            BackboardStatus = self.AddBlock(BackboardStatus, x, y-1, 2)
            BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y-1, 2)
        elif 1 == Shape_pattern:
            if x < 1:
                print("ERR:GetSimulationOfBackboardStatusWithShapeL", x)
                x = 1
            elif x > 8:
                print("ERR:GetSimulationOfBackboardStatusWithShapeL", x)
                x = 8
            Candidate_y[0] = self.GetYOfTopBlock(BackboardStatus, x - 1)
            Candidate_y[1] = self.GetYOfTopBlock(BackboardStatus, x)
            Candidate_y[2] = self.GetYOfTopBlock(BackboardStatus, x + 1)
            
            y = self.GetMinYOfBlock(22, Candidate_y[1], Candidate_y[2], 22)
            
            if Candidate_y[0] < y + 1:
                y = Candidate_y[0]
                BackboardStatus = self.AddBlock(BackboardStatus, x - 1, y - 2, 2)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 2, 2)
                BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 2, 2)
                BackboardStatus = self.AddBlock(BackboardStatus, x - 1, y - 1, 2)
            else:
                BackboardStatus = self.AddBlock(BackboardStatus, x - 1, y - 1, 2)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 1, 2)
                BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 1, 2)
                BackboardStatus = self.AddBlock(BackboardStatus, x - 1, y, 2)
        elif 2 == Shape_pattern:
            if x < 1:
                print("ERR:GetSimulationOfBackboardStatusWithShapeL", x)
                x = 1
            Candidate_y[0] = self.GetYOfTopBlock(BackboardStatus, x - 1)
            Candidate_y[1] = self.GetYOfTopBlock(BackboardStatus, x)
            if Candidate_y[0] < Candidate_y[1] - 2:
                y = Candidate_y[0]
                BackboardStatus = self.AddBlock(BackboardStatus, x - 1, y - 1, 2)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 1, 2)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y,     2)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y + 1, 2)
            else:
                y = Candidate_y[1]
                BackboardStatus = self.AddBlock(BackboardStatus, x - 1, y - 3, 2)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 3, 2)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 2, 2)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 1, 2)
            
        elif 3 == Shape_pattern:
            if x < 1:
                print("ERR:GetSimulationOfBackboardStatusWithShapeL", x)
                x = 1
            elif x > 8:
                print("ERR:GetSimulationOfBackboardStatusWithShapeL", x)
                x = 8
            Candidate_y[0] = self.GetYOfTopBlock(BackboardStatus, x - 1)
            Candidate_y[1] = self.GetYOfTopBlock(BackboardStatus, x)
            Candidate_y[2] = self.GetYOfTopBlock(BackboardStatus, x + 1)
            
            y = self.GetMinYOfBlock(Candidate_y[0], Candidate_y[1], Candidate_y[2], 22)
            
            BackboardStatus = self.AddBlock(BackboardStatus, x - 1, y - 1, 2)
            BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 1, 2)
            BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 1, 2)
            BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 2, 2)
                        
        return BackboardStatus


    def GetSimulationOfBackboardStatusWithShapeJ(self, board_status,
                                                 Shape_direction, Shape_x):
        BackboardStatus = board_status
        Shape_pattern = 0
        x = Shape_x
        y = 0
        Candidate_y = [0, 0, 0]
        
        Shape_pattern = (self.CurrentDirection + Shape_direction)%4
        
        if 0 == Shape_pattern:
            if x < 1:
                print("ERR:GetSimulationOfBackboardStatusWithShapeJ", x)
                x = 1
            Candidate_y[0] = self.GetYOfTopBlock(BackboardStatus, x - 1)
            Candidate_y[1] = self.GetYOfTopBlock(BackboardStatus, x)
            
            y = self.GetMinYOfBlock(Candidate_y[0], Candidate_y[1], 22, 22)
            
            BackboardStatus = self.AddBlock(BackboardStatus, x, y-3, 3)
            BackboardStatus = self.AddBlock(BackboardStatus, x, y-2, 3)
            BackboardStatus = self.AddBlock(BackboardStatus, x, y-1, 3)
            BackboardStatus = self.AddBlock(BackboardStatus, x - 1, y-1, 3)
        elif 1 == Shape_pattern:
            if x < 1:
                print("ERR:GetSimulationOfBackboardStatusWithShapeJ", x)
                x = 1
            elif x > 8:
                print("ERR:GetSimulationOfBackboardStatusWithShapeJ", x)
                x = 8
            Candidate_y[0] = self.GetYOfTopBlock(BackboardStatus, x - 1)
            Candidate_y[1] = self.GetYOfTopBlock(BackboardStatus, x)
            Candidate_y[2] = self.GetYOfTopBlock(BackboardStatus, x + 1)
            
            y = self.GetMinYOfBlock(Candidate_y[0], Candidate_y[1], Candidate_y[2], 22)

            BackboardStatus = self.AddBlock(BackboardStatus, x - 1, y - 2, 3)
            BackboardStatus = self.AddBlock(BackboardStatus, x - 1, y - 1, 3)
            BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 1, 3)
            BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 1, 3)
        elif 2 == Shape_pattern:
            if x > 8:
                print("ERR:GetSimulationOfBackboardStatusWithShapeJ", x)
                x = 8
            Candidate_y[0] = self.GetYOfTopBlock(BackboardStatus, x)
            Candidate_y[1] = self.GetYOfTopBlock(BackboardStatus, x + 1)
            if Candidate_y[1] < Candidate_y[0] - 2:
                y = Candidate_y[1]
                BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 1, 3)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 1, 3)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y,     3)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y + 1, 3)
            else:
                y = Candidate_y[0]
                BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 3, 3)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 3, 3)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 2, 3)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 1, 3)
            
        elif 3 == Shape_pattern:
            if x < 1:
                print("ERR:GetSimulationOfBackboardStatusWithShapeJ", x)
                x = 1
            elif x > 8:
                print("ERR:GetSimulationOfBackboardStatusWithShapeJ", x)
                x = 8
            Candidate_y[0] = self.GetYOfTopBlock(BackboardStatus, x - 1)
            Candidate_y[1] = self.GetYOfTopBlock(BackboardStatus, x)
            Candidate_y[2] = self.GetYOfTopBlock(BackboardStatus, x + 1)

            y = self.GetMinYOfBlock(Candidate_y[0], Candidate_y[1], 22, 22)
            
            if Candidate_y[2] < y + 1:
                y = Candidate_y[2]
                BackboardStatus = self.AddBlock(BackboardStatus, x - 1, y - 2, 3)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 2, 3)
                BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 2, 3)
                BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 1, 3)
            else:
                BackboardStatus = self.AddBlock(BackboardStatus, x - 1, y - 1, 3)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 1, 3)
                BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 1, 3)
                BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y,     3)
                        
        return BackboardStatus


    def GetSimulationOfBackboardStatusWithShapeT(self, board_status,
                                                 Shape_direction, Shape_x):
        BackboardStatus = board_status
        Shape_pattern = 0
        x = Shape_x
        y = 0
        Candidate_y = [0, 0, 0]
        
        Shape_pattern = (self.CurrentDirection + Shape_direction)%4
        
        if 0 == Shape_pattern:
            if x > 8:
                print("ERR:GetSimulationOfBackboardStatusWithShapeT", x)
                x = 8
            Candidate_y[0] = self.GetYOfTopBlock(BackboardStatus, x)
            Candidate_y[1] = self.GetYOfTopBlock(BackboardStatus, x + 1)
            if Candidate_y[1] < Candidate_y[0] - 1:
                y = Candidate_y[1]
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 2, 4)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 1, 4)
                BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 1, 4)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y   ,  4)
            else:
                y = Candidate_y[0]
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 3, 4)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 2, 4)
                BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 2, 4)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 1, 4)

        elif 1 == Shape_pattern:
            if x < 1:
                print("ERR:GetSimulationOfBackboardStatusWithShapeT", x)
                x = 1
            elif x > 8:
                print("ERR:GetSimulationOfBackboardStatusWithShapeT", x)
                x = 8
            Candidate_y[0] = self.GetYOfTopBlock(BackboardStatus, x - 1)
            Candidate_y[1] = self.GetYOfTopBlock(BackboardStatus, x)
            Candidate_y[2] = self.GetYOfTopBlock(BackboardStatus, x + 1)

            y = self.GetMinYOfBlock(Candidate_y[0], Candidate_y[2], 22, 22)
            
            if Candidate_y[1] < y + 1:
                y = Candidate_y[1]
                BackboardStatus = self.AddBlock(BackboardStatus, x - 1, y - 2, 4)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 2, 4)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 1, 4)
                BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 2, 4)
            else:
                BackboardStatus = self.AddBlock(BackboardStatus, x - 1, y - 1, 4)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 1, 4)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y,     4)
                BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 1, 4)

        elif 2 == Shape_pattern:
            if x < 1:
                print("ERR:GetSimulationOfBackboardStatusWithShapeT", x)
                x = 1
            Candidate_y[0] = self.GetYOfTopBlock(BackboardStatus, x - 1)
            Candidate_y[1] = self.GetYOfTopBlock(BackboardStatus, x)
            if Candidate_y[0] < Candidate_y[1] - 1:
                y = Candidate_y[0]
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 2, 4)
                BackboardStatus = self.AddBlock(BackboardStatus, x - 1, y - 1, 4)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 1, 4)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y,     4)
            else:
                y = Candidate_y[1]
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 3, 4)
                BackboardStatus = self.AddBlock(BackboardStatus, x - 1, y - 2, 4)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 2, 4)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 1, 4)
            
        elif 3 == Shape_pattern:
            if x < 1:
                print("ERR:GetSimulationOfBackboardStatusWithShapeT", x)
                x = 1
            elif x > 8:
                print("ERR:GetSimulationOfBackboardStatusWithShapeT", x)
                x = 8
            Candidate_y[0] = self.GetYOfTopBlock(BackboardStatus, x - 1)
            Candidate_y[1] = self.GetYOfTopBlock(BackboardStatus, x)
            Candidate_y[2] = self.GetYOfTopBlock(BackboardStatus, x + 1)

            y = self.GetMinYOfBlock(Candidate_y[0], Candidate_y[1], Candidate_y[2], 22)

            BackboardStatus = self.AddBlock(BackboardStatus, x - 1, y - 1, 4)
            BackboardStatus = self.AddBlock(BackboardStatus, x    , y - 2, 4)
            BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 1, 4)
            BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 1, 4)
            
        return BackboardStatus
        

    def GetSimulationOfBackboardStatusWithShapeO(self, board_status,
                                                 Shape_direction, Shape_x):
        BackboardStatus = board_status
        Shape_pattern = 0
        x = Shape_x
        y = 0
        Candidate_y = [0, 0]

        Shape_pattern = (self.CurrentDirection + Shape_direction)%1
        
        if x > 8:
            print("ERR:GetSimulationOfBackboardStatusWithShapeO", x)
            x = 8
        Candidate_y[0] = self.GetYOfTopBlock(BackboardStatus, x)
        Candidate_y[1] = self.GetYOfTopBlock(BackboardStatus, x + 1)
        
        y = self.GetMinYOfBlock(Candidate_y[0], Candidate_y[1], 22, 22)
        
        BackboardStatus = self.AddBlock(BackboardStatus, x    , y - 2, 5)
        BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 2, 5)
        BackboardStatus = self.AddBlock(BackboardStatus, x    , y - 1, 5)
        BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 1, 5)
            
        return BackboardStatus


    def GetSimulationOfBackboardStatusWithShapeS(self, board_status,
                                                 Shape_direction, Shape_x):
        BackboardStatus = board_status
        Shape_pattern = 0
        x = Shape_x
        y = 0
        Candidate_y = [0, 0, 0]
        
        Shape_pattern = (self.CurrentDirection + Shape_direction)%2
        
        if 0 == Shape_pattern:
            if x < 1:
                print("ERR:GetSimulationOfBackboardStatusWithShapeS", x)
                x = 1
            elif x > 8:
                print("ERR:GetSimulationOfBackboardStatusWithShapeS", x)
                x = 8
            Candidate_y[0] = self.GetYOfTopBlock(BackboardStatus, x - 1)
            Candidate_y[1] = self.GetYOfTopBlock(BackboardStatus, x)
            Candidate_y[2] = self.GetYOfTopBlock(BackboardStatus, x + 1)

            y = self.GetMinYOfBlock(Candidate_y[0], Candidate_y[1], 22, 22)
            if Candidate_y[2] < y - 1:
                y = Candidate_y[2]
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 1, 6)
                BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 1, 6)
                BackboardStatus = self.AddBlock(BackboardStatus, x - 1, y    , 6)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y    , 6)
            else:
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 2, 6)
                BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 2, 6)
                BackboardStatus = self.AddBlock(BackboardStatus, x - 1, y - 1, 6)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 1, 6)
            
        elif 1 == Shape_pattern:
            if x > 8:
                print("ERR:GetSimulationOfBackboardStatusWithShapeS", x)
                x = 8
            Candidate_y[0] = self.GetYOfTopBlock(BackboardStatus, x)
            Candidate_y[1] = self.GetYOfTopBlock(BackboardStatus, x + 1)
            
            if Candidate_y[0] < Candidate_y[1] - 1:
                y = Candidate_y[0]
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 2, 6)
                BackboardStatus = self.AddBlock(BackboardStatus, x    , y - 1, 6)
                BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 1, 6)
                BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y,     6)
            else:
                y = Candidate_y[1]
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 3, 6)
                BackboardStatus = self.AddBlock(BackboardStatus, x    , y - 2, 6)
                BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 2, 6)
                BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 1, 6)
                            
        return BackboardStatus
        
        
    def GetSimulationOfBackboardStatusWithShapeZ(self, board_status,
                                                 Shape_direction, Shape_x):
        BackboardStatus = board_status
        Shape_pattern = 0
        x = Shape_x
        y = 0
        Candidate_y = [0, 0, 0]
        
        Shape_pattern = (self.CurrentDirection + Shape_direction)%2
        
        if 0 == Shape_pattern:
            if x < 1:
                print("ERR:GetSimulationOfBackboardStatusWithShapeZ", x)
                x = 1
            elif x > 8:
                print("ERR:GetSimulationOfBackboardStatusWithShapeZ", x)
                x = 8
            Candidate_y[0] = self.GetYOfTopBlock(BackboardStatus, x - 1)
            Candidate_y[1] = self.GetYOfTopBlock(BackboardStatus, x)
            Candidate_y[2] = self.GetYOfTopBlock(BackboardStatus, x + 1)

            y = self.GetMinYOfBlock(22, Candidate_y[1], Candidate_y[2], 22)
            if Candidate_y[0] < y - 1:
                y = Candidate_y[0]
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 1, 7)
                BackboardStatus = self.AddBlock(BackboardStatus, x - 1, y - 1, 7)
                BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y    , 7)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y    , 7)
            else:
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 2, 7)
                BackboardStatus = self.AddBlock(BackboardStatus, x - 1, y - 2, 7)
                BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 1, 7)
                BackboardStatus = self.AddBlock(BackboardStatus, x,     y - 1, 7)
            
        elif 1 == Shape_pattern:
            if x > 8:
                print("ERR:GetSimulationOfBackboardStatusWithShapeZ", x)
                x = 8
            Candidate_y[0] = self.GetYOfTopBlock(BackboardStatus, x)
            Candidate_y[1] = self.GetYOfTopBlock(BackboardStatus, x + 1)
            
            if Candidate_y[1] < Candidate_y[0] - 1:
                y = Candidate_y[1]
                BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 2, 7)
                BackboardStatus = self.AddBlock(BackboardStatus, x    , y - 1, 7)
                BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 1, 7)
                BackboardStatus = self.AddBlock(BackboardStatus, x    , y,     7)
            else:
                y = Candidate_y[0]
                BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 3, 7)
                BackboardStatus = self.AddBlock(BackboardStatus, x    , y - 2, 7)
                BackboardStatus = self.AddBlock(BackboardStatus, x + 1, y - 2, 7)
                BackboardStatus = self.AddBlock(BackboardStatus, x    , y - 1, 7)
                
        return BackboardStatus


    def GetSimulationOfBackboardStatus(self, board_status, 
                                       Shape_index, Shape_direction, Shape_x):
        #
        # Simulate BackboardStatus With Shape index and direction, x
        #
        #
        
        BackboardStatus = copy.deepcopy(board_status)
        
        if 1 == Shape_index:
            BackboardStatus = self.GetSimulationOfBackboardStatusWithShapeI(BackboardStatus,
                                                                            Shape_direction, 
                                                                            Shape_x)
        elif 2 == Shape_index:
            BackboardStatus = self.GetSimulationOfBackboardStatusWithShapeL(BackboardStatus,
                                                                            Shape_direction, 
                                                                            Shape_x)
        elif 3 == Shape_index:
            BackboardStatus = self.GetSimulationOfBackboardStatusWithShapeJ(BackboardStatus,
                                                                            Shape_direction, 
                                                                            Shape_x)
        elif 4 == Shape_index:
            BackboardStatus = self.GetSimulationOfBackboardStatusWithShapeT(BackboardStatus,
                                                                            Shape_direction, 
                                                                            Shape_x)
        elif 5 == Shape_index:
            BackboardStatus = self.GetSimulationOfBackboardStatusWithShapeO(BackboardStatus,
                                                                            Shape_direction, 
                                                                            Shape_x)
        elif 6 == Shape_index:
            BackboardStatus = self.GetSimulationOfBackboardStatusWithShapeS(BackboardStatus,
                                                                            Shape_direction, 
                                                                            Shape_x)
        elif 7 == Shape_index:
            BackboardStatus = self.GetSimulationOfBackboardStatusWithShapeZ(BackboardStatus,
                                                                            Shape_direction, 
                                                                            Shape_x)
#        print(Shape_index, Shape_x, Shape_direction)
#        pprint.pprint(BackboardStatus, width = 61, compact = True)
        return BackboardStatus


    def GetEraceCountInBackboard(self, board_status):
        #
        #
        #
        BackboardStatus = board_status
        EraceCount = 0
        
        for y in range(22):
            if board_status[y][0] > 0 and board_status[y][1] > 0 and board_status[y][2] > 0 and \
               board_status[y][3] > 0 and board_status[y][4] > 0 and board_status[y][5] > 0 and \
               board_status[y][6] > 0 and board_status[y][7] > 0 and board_status[y][8] > 0 and \
               board_status[y][9] > 0:
               
               EraceCount = EraceCount + 1
               
        return EraceCount


BLOCK_CONTROLLER = Block_Controller()


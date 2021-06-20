#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
import pprint
import random

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
        self.CurrentShape_index = GameStatus["block_info"]["currentShape"]["index"]
        self.CurrentDirection = GameStatus["block_info"]["currentDirection"]
        
        print("Direction = ", self.CurrentDirection)
	
        # search best nextMove -->
        # random sample
        nextMove["strategy"]["direction"] = random.randint(0,3)
        nextMove["strategy"]["x"] = random.randint(0,9)
        nextMove["strategy"]["y_operation"] = 1
        nextMove["strategy"]["y_moveblocknum"] = 0
#        nextMove["strategy"]["y_moveblocknum"] = random.randint(1,8)
        
        self.board_status = self.GetBackboardStatus(self.board_backboard)
        pprint.pprint(self.board_status, width = 61, compact = True);
#        print(self.GetNumOfSpace(self.board_status))
        
        BackboardStatus = self.GetSimulationOfBackboardStatus(self.board_status,
                                            self.CurrentShape_index,
                                            nextMove["strategy"]["direction"],
                                            nextMove["strategy"]["x"])
        print(self.GetNumOfSpace(BackboardStatus))
        
        # test position by shape index
#        if 1 == self.CurrentShape_index:
#            nextMove["strategy"]["x"] = 0;
#        elif 2 == self.CurrentShape_index:
#            nextMove["strategy"]["x"] = 1;
#        elif 3 == self.CurrentShape_index:
#            nextMove["strategy"]["x"] = 2;
#        elif 4 == self.CurrentShape_index:
#            nextMove["strategy"]["x"] = 3;
#        elif 5 == self.CurrentShape_index:
#            nextMove["strategy"]["x"] = 4;
#        elif 6 == self.CurrentShape_index:
#            nextMove["strategy"]["x"] = 5;
#        elif 7 == self.CurrentShape_index:
#            nextMove["strategy"]["x"] = 6;
        
        
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
            print("Shape Pattern 0")
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
            print("Shape Pattern 1")
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
            print("Shape Pattern 2")
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
            print("Shape Pattern 3")
            if x < 1:
                print("ERR:GetSimulationOfBackboardStatusWithShapeJ", x)
                x = 1
            elif x > 8:
                print("ERR:GetSimulationOfBackboardStatusWithShapeL", x)
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
            print("Shape Pattern 0")

        elif 1 == Shape_pattern:
            print("Shape Pattern 1")

        elif 2 == Shape_pattern:
            print("Shape Pattern 2")
            
        elif 3 == Shape_pattern:
            print("Shape Pattern 3")
                        
        return BackboardStatus
        

    def GetSimulationOfBackboardStatusWithShapeO(self, board_status,
                                                 Shape_direction, Shape_x):
        BackboardStatus = board_status
        Shape_pattern = 0
        x = Shape_x
        y = 0
        Candidate_y = [0, 0]
        
        print("Shape Pattern 0")
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
            print("Shape Pattern 0")

        elif 1 == Shape_pattern:
            print("Shape Pattern 1")
                        
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
            print("Shape Pattern 0")

        elif 1 == Shape_pattern:
            print("Shape Pattern 1")
                        
        return BackboardStatus


    def GetSimulationOfBackboardStatus(self, board_status, 
                                       Shape_index, Shape_direction, Shape_x):
        #
        # Simulate BackboardStatus With Shape index and direction, x
        #
        #
        
        BackboardStatus = board_status
        
        if 1 == Shape_index:
            print(Shape_index)
            BackboardStatus = self.GetSimulationOfBackboardStatusWithShapeI(board_status,
                                                                            Shape_direction, 
                                                                            Shape_x)
            pprint.pprint(BackboardStatus, width = 61, compact = True);
        elif 2 == Shape_index:
            print(Shape_index)
            BackboardStatus = self.GetSimulationOfBackboardStatusWithShapeL(board_status,
                                                                            Shape_direction, 
                                                                            Shape_x)
            pprint.pprint(BackboardStatus, width = 61, compact = True);
        elif 3 == Shape_index:
            print(Shape_index)
            BackboardStatus = self.GetSimulationOfBackboardStatusWithShapeJ(board_status,
                                                                            Shape_direction, 
                                                                            Shape_x)
            pprint.pprint(BackboardStatus, width = 61, compact = True);
        elif 4 == Shape_index:
            print(Shape_index)
            BackboardStatus = self.GetSimulationOfBackboardStatusWithShapeT(board_status,
                                                                            Shape_direction, 
                                                                            Shape_x)
            pprint.pprint(BackboardStatus, width = 61, compact = True);
        elif 5 == Shape_index:
            print(Shape_index)
            BackboardStatus = self.GetSimulationOfBackboardStatusWithShapeO(board_status,
                                                                            Shape_direction, 
                                                                            Shape_x)
            pprint.pprint(BackboardStatus, width = 61, compact = True);
        elif 6 == Shape_index:
            print(Shape_index)
            BackboardStatus = self.GetSimulationOfBackboardStatusWithShapeS(board_status,
                                                                            Shape_direction, 
                                                                            Shape_x)
            pprint.pprint(BackboardStatus, width = 61, compact = True);
        elif 7 == Shape_index:
            print(Shape_index)
            BackboardStatus = self.GetSimulationOfBackboardStatusWithShapeZ(board_status,
                                                                            Shape_direction, 
                                                                            Shape_x)
            pprint.pprint(BackboardStatus, width = 61, compact = True);

        return BackboardStatus


BLOCK_CONTROLLER = Block_Controller()


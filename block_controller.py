#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
import pprint
import random
import copy

class Block_Controller(object):

    # init parameter
    Mode = 2
    
    board_backboard = 0
    board_data_width = 10
    board_data_height = 22
    board_status = 0
    ShapeNone_index = 0
    CurrentShape_class = 0
    CurrentShape_index = 0
    CurrentDirection = 0
    NextShape_class = 0
    
    BlockIndexNo = 0
    
    LatestEvalSpace = 100000
    LatestEvalSpaceOfWidth = 10000
    LatestEvalSpaceOfWidthUnderHalf = 10000
    LatestEvalAverageHeight = 0
    LatestEvalMaxHeight = 0
    LatestEvalMinHeight = 100000
    LatestEvalMaxMinHeight = 100000
    LatestEvalEraceCount = 0
    LatestBackboardStatus = 0
    
    LatestDirection = 0
    LatestX = 0

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
        self.board_data_width = GameStatus["field_info"]["width"]
        self.board_data_height = GameStatus["field_info"]["height"]
        # current Shape info
        CurrentShapeDirectionRange = GameStatus["block_info"]["currentShape"]["direction_range"]
        self.CurrentShape_index = GameStatus["block_info"]["currentShape"]["index"]
        self.CurrentDirection = GameStatus["block_info"]["currentDirection"]
	
        self.BlockIndexNo = GameStatus["judge_info"]["block_index"]
        
        # search best nextMove -->
        nextMove["strategy"]["y_operation"] = 1
        nextMove["strategy"]["y_moveblocknum"] = 0
        
        self.board_status = self.GetBackboardStatus(self.board_backboard)
        pprint.pprint(self.board_status, width = 61, compact = True);
        
        # search with current block Shape
        # Initialize Latest Scores And NextMove

        if (self.Mode == 0):
            nextMove = self.GetNextMoveByGameModeZero(nextMove, GameStatus)
        elif (self.Mode == 1):
            nextMove = self.GetNextMoveByGameModeOne(nextMove, GameStatus)
        elif (self.Mode == 2):
            nextMove = self.GetNextMoveByGameModeTwo(nextMove, GameStatus)
        elif (self.Mode == 3):
            nextMove = self.GetNextMoveByGameModeThree(nextMove, GameStatus)
        elif (self.Mode == 4):
            nextMove = self.GetNextMoveByGameModeFour(nextMove, GameStatus)

        # return nextMove
        print("===", datetime.now() - t1)
        print(nextMove)
        return nextMove

    def GetNextMoveByGameModeZero(self, nextMove, GameStatus):
    
        CurrentShapeDirectionRange = GameStatus["block_info"]["currentShape"]["direction_range"]
    
        # search with current block Shape
        # Initialize Latest Scores And NextMove
        self.UpdateLatestEval(100000, 100000, 100000,
                              0, 0, 0,
                              100000, 100000, self.board_status)
        self.UpdateLatestNextMove(0, 0)
        
        break_flag = 0

        for direction0 in CurrentShapeDirectionRange:
            if( break_flag > 0):
                break
        
            # search with x
            for x0 in range(self.board_data_width):
                BackboardStatus = self.GetSimulationOfBackboardStatus(self.board_status,
                                                                      self.CurrentShape_index,
                                                                      direction0,
                                                                      x0)
                EvalSpace = self.GetNumOfSpace(BackboardStatus)
                EvalSpaceOfWidth = self.GetNumOfSpaceWidth(BackboardStatus)
                EvalSpaceOfWidthUnderHalf = self.GetNumOfSpaceWidthUnderHalf(BackboardStatus)
                EvalEraceCount = self.GetEraceCountInBackboard(BackboardStatus)
                EvalAverageHeight = self.GetYOfAverageBlock(BackboardStatus)
                EvalMaxHeight = self.GetYOfMaxBlock(BackboardStatus)
                EvalMinHeight = self.GetYOfMinBlock(BackboardStatus)
                EvalMaxMinHeight = EvalMinHeight - EvalMaxHeight
                print(EvalSpace, EvalSpaceOfWidth, EvalSpaceOfWidthUnderHalf,
                      EvalEraceCount, EvalAverageHeight, EvalMaxHeight,
                      EvalMinHeight, EvalMaxMinHeight)

                if( EvalEraceCount > 2 ):
                    self.UpdateLatestEval(EvalSpace, EvalSpaceOfWidth, EvalSpaceOfWidthUnderHalf,
                                          EvalEraceCount, EvalAverageHeight, EvalMaxHeight,
                                          EvalMinHeight, EvalMaxMinHeight, BackboardStatus)
                    self.UpdateLatestNextMove(direction0, x0)
                    
                    break_flag = 1
                    break

                if( EvalSpace < self.LatestEvalSpace ):
                    self.UpdateLatestEval(EvalSpace, EvalSpaceOfWidth, EvalSpaceOfWidthUnderHalf,
                                          EvalEraceCount, EvalAverageHeight, EvalMaxHeight,
                                          EvalMinHeight, EvalMaxMinHeight, BackboardStatus)
                    self.UpdateLatestNextMove(direction0, x0)
                elif( EvalSpace == self.LatestEvalSpace ):
                    if( EvalMaxMinHeight < self.LatestEvalMaxMinHeight ):
                        self.UpdateLatestEval(EvalSpace, EvalSpaceOfWidth, EvalSpaceOfWidthUnderHalf,
                                              EvalEraceCount, EvalAverageHeight, EvalMaxHeight,
                                              EvalMinHeight, EvalMaxMinHeight, BackboardStatus)
                        self.UpdateLatestNextMove(direction0, x0)
                    elif( EvalMaxMinHeight == self.LatestEvalMaxMinHeight\
                      and EvalSpaceOfWidthUnderHalf < self.LatestEvalSpaceOfWidthUnderHalf ):
                         self.UpdateLatestEval(EvalSpace, EvalSpaceOfWidth, EvalSpaceOfWidthUnderHalf,
                                               EvalEraceCount, EvalAverageHeight, EvalMaxHeight,
                                               EvalMinHeight, EvalMaxMinHeight, BackboardStatus)
                         self.UpdateLatestNextMove(direction0, x0)
         

        nextMove["strategy"]["direction"] = self.LatestDirection
        nextMove["strategy"]["x"] = self.LatestX

        print(self.CurrentShape_index)        
        print(self.LatestEvalSpace, self.LatestEvalSpaceOfWidth, self.LatestEvalSpaceOfWidthUnderHalf,
              self.LatestEvalEraceCount, self.LatestEvalAverageHeight, self.LatestEvalMaxHeight,
              self.LatestEvalMinHeight, self.LatestEvalMaxMinHeight)
        pprint.pprint(self.LatestBackboardStatus, width = 61, compact = True)
    
        return nextMove

    def GetNextMoveByGameModeOne(self, nextMove, GameStatus):

        CurrentShapeDirectionRange = GameStatus["block_info"]["currentShape"]["direction_range"]
    
        # search with current block Shape
        # Initialize Latest Scores And NextMove
        self.UpdateLatestEval(100000, 100000, 100000,
                              0, 0, 0,
                              100000, 100000, self.board_status)
        self.UpdateLatestNextMove(0, 0)
        
        break_flag = 0

        for direction0 in CurrentShapeDirectionRange:
            if( break_flag > 0):
                break
        
            # search with x
            for x0 in range(self.board_data_width):
                BackboardStatus = self.GetSimulationOfBackboardStatus(self.board_status,
                                                                      self.CurrentShape_index,
                                                                      direction0,
                                                                      x0)
                EvalSpace = self.GetNumOfSpace(BackboardStatus)
                EvalSpaceOfWidth = self.GetNumOfSpaceWidth(BackboardStatus)
                EvalSpaceOfWidthUnderHalf = self.GetNumOfSpaceWidthUnderHalf(BackboardStatus)
                EvalEraceCount = self.GetEraceCountInBackboard(BackboardStatus)
                EvalAverageHeight = self.GetYOfAverageBlock(BackboardStatus)
                EvalMaxHeight = self.GetYOfMaxBlock(BackboardStatus)
                EvalMinHeight = self.GetYOfMinBlock(BackboardStatus)
                EvalMaxMinHeight = EvalMinHeight - EvalMaxHeight
                print(EvalSpace, EvalSpaceOfWidth, EvalSpaceOfWidthUnderHalf,
                      EvalEraceCount, EvalAverageHeight, EvalMaxHeight,
                      EvalMinHeight, EvalMaxMinHeight)

                if( EvalEraceCount > 0 ):
                    self.UpdateLatestEval(EvalSpace, EvalSpaceOfWidth, EvalSpaceOfWidthUnderHalf,
                                          EvalEraceCount, EvalAverageHeight, EvalMaxHeight,
                                          EvalMinHeight, EvalMaxMinHeight, BackboardStatus)
                    self.UpdateLatestNextMove(direction0, x0)
                    
                    break_flag = 1
                    break

                if( EvalMaxHeight > self.LatestEvalMaxHeight ):
                    self.UpdateLatestEval(EvalSpace, EvalSpaceOfWidth, EvalSpaceOfWidthUnderHalf,
                                          EvalEraceCount, EvalAverageHeight, EvalMaxHeight,
                                          EvalMinHeight, EvalMaxMinHeight, BackboardStatus)
                    self.UpdateLatestNextMove(direction0, x0)
                elif( EvalMaxHeight == self.LatestEvalMaxHeight ):
                    if ( EvalSpace < self.LatestEvalSpace ):
                        self.UpdateLatestEval(EvalSpace, EvalSpaceOfWidth, EvalSpaceOfWidthUnderHalf,
                                              EvalEraceCount, EvalAverageHeight, EvalMaxHeight,
                                              EvalMinHeight, EvalMaxMinHeight, BackboardStatus)
                        self.UpdateLatestNextMove(direction0, x0)
                    elif( EvalSpace == self.LatestEvalSpace and EvalMaxMinHeight < self.LatestEvalMaxMinHeight ):
                        self.UpdateLatestEval(EvalSpace, EvalSpaceOfWidth, EvalSpaceOfWidthUnderHalf,
                                              EvalEraceCount, EvalAverageHeight, EvalMaxHeight,
                                              EvalMinHeight, EvalMaxMinHeight, BackboardStatus)
                        self.UpdateLatestNextMove(direction0, x0)
                    elif( EvalSpace == self.LatestEvalSpace and EvalMaxMinHeight == self.LatestEvalMaxMinHeight\
                      and EvalSpaceOfWidthUnderHalf < self.LatestEvalSpaceOfWidthUnderHalf ):
                         self.UpdateLatestEval(EvalSpace, EvalSpaceOfWidth, EvalSpaceOfWidthUnderHalf,
                                               EvalEraceCount, EvalAverageHeight, EvalMaxHeight,
                                               EvalMinHeight, EvalMaxMinHeight, BackboardStatus)
                         self.UpdateLatestNextMove(direction0, x0)
         

        nextMove["strategy"]["direction"] = self.LatestDirection
        nextMove["strategy"]["x"] = self.LatestX

        print(self.CurrentShape_index)        
        print(self.LatestEvalSpace, self.LatestEvalSpaceOfWidth, self.LatestEvalSpaceOfWidthUnderHalf,
              self.LatestEvalEraceCount, self.LatestEvalAverageHeight, self.LatestEvalMaxHeight,
              self.LatestEvalMinHeight, self.LatestEvalMaxMinHeight)
        pprint.pprint(self.LatestBackboardStatus, width = 61, compact = True)
    
        return nextMove

    def GetNextMoveByGameModeTwo(self, nextMove, GameStatus):
            if ( self.GetYOfMaxBlock(self.board_status) > self.board_data_height/2 ):
                nextMove = self.GetNextMoveByGameModeZero(nextMove, GameStatus)
            else:
                nextMove = self.GetNextMoveByGameModeOne(nextMove, GameStatus)
            return nextMove

    def GetNextMoveByGameModeThree(self, nextMove, GameStatus):
        MoveList = [[1,   1, 1, 2], [2,   2, 3, 5], [3,   3, 0, 8], [4,   4, 3, 4], [5,   5, 0, 0], 
                    [6,   6, 1, 6], [7,   7, 1, 2], [8,   1, 0, 0], [9,   2, 0, 1], [10,  3, 0, 8],
                    [11,  4, 2, 5], [12,  5, 0, 6], [13,  6, 0, 4], [14,  7, 1, 2], [15,  1, 0, 9],
                    [16,  2, 3, 7], [17,  3, 0, 2], [18,  4, 0, 7], [19,  5, 0, 0], [20,  6, 1, 7],
                    [21,  7, 0, 4], [22,  1, 0, 6], [23,  2, 0, 0], [24,  3, 3, 4], [25,  4, 3, 3],
                    [26,  5, 0, 1], [27,  6, 1, 4], [28,  7, 0, 5], [29,  1, 0, 9], [30,  2, 0, 4],
                    [31,  3, 3, 2], [32,  4, 0, 0], [33,  5, 0, 2], [34,  6, 1, 0], [35,  7, 0, 2],
                    [36,  1, 0, 0], [37,  2, 0, 1], [38,  3, 3, 7], [39,  4, 2, 6], [40,  5, 0, 7],
                    [41,  6, 1, 0], [42,  7, 0, 7], [43,  1, 0, 9], [44,  2, 2, 3], [45,  3, 3, 7],
                    [46,  4, 2, 5], [47,  5, 0, 2], [48,  6, 1, 0], [49,  7, 1, 4], [50,  1, 0, 9],
                    [51,  2, 2, 4], [52,  3, 1, 7], [53,  4, 0, 2], [54,  5, 0, 7], [55,  6, 0, 6],
                    [56,  7, 0, 1], [57,  1, 0, 9], [58,  2, 2, 3], [59,  3, 3, 7], [60,  4, 3, 2],
                    [61,  5, 0, 7], [62,  6, 1, 4], [63,  7, 0, 5], [64,  1, 0, 9], [65,  2, 1, 7],
                    [66,  3, 1, 7], [67,  4, 0, 0], [68,  5, 0, 4], [69,  6, 1, 0], [70,  7, 0, 7],
                    [71,  1, 0, 0], [72,  2, 2, 2], [73,  3, 3, 7], [74,  4, 3, 4], [75,  5, 0, 1],
                    [76,  6, 1, 4], [77,  7, 0, 5], [78,  1, 0, 3], [79,  2, 2, 1], [80,  3, 0, 8],
                    [81,  4, 3, 4], [82,  5, 0, 6], [83,  6, 0, 3], [84,  7, 1, 2], [85,  1, 0, 9],
                    [86,  2, 0, 0], [87,  3, 0, 8], [88,  4, 1, 2], [89,  5, 0, 5], [90,  6, 1, 6],
                    [91,  7, 0, 1], [92,  1, 0, 9], [93,  2, 0, 4], [94,  3, 0, 8], [95,  4, 0, 5],
                    [96,  5, 0, 0], [97,  6, 1, 2], [98,  7, 1, 4], [99,  1, 0, 9], [100, 2, 0, 3],
                    [101, 3, 3, 1], [102, 4, 3, 2], [103, 5, 0, 4], [104, 6, 1, 6], [105, 7, 0, 7],
                    [106, 1, 0, 9], [107, 2, 0, 4], [108, 3, 3, 7], [109, 4, 0, 0], [110, 5, 0, 6],
                    [111, 6, 1, 2], [112, 7, 0, 3], [113, 1, 0, 8], [114, 2, 3, 6], [115, 3, 0, 8],
                    [116, 4, 2, 1], [117, 5, 0, 5], [118, 6, 1, 3], [119, 7, 1, 0], [120, 1, 0, 9],
                    [121, 2, 2, 2], [122, 3, 2, 0], [123, 4, 3, 6], [124, 5, 0, 0], [125, 6, 1, 4],
                    [126, 7, 1, 7], [127, 1, 0, 2], [128, 2, 0, 0], [129, 3, 0, 2], [130, 4, 0, 6],
                    [131, 5, 0, 7], [132, 6, 1, 0], [133, 7, 0, 1], [134, 1, 0, 9], [135, 2, 0, 0],
                    [136, 3, 2, 5], [137, 4, 0, 3], [138, 5, 0, 7], [139, 6, 1, 3], [140, 7, 0, 5],
                    [141, 1, 0, 9], [142, 2, 2, 2], [143, 3, 3, 5], [144, 4, 0, 3], [145, 5, 0, 7],
                    [146, 6, 0, 6], [147, 7, 0, 1], [148, 1, 0, 9], [149, 2, 0, 4], [150, 3, 2, 3],
                    [151, 4, 2, 8], [152, 5, 0, 5], [153, 6, 1, 1], [154, 7, 1, 7], [155, 1, 0, 9],
                    [156, 2, 0, 3], [157, 3, 2, 0], [158, 4, 0, 6], [159, 5, 0, 0], [160, 6, 1, 2],
                    [161, 7, 0, 7], [162, 1, 0, 5], [163, 2, 0, 0], [164, 3, 2, 4], [165, 4, 2, 8],
                    [166, 5, 0, 4], [167, 6, 1, 2], [168, 7, 1, 6], [169, 1, 0, 9], [170, 2, 2, 1],
                    [171, 3, 3, 5], [172, 4, 2, 8], [173, 5, 0, 3], [174, 6, 0, 7], [175, 7, 1, 5],
                    [176, 1, 0, 9], [177, 2, 2, 9], [178, 3, 0, 5], [179, 4, 0, 2], [180, 5, 0, 0]]

        if (self.BlockIndexNo <= len(MoveList) and self.BlockIndexNo == MoveList[self.BlockIndexNo-1][0]\
                                               and self.CurrentShape_index == MoveList[self.BlockIndexNo-1][1]):            
            # Set nextMove Scenario
            nextMove["strategy"]["direction"] = MoveList[self.BlockIndexNo-1][2]
            nextMove["strategy"]["x"]         = MoveList[self.BlockIndexNo-1][3]
        else:
            nextMove = self.GetNextMoveByGameModeTwo(nextMove, GameStatus)
            self.Mode = 2

        return nextMove
            
    def GetNextMoveByGameModeFour(self, nextMove, GameStatus):
    
        return nextMove

    def GetShapeDirectionSerchList(self):
        
        if 1 == self.CurrentShape_index:
            ReturnShapeDirectionRange = [0, 1]
        elif 2 == self.CurrentShape_index:
            ReturnShapeDirectionRange = [2, 0, 1, 3]
        elif 3 == self.CurrentShape_index:
            ReturnShapeDirectionRange = [2, 0, 1, 3]
        elif 4 == self.CurrentShape_index:
            ReturnShapeDirectionRange = [1, 0, 2, 3]
        elif 5 == self.CurrentShape_index:
            ReturnShapeDirectionRange = [0]
        elif 6 == self.CurrentShape_index:
            ReturnShapeDirectionRange = [0, 1]
        elif 7 == self.CurrentShape_index:
            ReturnShapeDirectionRange = [0, 1]

        return ReturnShapeDirectionRange

    def UpdateLatestEval(self, EvalSpace, EvalSpaceOfWidth, EvalSpaceOfWidthUnderHalf, 
                               EvalEraceCount, EvalAverageHeight, EvalMaxHeight,
                               EvalMinHeight, EvalMaxMinHeight, BackboardStatus):
    
        self.LatestEvalSpace                 = EvalSpace
        self.LatestEvalSpaceOfWidth          = EvalSpaceOfWidth
        self.LatestEvalSpaceOfWidthUnderHalf = EvalSpaceOfWidthUnderHalf
        self.LatestEvalEraceCount            = EvalEraceCount
        self.LatestEvalAverageHeight         = EvalAverageHeight
        self.LatestEvalMaxHeight             = EvalMaxHeight
        self.LatestEvalMinHeight             = EvalMinHeight
        self.LatestEvalMaxMinHeight          = EvalMaxMinHeight
        self.LatestBackboardStatus           = copy.deepcopy(BackboardStatus)
        
        return 0
        
    def UpdateLatestNextMove(self, direction, x):
    
        self.LatestDirection = direction
        self.LatestX = x
    
        return 0

    def GetBackboardStatus(self, board_backboard):
        #
        # get Backboard Status by 0/1.
        # in two-dimensional array
        #

        BackboardStatus = self.convert_1d_to_2d(board_backboard, self.board_data_width)
        
        for y in range(self.board_data_height):
            for x in range(self.board_data_width):
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
        for x in range(self.board_data_width):
            first_block = 0
            for y in range(self.board_data_height):
                if board_status[y][x] == 0 and first_block == 1:
                    count = count + 1
                elif board_status[y][x] > 0 and first_block == 0:
                    first_block = 1
        return count

    def GetNumOfSpaceWidthWithRange(self, board_status, start, end):
        # 
        # Get Space Num. 
        # Count Space Of Width.
        #
        
        count = 0
        for y in range(start, end):
            width_block = 0
            count_of_y = 0
            for x in range(self.board_data_width):
                if board_status[y][x] == 0:
                    count_of_y = count_of_y + 1
                elif board_status[y][x] > 0 and width_block == 0:
                    width_block = 1
            if(width_block == 1):
                count = count + count_of_y
                
        return count

    def GetNumOfSpaceWidth(self, board_status):
        # 
        # Get Space Num. 
        # Count Space Of Width.
        #
        
        return self.GetNumOfSpaceWidthWithRange(board_status, 0, self.board_data_height)
        
        
    def GetNumOfSpaceWidthUnderHalf(self, board_status):
        # 
        # Get Space Num. 
        # Count Space Of Width.
        # 14 22 14426
        
        return self.GetNumOfSpaceWidthWithRange(board_status, self.board_data_height - 8, self.board_data_height)

    def AddBlock(self, board_status, x, y, index):
    
        BackboardStatus = board_status
        if BackboardStatus[y][x] == 0:
            BackboardStatus[y][x] = index
        elif BackboardStatus[y][x] > 0:
            print("ERR:AddBlock", x, y)
            pprint.pprint(BackboardStatus, width = 61, compact = True);
        
        return BackboardStatus

    def GetYOfTopBlock(self, board_status, x):
        return_y = self.board_data_height
        for y in range(self.board_data_height):
            if board_status[y][x] > 0:
                return_y = y
                break
        return return_y

    def GetYOfAverageBlock(self, board_status):
        average = 0;
        for x in range(self.board_data_width):
            average = average + self.GetYOfTopBlock(board_status, x)
                
        return average/self.board_data_width

    def GetYOfMaxBlock(self, board_status):
        max_y = self.board_data_height
        for x in range(self.board_data_width):
            if self.GetYOfTopBlock(board_status, x) < max_y:
                max_y = self.GetYOfTopBlock(board_status, x)

        return max_y

    def GetYOfMinBlock(self, board_status):
        min_y = 0
        for x in range(self.board_data_width):
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
            
            y = self.GetMinYOfBlock(Candidate_y[0], Candidate_y[1], self.board_data_height, self.board_data_height)
            
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
            
            y = self.GetMinYOfBlock(self.board_data_height, Candidate_y[1], Candidate_y[2], self.board_data_height)
            
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
            
            y = self.GetMinYOfBlock(Candidate_y[0], Candidate_y[1], Candidate_y[2], self.board_data_height)
            
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
            
            y = self.GetMinYOfBlock(Candidate_y[0], Candidate_y[1], self.board_data_height, self.board_data_height)
            
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
            
            y = self.GetMinYOfBlock(Candidate_y[0], Candidate_y[1], Candidate_y[2], self.board_data_height)

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

            y = self.GetMinYOfBlock(Candidate_y[0], Candidate_y[1], self.board_data_height, self.board_data_height)
            
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

            y = self.GetMinYOfBlock(Candidate_y[0], Candidate_y[2], self.board_data_height, self.board_data_height)
            
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

            y = self.GetMinYOfBlock(Candidate_y[0], Candidate_y[1], Candidate_y[2], self.board_data_height)

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
        
        y = self.GetMinYOfBlock(Candidate_y[0], Candidate_y[1], self.board_data_height, self.board_data_height)
        
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

            y = self.GetMinYOfBlock(Candidate_y[0], Candidate_y[1], self.board_data_height, self.board_data_height)
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

            y = self.GetMinYOfBlock(self.board_data_height, Candidate_y[1], Candidate_y[2], self.board_data_height)
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

        return BackboardStatus


    def GetEraceCountInBackboard(self, board_status):
        #
        #
        #
        BackboardStatus = board_status
        EraceCount = 0
        
        for y in range(self.board_data_height):
            if board_status[y][0] > 0 and board_status[y][1] > 0 and board_status[y][2] > 0 and \
               board_status[y][3] > 0 and board_status[y][4] > 0 and board_status[y][5] > 0 and \
               board_status[y][6] > 0 and board_status[y][7] > 0 and board_status[y][8] > 0 and \
               board_status[y][9] > 0:
               
               EraceCount = EraceCount + 1
               
        return EraceCount


BLOCK_CONTROLLER = Block_Controller()


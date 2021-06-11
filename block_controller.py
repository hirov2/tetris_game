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
    NextShape_class = 0
    
    CurrentShape_index = 0

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
        CurrentShape_index = GameStatus["block_info"]["currentShape"]["index"]
        print("GameStatus[field_info][backboard] =", GameStatus["field_info"]["backboard"])
	
	
	# current board info
        self.board_backboard = GameStatus["field_info"]["backboard"]
        # current Shape info
        self.CurrentShape_index = GameStatus["block_info"]["currentShape"]["index"]
	
        # search best nextMove -->
        # random sample
        nextMove["strategy"]["direction"] = random.randint(0,4)
        nextMove["strategy"]["x"] = random.randint(0,9)
        nextMove["strategy"]["y_operation"] = 1
        nextMove["strategy"]["y_moveblocknum"] = random.randint(1,8)
        
        self.board_status = self.GetBackboardStatus(self.board_backboard)
        
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
#        print("===", datetime.now() - t1)
#        print(nextMove)
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


BLOCK_CONTROLLER = Block_Controller()


#!/usr/bin/python
# -*- coding: utf-8 -*-

# Solve the 2048 puzzle without using any look ahead
# ie no wondering what it would be like to make a particular move
# especially we do not want to virtually take moves and then select the best move based on the virtual results
# the approach we want is similar to a closed form solution, but is actually rule based 

from __future__ import print_function
import time
import os

def print_board(m):
    for row in m:
        for c in row:
            print('%8d' % c, end=' ')
        print()


def movename(move):
    return ['up', 'down', 'left', 'right'][move]


def col(l, c):
    return [l[r][c] for r in 0, 1, 2, 3]


def transpose(board):
    return [col(board, r) for r in 3, 2, 1, 0]


ROW3, ROW2, ROW1, ROW0 = 3, 2, 1, 0
COL3, COL2, COL1, COL0 = 7, 6, 5, 4


def match(i1, i2):
    return any(map(lambda ( x, y ): ( x ) and ( x == y ), zip(i1, i2)))


class BoardEvaluator(object):
    def __init__(self, board):
        """

        :rtype : BoardEvaluator
        """
        self.b = board

    def set_board(self, board):
        self.b = board

    def get_board( self, board ):
        return self.b

    def equals( self, board ):
        return ( self.b == board )

    def print_board( self ):
        print_board( self.b )
    # fence fixer jose ramirez cib construction 310 384 9352

    def get(self, selector):
        d = {
            ROW0: self.b[0],
            ROW1: self.b[1],
            ROW2: self.b[2],
            ROW3: self.b[3],
            COL0: col(self.b, 0),
            COL1: col(self.b, 1),
            COL2: col(self.b, 2),
            COL3: col(self.b, 3)
        }
        return d[selector]

    def is_full(self, selector):
        # temp = self.get( selector ) 
        # print ( "@@@@ ", temp, all( temp ) )
        return all(self.get(selector))

    def num_open(self):
        return sum(map(lambda i: sum(map(lambda x: not x, i)), self.b))

    def is_compressible(self, selector):
        test = self.get(selector)
        return match(test[0:3], test[1:4])
        # highfalutin way of saying 
        # return ( ( test[0] == test[1] ) or ( test[1] == test[2] ) or ( test[2] == test[3] ) )
        # yes! I wrote this comment just to use "highfalutin".  highfalutin, highfalutin, highfalutin

    def is_sorted(self, selector):
        test = self.get(selector)
        return sorted(test) == test

    def first_empty(self, selector):
        test = self.get(selector)
        return ( not ( test[0] ) )

    def br_is_biggest(self):
        br = self.b[3][3]
        biggest = max(map(max, self.b))
        return br == biggest

    # needs a lot more tests
    def lap_helper(self, index):
        this_row = index
        next_row = ( index + 1 )
        return ( ( self.is_full(next_row) ) and
                 ( ( not self.is_compressible(next_row) ) and ( not self.is_compressible(this_row) ) ) and
                 (
                     ( not ( any(self.b[this_row][0:1]) ) and match(self.b[next_row][0:3], self.b[this_row][1:4]) ) or
                     ( not ( any(self.b[this_row][0:2]) ) and match(self.b[next_row][0:2], self.b[this_row][2:4]) ) or
                     ( not ( any(self.b[this_row][0:3]) ) and match(self.b[next_row][0:1], self.b[this_row][3:4]) )
                 )
        )

    def left_align_opp(self):
        return (
            self.lap_helper(ROW2) or
            ( self.is_full(ROW3) and ( not self.is_compressible(ROW3) ) and self.lap_helper(ROW1) ) or
            (self.is_full(ROW3) and ( not self.is_compressible(ROW3) ) and self.is_full(ROW2) and (
                not self.is_compressible(ROW2) ) and self.lap_helper(ROW0) )
        )

    def rao_helper(self, index):
        this_row = index
        next_row = ( index + 1 )
        return (( self.is_full(next_row) ) and ( not self.is_compressible(next_row) ) and (
            not self.is_compressible(this_row) ) and
                (
                    ( not ( any(self.b[this_row][3:4]) ) and match(self.b[this_row][0:3], self.b[next_row][1:4]) ) or
                    ( not ( any(self.b[this_row][2:4]) ) and match(self.b[this_row][0:2], self.b[next_row][2:4]) ) or
                    ( not ( any(self.b[this_row][1:4]) ) and match(self.b[this_row][0:1], self.b[next_row][3:4]) )
                )
        )

    def right_align_opp(self):
        return (
            self.rao_helper(ROW2) or
            ( self.is_full(ROW3) and ( not self.is_compressible(ROW3) ) and self.rao_helper(ROW1) ) or
            (self.is_full(ROW3) and ( not self.is_compressible(ROW3) ) and self.is_full(ROW2) and (
                not self.is_compressible(ROW2) ) and self.rao_helper(ROW0) )
        )


    def up_align_opp(self):
        temp = self.b
        self.set_board(transpose(self.b))
        uao = self.left_align_opp()
        self.set_board(temp)
        return uao

    def down_align_opp(self):
        temp = self.b
        self.set_board(transpose(self.b))
        rao = self.right_align_opp()
        self.set_board(temp)
        return rao


    def align_opp(self, direction):
        opp = [self.up_align_opp, self.down_align_opp, self.left_align_opp, self.right_align_opp][direction]
        return opp()

def rungame(args):
    from gamectrl import BrowserRemoteControl, Fast2048Control

    if len(args) == 1:
        port = int(args[0])
    else:
        port = 32000

    ctrl = BrowserRemoteControl(port)
    # Use Keyboard2048Control if Fast2048Control doesn't seem to be working.
    gamectrl = Fast2048Control(ctrl)
    board0 = gamectrl.get_board()
    be = BoardEvaluator(board0)
    moveno = 0
    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

    def go(direction):
        gamectrl.execute_move(direction)
        be.set_board( gamectrl.get_board() )


    def go_left():
        go(LEFT)

    def go_right():
        go(RIGHT)

    def go_up():
        go(UP)

    def go_down():
        go(DOWN)

    def flip(direction):
        return [DOWN, UP, RIGHT, LEFT][direction]


    if gamectrl.get_status() == 'ended':
        gamectrl.restart_game()

    moveno = 0
    start = time.time()
    br = False
    bd = False

    second_dir = RIGHT

    while ( not ( gamectrl.get_status() in  [ 'ended' , 'won' ] ) ):
            
        inv_count = 0
        flip_count = 0
        while True:
            board0 = gamectrl.get_board()
            go_down()
            if ( be.equals( board0 ) ):
                bd = True
                print(" down  has no effect ")

            # must come in handy when the board is full 
            if ( be.is_full(ROW3) and be.is_full(ROW2) and be.is_full(ROW1) ):
                print(" rows 321 are full  ")
                flip_dir = flip( second_dir )
                if be.align_opp(flip_dir):
                    print("F align opp for ", movename(flip_dir) )
                    be.print_board()
                    go(flip_dir)
                    be.print_board()
                    continue
                if be.align_opp(second_dir):
                    print("align opp for ", movename(( second_dir )))
                    be.print_board()
                    go(second_dir)
                    be.print_board()
                    continue
            # be.set_board(board1)
            if ( be.is_compressible(ROW3) ):  # or  ( not be.br_is_biggest() ) ):
                print("row3 is compressible, so second_dir is RIGHT ")
                second_dir = RIGHT
            else:
                flip_dir = flip( second_dir )
                if be.align_opp(flip_dir):
                    print("row3 is NOT compressible, and align opp for ", movename(flip_dir) ) 
                    go(flip_dir)
                    continue
            board1 = gamectrl.get_board()
            go(second_dir)
            
            if ( be.equals( board1 ) ):
                br = True
                print( movename( second_dir ), " has no effect " )
            
            board2 = gamectrl.get_board()

            if be.align_opp(flip(second_dir)):
                print("AO case 3: align_opp for ", flip( second_dir ) )
                go(flip(second_dir))
                continue

            if board0 == board2:

                inv_count += 1
                if ( inv_count > 2 ):
                    print("=============")
                    print_board(board0)
                    print(" inv_count = ", inv_count, "flip_count = ", flip_count)
                    if ( be.is_full(ROW3) and ( not be.is_compressible(ROW3) ) ):
                        second_dir = flip(second_dir)
                        inv_count = 0
                        flip_count += 1
                        if ( ( flip_count > 5 ) or ( gamectrl.get_status() in ['ended', 'won'] ) ):
                            print("flip_count > 5 or game finished ")
                            break
                    else:
                        print("row3 not full or not compressible")
                        break

        if ( be.num_open() < 3 ):
            print(" less than 3 open squares ")
            break
        else:
            print(" Number of open squares : ", be.num_open())

        # if ( all ( board2[3] ) ):
        if ( be.is_full(ROW3) and ( not be.is_compressible(ROW3) ) ):
            print(" DR did not work, Bottom row full and not compressible, so going left ")
            # time.sleep( 3 )
            go(flip(second_dir))
            boardx = gamectrl.get_board()
            if ( board2 == boardx ):
                print(
                    " <><><><><><><><><><><><><><><><><><><><><><><><><><><><> Hail Mary move: left failed, goin right")
                go(second_dir)
                boardx = gamectrl.get_board()

                if ( board2 == boardx ):
                    print(
                        " #$%#$%@#$%@#$%@#$%@#$%@#$%@#$%@#$%@#$%@#$%@#$%@#$%@#$%@#$%@#$%@$#%@#$ Hail Mary move: left and right failed, goinup ")
                    go_up()

                continue

        elif ( ( be.is_full(COL3) and ( not be.is_compressible(COL3) ) ) ):
            print(" DR did not work, Bottom row not full but Right col full and not compressible ")
            if ( be.up_align_opp() ):
                print(" BR not full but Roght Col full and I smell a up   opp ")
                # time.sleep( 3 )
                go_up()
                go_right()
                continue
            elif ( be.left_align_opp() ):
                print(" BR not full but Roght Col full and I smell a left opp ")
                # time.sleep( 3 )
                go_left()
                go_right()
                continue
            else:
                print(" BR not full but Roght Col full and I DO NOT smell a up opp but moving up any way")
                # time.sleep( 3 )
                go_up()
                # what if this fails? [ e.g. only the left most col is empty ]
                continue
        else:
            if ( be.num_open() < 3 ):
                print("all attempts failed and  less than 3 open squares ")
                # break
            board0 = gamectrl.get_board()
            print(
                " <><><><><><><><><><><><><><><><><><><><><><><><><><><><> the real Hail Hanuman move: Try left first ")
            go_left()
            board1 = gamectrl.get_board()
            if ( board0 == board1 ):
                go_up()
                print("case 6 " + movename(UP))
                board3 = gamectrl.get_board()
                if ( push_right_opp(board3) ):
                    go_right()
                    print("case 6+ " + movename(RIGHT))
            else:
                go_right()

    score = gamectrl.get_score()
    board = gamectrl.get_board()
    maxval = max(max(row) for row in board )
    moveno = gamectrl.moveno
    print("Game over. Final score %d; highest tile %d." % (score, 2 ** maxval))
    print("%010.6f: Score %d, Move %d, mps= %010.6f" % (
        time.time() - start, gamectrl.get_score(), moveno, ( moveno / ( time.time() - start) ) ))


if __name__ == '__main__':
    import sys

    rungame(sys.argv[1:])

"""Avaliador que reune todas as regras dos outros arquivos."""

from core.position import Position
from .base_evaluator import BaseEvaluator
from ..board_state import BoardState
from ..enums import PlayerColor


class AMPEvaluator(BaseEvaluator):

    # Pesos para diferentes tipos de peças
    NORMAL_PIECE_VALUE = 2.0
    KING_PIECE_VALUE = 4.0

    def evaluate(self, board: BoardState, color: PlayerColor) -> float:

        opponent_color = color.opposite()

        # Contar peças do jogador
        player_pieces = board.get_pieces_by_color(color)
        player_score = sum(
            self.KING_PIECE_VALUE if piece.is_king() else self.NORMAL_PIECE_VALUE
            for piece in player_pieces
        )

        # Contar peças do adversário
        opponent_pieces = board.get_pieces_by_color(opponent_color)
        opponent_score = sum(
            self.KING_PIECE_VALUE if piece.is_king() else self.NORMAL_PIECE_VALUE
            for piece in opponent_pieces
        )

        boardStateValue = player_score - opponent_score

        allpieces = board.get_all_pieces()

        #Verificando se podem capturar
        for piece in allpieces:
            if piece.position.row+2<=7 and piece.position.col+2<=7:
                if piece.color == color and board.get_piece(Position(piece.position.row+1, piece.position.col+1)) != None and piece.position.row+2<=7 and piece.position.col+2<=7:
                    if board.get_piece(Position(piece.position.row+1, piece.position.col+1)).color == color.opposite and (board.get_piece(Position(piece.position.row+2, piece.position.col+2)) == None):
                        boardStateValue += 1
            if piece.position.row+2<=7 and piece.position.col-2>=0:
                if piece.color == color and board.get_piece(Position(piece.position.row+1, piece.position.col-1)) != None:
                    if board.get_piece(Position(piece.position.row+1, piece.position.col-1)).color == color.opposite and (board.get_piece(Position(piece.position.row+2, piece.position.col-2)) == None):
                        boardStateValue += 1
            if piece.position.row-2>=0 and piece.position.col+2<=7:
                if piece.color == color and board.get_piece(Position(piece.position.row-1, piece.position.col+1)) != None:
                    if board.get_piece(Position(piece.position.row-1, piece.position.col+1)).color == color.opposite and (board.get_piece(Position(piece.position.row-2, piece.position.col+2)) == None):
                        boardStateValue += 1
            if piece.position.row-2>=0 and piece.position.col-2>=0:
                if piece.color == color and board.get_piece(Position(piece.position.row-1, piece.position.col-1)) != None:
                    if board.get_piece(Position(piece.position.row-1, piece.position.col-1)).color == color.opposite and (board.get_piece(Position(piece.position.row-2, piece.position.col-2)) == None):
                        boardStateValue += 1
            
            if piece.position.row+2<=7 and piece.position.col+2<=7:
                if piece.color == color.opposite and board.get_piece(Position(piece.position.row+1, piece.position.col+1)) != None:
                    if board.get_piece(Position(piece.position.row+1, piece.position.col+1)).color == color and (board.get_piece(Position(piece.position.row+2, piece.position.col+2)) == None):
                        boardStateValue -= 1
            if piece.position.row+2<=7 and piece.position.col-2>=0:
                if piece.color == color.opposite and board.get_piece(Position(piece.position.row+1, piece.position.col-1)) != None:
                    if board.get_piece(Position(piece.position.row+1, piece.position.col-1)).color == color and (board.get_piece(Position(piece.position.row+2, piece.position.col-2)) == None):
                        boardStateValue -= 1
            if piece.position.row-2>=0 and piece.position.col+2<=7:
                if piece.color == color.opposite and board.get_piece(Position(piece.position.row-1, piece.position.col+1)) != None:
                    if board.get_piece(Position(piece.position.row-1, piece.position.col+1)).color == color and (board.get_piece(Position(piece.position.row-2, piece.position.col+2)) == None):
                        boardStateValue -= 1
            if piece.position.row-2>=0 and piece.position.col-2>=0:
                if piece.color == color.opposite and board.get_piece(Position(piece.position.row-1, piece.position.col-1)) != None:
                    if board.get_piece(Position(piece.position.row-1, piece.position.col-1)).color == color and (board.get_piece(Position(piece.position.row-2, piece.position.col-2)) == None):
                        boardStateValue -= 1
            
        
        #Verificando se estão nas bordas
        for piece in allpieces:
            if piece.position.col == 0 or piece.position.col == 7:
                if piece.color == color:
                    boardStateValue += 0.3
                else:
                    boardStateValue -= 0.3

        #Verificando estão prestes a serem promovidas
        for piece in allpieces:
            if color == PlayerColor.RED:
                if piece.color == PlayerColor.RED and piece.position.row == 1 and piece.is_king() == False:
                    if piece.position.col-1 >= 0:
                        if board.get_piece(Position(piece.position.row-1, piece.position.col-1)) == None:
                            boardStateValue += 1.5
                    if piece.position.col+1 <= 7:
                        if board.get_piece(Position(piece.position.row-1, piece.position.col+1)) == None:
                            boardStateValue += 1.5
                if piece.color == PlayerColor.BLACK and piece.position.row == 6 and piece.is_king() == False:
                    if piece.position.col-1 >= 0:
                        if board.get_piece(Position(piece.position.row+1, piece.position.col-1)) == None:
                            boardStateValue -= 1.5
                    if piece.position.col+1 <= 7:
                        if board.get_piece(Position(piece.position.row+1, piece.position.col+1)) == None:
                            boardStateValue -= 1.5
            else:
                if piece.color == PlayerColor.RED and piece.position.row == 1 and piece.is_king() == False:
                    if piece.position.col-1 >= 0:
                        if board.get_piece(Position(piece.position.row-1, piece.position.col-1)) == None:
                            boardStateValue -= 1.5
                    if piece.position.col+1 <= 7:
                        if board.get_piece(Position(piece.position.row-1, piece.position.col+1)) == None:
                            boardStateValue -= 1.5
                if piece.color == PlayerColor.BLACK and piece.position.row == 6 and piece.is_king() == False:
                    if piece.position.col-1 >= 0:
                        if board.get_piece(Position(piece.position.row+1, piece.position.col-1)) == None:
                            boardStateValue += 1.5
                    if piece.position.col+1 <= 7:
                        if board.get_piece(Position(piece.position.row+1, piece.position.col+1)) == None:
                            boardStateValue += 1.5

        # Retornar resultado
        return boardStateValue
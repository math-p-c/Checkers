"""Avaliador simples baseado em contagem de peças ameaçadas."""

from core.position import Position
from .base_evaluator import BaseEvaluator
from ..board_state import BoardState
from ..enums import PlayerColor


class PiecesThreatenedEvaluator(BaseEvaluator):
    """
    Avaliador que conta peças que, em um determinado estado, estarão ameaçadas.
    """

    def evaluate(self, board: BoardState, color: PlayerColor) -> float:
        """
        Avalia a posição das peças e checa se há alguma ameaça em potencial.

        Args:
            board: Estado atual do tabuleiro
            color: Cor do jogador a avaliar

        Returns:
            Diferença de pontos (peças do jogador nas laterais - peças do adversário nas laterais)
        """

        allpieces = board.get_all_pieces()

        boardStateValue = 0.0

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
        
        # Retornar resultado
        return boardStateValue
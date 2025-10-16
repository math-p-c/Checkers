"""Avaliador simples baseado em contagem de peças ameaçadas."""

from .base_evaluator import BaseEvaluator
from ..board_state import BoardState
from ..enums import PlayerColor


class PieceOnSidesEvaluator(BaseEvaluator):
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
            if piece.color == color and (board.get_piece(piece.position.row+1, piece.position.col+1).color == color.opposite and (board.get_piece(piece.position.row+2, piece.position.col+2) == None) and piece.position.row+2<8 and piece.position.col+2<8):
                boardStateValue += 1
            if piece.color == color and (board.get_piece(piece.position.row-1, piece.position.col+1).color == color.opposite and (board.get_piece(piece.position.row-2, piece.position.col+2) == None) and piece.position.row-2>=0 and piece.position.col+2<8):
                boardStateValue += 1
            if piece.color == color and (board.get_piece(piece.position.row+1, piece.position.col-1).color == color.opposite and (board.get_piece(piece.position.row+2, piece.position.col-2) == None) and piece.position.row+2<8 and piece.position.col-2>=0):
                boardStateValue += 1
            if piece.color == color and (board.get_piece(piece.position.row-1, piece.position.col-1).color == color.opposite and (board.get_piece(piece.position.row-2, piece.position.col-2) == None) and piece.position.row-2>=0 and piece.position.col-2>=0):
                boardStateValue += 1
            
            if piece.color == color.opposite and (board.get_piece(piece.position.row+1, piece.position.col+1).color == color and (board.get_piece(piece.position.row+2, piece.position.col+2) == None) and piece.position.row+2<8 and piece.position.col+2<8):
                boardStateValue -= 1
            if piece.color == color.opposite and (board.get_piece(piece.position.row-1, piece.position.col+1).color == color and (board.get_piece(piece.position.row-2, piece.position.col+2) == None) and piece.position.row-2>=0 and piece.position.col+2<8):
                boardStateValue -= 1
            if piece.color == color.opposite and (board.get_piece(piece.position.row+1, piece.position.col-1).color == color and (board.get_piece(piece.position.row+2, piece.position.col-2) == None) and piece.position.row+2<8 and piece.position.col-2>=0):
                boardStateValue -= 1
            if piece.color == color.opposite and (board.get_piece(piece.position.row-1, piece.position.col-1).color == color and (board.get_piece(piece.position.row-2, piece.position.col-2) == None) and piece.position.row-2>=0 and piece.position.col-2>=0):
                boardStateValue -= 1
        
        # Retornar resultado
        return boardStateValue
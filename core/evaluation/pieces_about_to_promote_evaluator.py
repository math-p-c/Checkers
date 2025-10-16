"""Avaliador se peças estão prestes a ser promovidas."""

from .base_evaluator import BaseEvaluator
from ..board_state import BoardState
from ..enums import PlayerColor


class PieceAboutToPromoteEvaluator(BaseEvaluator):
    """
    Avaliador que conta peças nas penultimas linhas do tabuleiro.
    """

    def evaluate(self, board: BoardState, color: PlayerColor) -> float:
        """
        Avalia a posição das peças nas penultimas linhas.

        Args:
            board: Estado atual do tabuleiro
            color: Cor do jogador a avaliar

        Returns:
            Diferença de pontos (peças do jogador nas penultimas linhas - peças do adversário nas penultimas linhas)
        """

        allpieces = board.get_all_pieces()

        boardStateValue = 0.0

        for piece in allpieces:
            if color == PlayerColor.RED:
                if piece.color == PlayerColor.RED and piece.position.row == 1 and piece.is_king() == False and (board.get_piece(piece.position.row-1, piece.position.col-1) == None or board.get_piece(piece.position.row-1, piece.position.col+1) == None):
                    boardStateValue += 1.5
                if piece.color == PlayerColor.BLACK and piece.position.row == 6 and piece.is_king() == False and (board.get_piece(piece.position.row+1, piece.position.col-1) == None or board.get_piece(piece.position.row+1, piece.position.col+1) == None):
                    boardStateValue -= 1.5
            else:
                if piece.color == PlayerColor.BLACK and piece.position.row == 6 and piece.is_king() == False and (board.get_piece(piece.position.row+1, piece.position.col-1) == None or board.get_piece(piece.position.row+1, piece.position.col+1) == None):
                    boardStateValue += 1.5
                if piece.color == PlayerColor.RED and piece.position.row == 1 and piece.is_king() == False and (board.get_piece(piece.position.row-1, piece.position.col-1) == None or board.get_piece(piece.position.row-1, piece.position.col+1) == None):
                    boardStateValue -= 1.5

        # Retornar diferença
        return boardStateValue
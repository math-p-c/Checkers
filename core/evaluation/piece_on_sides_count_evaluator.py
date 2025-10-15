"""Avaliador simples baseado em contagem de peças nas laterais."""

from .base_evaluator import BaseEvaluator
from ..board_state import BoardState
from ..enums import PlayerColor


class PieceOnSidesEvaluator(BaseEvaluator):
    """
    Avaliador que conta peças nas colunas laterais do tabuleiro (0 e 7).
    """

    def evaluate(self, board: BoardState, color: PlayerColor) -> float:
        """
        Avalia a posição das peças nas laterais.

        Args:
            board: Estado atual do tabuleiro
            color: Cor do jogador a avaliar

        Returns:
            Diferença de pontos (peças do jogador nas laterais - peças do adversário nas laterais)
        """

        allpieces = board.get_all_pieces()

        boardStateValue = 0.0

        for piece in allpieces:
            if piece.position.col == 0 or piece.position.col == 7:
                if piece.color == color:
                    boardStateValue += 0.3
                else:
                    boardStateValue -= 0.3

        # Retornar diferença
        return boardStateValue
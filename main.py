"""Arquivo principal do jogo de damas."""

import pygame
import sys
from typing import Optional
from config import WindowConfig, BoardConfig, ColorsConfig, UIElementConfig
from core.enums import PlayerColor, GameMode, Difficulty
from core.game_manager import GameManager
from core.position import Position
from renderers.board_renderer import BoardRenderer
from renderers.piece_renderer import PieceRenderer
from ui.mode_selector import ModeSelector
from ui.difficulty_selector import DifficultySelector
from ui.control_panel import ControlPanel


class CheckersWindow:
    """Janela principal do jogo de damas."""

    def __init__(self):
        """Inicializa a aplicação."""
        pygame.init()
        pygame.font.init()

        # Configurar janela
        self.width = WindowConfig.WIDTH
        self.height = WindowConfig.HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(WindowConfig.TITLE)

        # Clock para FPS
        self.clock = pygame.time.Clock()
        self.running = True

        # Criar gerenciador do jogo
        self.game_manager = GameManager(GameMode.HUMAN_VS_AI, Difficulty.MEDIUM)

        # Criar renderizadores
        self.board_renderer = BoardRenderer(self.screen)
        self.piece_renderer = PieceRenderer(self.screen)

        # Criar componentes UI
        # Layout: Coluna esquerda com seletores e controles
        left_column_x = 20
        # Largura dos botões: do x=20 até 20px antes do tabuleiro (que está em x=260)
        button_width = BoardConfig.BOARD_X - 20 - left_column_x  # 260 - 20 - 20 = 220

        # Alinhar com a borda superior do tabuleiro
        selector_y_start = BoardConfig.BOARD_Y

        self.mode_selector = ModeSelector(
            x=left_column_x,
            y=selector_y_start,
            width=button_width,
            on_mode_change=self._on_mode_change
        )

        # Espaçamento uniforme entre grupos de botões
        button_group_spacing = 30

        # Posição do difficulty selector: após 3 botões de modo + espaço
        difficulty_y = selector_y_start + 3 * UIElementConfig.SELECTOR_BUTTON_HEIGHT + button_group_spacing

        self.difficulty_selector = DifficultySelector(
            x=left_column_x,
            y=difficulty_y,
            width=button_width,
            on_difficulty_change=self._on_difficulty_change
        )

        # Posição do control panel: após difficulty + mesmo espaço
        control_y = difficulty_y + 3 * UIElementConfig.SELECTOR_BUTTON_HEIGHT + button_group_spacing

        self.control_panel = ControlPanel(
            x=left_column_x,
            y=control_y,
            width=button_width,
            on_reset=self._on_reset_clicked
        )

    def _on_mode_change(self, mode: GameMode) -> None:
        """
        Callback para mudança de modo de jogo.

        Args:
            mode: Novo modo de jogo
        """
        print(f"Modo alterado para: {mode.value}")
        self.game_manager.set_game_mode(mode)
        self.difficulty_selector.update_visibility(mode)

    def _on_difficulty_change(self, difficulty: Difficulty) -> None:
        """
        Callback para mudança de dificuldade.

        Args:
            difficulty: Nova dificuldade
        """
        print(f"Dificuldade alterada para: {difficulty.value}")
        self.game_manager.set_difficulty(difficulty)

    def _on_reset_clicked(self) -> None:
        """Callback para quando clicar em "Reiniciar"."""
        self.game_manager.reset_game()
        print("Jogo reiniciado")

    def _handle_board_click(self, event: pygame.event.Event) -> None:
        """
        Processa clique no tabuleiro.

        Args:
            event: Evento do pygame
        """
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return

        # Verificar se é turno humano
        if not self.game_manager.is_human_turn():
            return

        # Obter posição clicada
        mouse_x, mouse_y = event.pos
        square = BoardConfig.get_square_from_pos(mouse_x, mouse_y)

        if square is None:
            return

        row, col = square
        clicked_pos = Position(row, col)

        # Lógica de seleção e movimento
        if self.game_manager.selected_piece is None:
            # Nenhuma peça selecionada: tentar selecionar
            if self.game_manager.select_piece(clicked_pos):
                print(f"Peça selecionada em {clicked_pos}")
        else:
            # Peça já selecionada
            if clicked_pos == self.game_manager.selected_piece:
                # Clicou na mesma peça: desselecionar
                self.game_manager.deselect_piece()
                print("Peça desselecionada")
            elif self.game_manager.make_human_move(clicked_pos):
                # Movimento executado com sucesso
                print(f"Movimento para {clicked_pos}")
            else:
                # Tentar selecionar outra peça
                self.game_manager.deselect_piece()
                if self.game_manager.select_piece(clicked_pos):
                    print(f"Peça selecionada em {clicked_pos}")

    def handle_events(self) -> None:
        """Processa eventos do pygame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Processar eventos dos componentes UI
            self.mode_selector.handle_event(event)
            self.difficulty_selector.handle_event(event)
            self.control_panel.handle_event(event)

            # Processar cliques no tabuleiro
            self._handle_board_click(event)

    def update(self) -> None:
        """Atualiza lógica da aplicação."""
        current_time = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()

        # Atualizar gerenciador de estado (processa IA se necessário)
        self.game_manager.update(current_time)

        # Atualizar componentes UI
        self.mode_selector.update(mouse_pos)
        self.difficulty_selector.update(mouse_pos)
        self.control_panel.update(mouse_pos)

    def render(self) -> None:
        """Renderiza todos os elementos na tela."""
        # Limpar tela
        self.screen.fill(ColorsConfig.BACKGROUND)

        # Renderizar tabuleiro
        self.board_renderer.render(
            self.game_manager.board,
            self.game_manager.selected_piece,
            self.game_manager.valid_moves_for_selected
        )

        # Renderizar peças
        self.piece_renderer.render_all_pieces(self.game_manager.board)

        # Renderizar componentes UI
        self.mode_selector.render(self.screen)
        self.difficulty_selector.render(self.screen)
        self.control_panel.render(self.screen)

        # Renderizar info de status
        self._render_status_info()

        # Renderizar mensagem se IA estiver pensando
        if self.game_manager.is_ai_thinking:
            self._render_thinking_message()

        # Atualizar tela
        pygame.display.flip()

    def _render_status_info(self) -> None:
        """Renderiza informações de status do jogo."""
        # Painel de status à esquerda do tabuleiro, abaixo do control panel
        panel_x = 20
        panel_width = BoardConfig.BOARD_X - 20 - 20  # Mesma largura dos botões
        panel_height = 160

        # Calcular posição Y após o control panel
        control_y = self.control_panel.panel_y
        control_height = self.control_panel.panel_height
        panel_y = control_y + control_height

        # Fontes
        font_title = pygame.font.Font(None, UIElementConfig.PANEL_TITLE_FONT_SIZE)
        font_text = pygame.font.Font(None, UIElementConfig.PANEL_TEXT_FONT_SIZE)

        # Renderizar título acima do painel, alinhado à esquerda
        title_surface = font_title.render("STATUS", True, ColorsConfig.TEXT)
        title_rect = title_surface.get_rect(topleft=(panel_x, panel_y - 20))
        self.screen.blit(title_surface, title_rect)

        # Desenhar fundo do painel
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, ColorsConfig.PANEL_BACKGROUND, panel_rect)
        pygame.draw.rect(self.screen, ColorsConfig.PANEL_BORDER, panel_rect, 2)

        # Turno atual
        y_offset = panel_y + 15
        player_name = "Vermelho" if self.game_manager.current_player == PlayerColor.RED else "Preto"
        player_color = ColorsConfig.TURN_RED if self.game_manager.current_player == PlayerColor.RED else ColorsConfig.TURN_BLACK

        turno_text = font_text.render(f"Turno: {player_name}", True, player_color)
        turno_rect = turno_text.get_rect(topleft=(panel_x + 15, y_offset))
        self.screen.blit(turno_text, turno_rect)

        # Peças restantes
        y_offset += 30
        red_pieces = self.game_manager.board.count_pieces(PlayerColor.RED)
        black_pieces = self.game_manager.board.count_pieces(PlayerColor.BLACK)

        pieces_text = font_text.render(f"Vermelhas: {red_pieces}", True, ColorsConfig.TURN_RED)
        pieces_rect = pieces_text.get_rect(topleft=(panel_x + 15, y_offset))
        self.screen.blit(pieces_text, pieces_rect)

        y_offset += 25
        pieces_text = font_text.render(f"Pretas: {black_pieces}", True, ColorsConfig.TURN_BLACK)
        pieces_rect = pieces_text.get_rect(topleft=(panel_x + 15, y_offset))
        self.screen.blit(pieces_text, pieces_rect)

        # Status do jogo
        y_offset += 35
        status_text = ""
        status_color = ColorsConfig.TEXT

        if self.game_manager.game_status.value == "RED_WINS":
            status_text = "VERMELHO VENCEU!"
            status_color = ColorsConfig.TURN_RED
        elif self.game_manager.game_status.value == "BLACK_WINS":
            status_text = "PRETO VENCEU!"
            status_color = ColorsConfig.TURN_BLACK
        elif self.game_manager.game_status.value == "DRAW":
            status_text = "EMPATE!"
            status_color = ColorsConfig.TEXT

        if status_text:
            status_surface = font_title.render(status_text, True, status_color)
            status_rect = status_surface.get_rect(center=(panel_x + panel_width // 2, y_offset))
            self.screen.blit(status_surface, status_rect)

    def _render_thinking_message(self) -> None:
        """Renderiza mensagem de IA pensando."""
        font = pygame.font.Font(None, 24)
        text_surface = font.render("IA está pensando...", True, ColorsConfig.TEXT_SECONDARY)
        text_rect = text_surface.get_rect(
            center=(BoardConfig.BOARD_X + BoardConfig.BOARD_SIZE // 2, BoardConfig.BOARD_Y + BoardConfig.BOARD_SIZE + 25)
        )
        self.screen.blit(text_surface, text_rect)

    def run(self) -> None:
        """Loop principal do jogo."""
        while self.running:
            # Processar eventos
            self.handle_events()

            # Atualizar
            self.update()

            # Renderizar
            self.render()

            # Manter FPS
            self.clock.tick(WindowConfig.FPS)

        # Encerrar pygame
        pygame.quit()
        sys.exit()


def main():
    """Função principal."""
    game = CheckersWindow()
    game.run()


if __name__ == "__main__":
    main()

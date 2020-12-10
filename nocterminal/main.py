from __future__ import annotations

from managers.game_manager import GameManager


def main() -> None:
    game_manager = GameManager()
    game_manager.loop()


if __name__ == '__main__':
    main()
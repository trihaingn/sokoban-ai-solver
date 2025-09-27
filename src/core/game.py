import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from collections import deque

class SokobanGame:
    __MOVES = ((-1, 0), (1, 0), (0, -1), (0, 1))
    __TILE_SIZE = 64
    def __init__(self, player, crates, obstacles, targets, bound):
        self.player = player
        self.crates = crates
        self.obstacles = obstacles
        self.targets = targets
        self.bound = bound
        
    def find_path(self, tpos):
        ppos = self.player

        if ppos == tpos:
            return []
        
        queue = deque([(ppos, [ppos])])
        visited = {ppos}

        def is_valid_pos(pos):
            if pos in self.obstacles or pos in self.crates:
                return False
            
            return True

        while queue:
            cpos, path = queue.popleft()
            cx, cy = cpos

            for dx, dy in self.__MOVES:
                next_pos = (cx + dx, cy + dy)
                if (next_pos not in visited and is_valid_pos(next_pos)):
                    new_path = path + [next_pos]
                    if next_pos == tpos:
                        return new_path[1:]
                    
                    visited.add(next_pos)
                    queue.append((next_pos, new_path))
        
        return []  # No path found

    def perform_move(self, pmove, cmove = None):
        self.player = pmove
        if cmove:
            self.crates.remove(pmove)
            self.crates.add(cmove)

    def _get_object_count(self, pos):
        return int(pos == self.player) + int(pos in self.crates) + int(pos in self.obstacles) + int(pos in self.targets)
    
    def _load_image(self, filename):
        asset_path = os.path.join("assets", "images", filename)
        return pygame.transform.scale(pygame.image.load(asset_path).convert(), (self.__TILE_SIZE, self.__TILE_SIZE))

    def rendering(self, moves):
        pygame.init()
        pygame.display.set_caption("Sokoban Game")

        # Fix bounds: bound is (maxX, maxY)
        maxX, maxY = self.bound
        gamew = maxY * self.__TILE_SIZE
        gameh = maxX * self.__TILE_SIZE

        gameSurface = pygame.Surface((gamew, gameh))

        info = pygame.display.Info()
        width, height = info.current_w, info.current_h
        screen = pygame.display.set_mode((width, height))

        wall_img = self._load_image("wall.png") 
        box_img = self._load_image("box.png")
        player_img = self._load_image("player.png")
        box_on_target_img = self._load_image("box_on_target.png")
        target_img = self._load_image("target.png")
        space_img = self._load_image("space.png")

        pygame.time.wait(2000)

        for move in moves:
            # Fix move format: (player_pos_before_push, crate_current_pos, crate_new_pos)
            tppos, nppos, ncpos = move

            # Player needs to move to tppos to push the crate
            must_move = self.find_path(tppos) + [nppos]

            for mmove in must_move:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                if mmove is not None:
                    if mmove != nppos:
                        self.perform_move(mmove)
                    else:
                        self.perform_move(mmove, ncpos)

                gameSurface.fill((0,0,0))
                
                # Fix coordinate loops: use actual grid bounds
                for r in range(maxX):
                    for c in range(maxY):
                        pos = (r, c)
                        # Convert grid to screen coordinates
                        screen_x = c * self.__TILE_SIZE
                        screen_y = r * self.__TILE_SIZE
                        game_pos = (screen_x, screen_y)

                        obj_cnt = self._get_object_count(pos)

                        # Draw space case
                        if obj_cnt == 0:
                            gameSurface.blit(space_img, game_pos)

                        # Single object case
                        elif obj_cnt == 1:
                            if pos in self.obstacles:
                                gameSurface.blit(wall_img, game_pos)
                            elif pos in self.crates:
                                gameSurface.blit(box_img, game_pos)
                            elif pos == self.player:
                                gameSurface.blit(player_img, game_pos)
                            elif pos in self.targets:
                                gameSurface.blit(target_img, game_pos)
                        
                        elif obj_cnt == 2:
                            if pos in self.crates and pos in self.targets:
                                gameSurface.blit(box_on_target_img, game_pos)
                            elif pos == self.player and pos in self.targets:
                                gameSurface.blit(player_img, game_pos)
                
                screen.fill((0,0,0))
                offsetX, offsetY = (width - gamew) // 2, (height - gameh) // 2

                screen.blit(gameSurface, (offsetX, offsetY))

                pygame.display.flip()
                pygame.time.wait(200)
        
        pygame.time.wait(2000)
        pygame.quit()
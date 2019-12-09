import json
import argparse
import pygame

from maze import MazeGame

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", default="config.json", help="game configuration file")
parser.add_argument("-a", "--auto", default=False ,action='store_true', help="solve maze automatically")


def main(config_path, autoplay):

    # Load game configuration file
    with open(config_path, "r") as f:
        config = json.loads(f.read())

    # Setup game environment
    game = MazeGame(config['maze']['path'], config['maze']['unit'])
    screen = pygame.display.set_mode(game.maze.image.get_size())
    player = game.player
    obstacle_group = game.obstacle_group

    # Play game until player get to the exit point
    while not game.finish():
        # Event checking
        for event in pygame.event.get():
            pass

        # Key held down
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.up()
        elif keys[pygame.K_DOWN]:
            player.down()
        elif keys[pygame.K_RIGHT]:
            player.right()
        elif keys[pygame.K_LEFT]:
            player.left()
        else:
            pass

        # Check collision
        if len(pygame.sprite.spritecollide(player, obstacle_group, False)) != 0 :
            player.stepback()

        # Update screen
        screen.blit(game.maze.image, game.maze.rect)
        screen.blit(player.image, player.rect)
        pygame.display.flip()
        pygame.time.delay(100)

if __name__ == "__main__":
    args = vars(parser.parse_args())
    main(args['config'], args['auto'])

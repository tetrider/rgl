import libtcodpy as libtcod

from enum import Enum, auto


class RenderOrder(Enum):
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()


def render_all(con, entities, player, game_map, fov_map, fov_recompute,
               screen_width, screen_height, colors):
    # Draw all tiles in the game map
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight
                color = None
                if visible:
                    if wall:
                        color = 'light_wall'
                    else:
                        color = 'light_ground'
                    game_map.tiles[x][y].explored = True
                elif game_map.tiles[x][y].explored:
                    if wall:
                        color = 'dark_wall'
                    else:
                        color = 'dark_ground'
                if color:
                    libtcod.console_set_char_background(con, x, y,
                                                        colors.get(color),
                                                        libtcod.BKGND_SET)
    # Draw all entities in the list
    entities_in_render_order = sorted(entities,
                                      key=lambda x: x.render_order.value)
    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map)

    libtcod.console_set_default_foreground(con, libtcod.white)
    libtcod.console_print_ex(con, 1, screen_height - 2, libtcod.BKGND_NONE,
                             libtcod.LEFT,
                             f'HP: {player.fighter.hp}/{player.fighter.max_hp}'
                             )
    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char,
                                 libtcod.BKGND_NONE)


def clear_entity(con, entity):
    # erase the character that represents this object
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)

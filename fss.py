a = [4, 5, 3]
print(a.__class__.__name__ )

# def execute_command(command, *args, character=player):
#     command = command.strip()
#     command_args = []
#     print(command, args)
#     for i in range(len(args)):
#         command_args.append(args[i].strip())
#     if command == "get":
#         try:
#             item = all_items[command_args[0]]
#             count = int(command_args[1])
#             if len(command_args) > 2:
#                 func = command_args[2]
#             Player_stats.inventory.extend([item for _ in range(count)])
#
#             DialogWindow.set_dialog_text(f"You got a {item.name}")
#             dialog_menu.open()
#
#         except KeyError:
#             print(f"There no item {command_args[0]}")
#         except ValueError:
#             print(f"parameter count - wrong")
#
#     if command == "door":
#         door_num = command_args[0]
#         location = command_args[1]
#         direction = command_args[2].lower()
#         try:
#             if direction not in ("right", "left", "down", "up"):
#                 raise CustomException(f"Theres no direction {direction}")
#             location_map.load_level(location)
#
#             f = False
#             for obj in walls:
#                 for property in obj.properties:
#                     if property[0] == "door" and property[1] == door_num:
#                         if direction == "down":
#                             pos = obj.rect.midbottom
#                             character.stand(DOWN)
#                             character.move_by_hit_polygon(pos[0] - character.hit_polygon.width / 2,
#                                                               pos[1] + location_map.tilewidth)
#                         elif direction == "up":
#                             pos = obj.rect.midtop
#                             character.stand(UP)
#                             character.move_by_hit_polygon(pos[0] - character.hit_polygon.width / 2,
#                                                               pos[1] - character.hit_polygon.height - location_map.tilewidth)
#                         elif direction == "left":
#                             pos = obj.rect.midleft
#                             character.stand(LEFT)
#                             character.move_by_hit_polygon(pos[0] - character.hit_polygon.width - location_map.tilewidth,
#                                                               pos[1] - character.hit_polygon.height / 2)
#                         elif direction == "right":
#                             pos = obj.rect.midright
#                             character.stand(RIGHT)
#                             character.move_by_hit_polygon(pos[0] + location_map.tilewidth,
#                                                               pos[1] - character.hit_polygon.height / 2)
#                         return None

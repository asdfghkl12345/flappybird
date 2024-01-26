import pygame
import tools as T
W,H = 288,512
FPS = 35
bird_x = W * 0.2
bird_y = H * 0.44
floor_y = H - T.IMAGES['floor'].get_height()
guide_x = (W - T.IMAGES['guide'].get_width())/2
guide_y = W * 0.84
guide1_x = (W - T.IMAGES['guide1'].get_width())/2
guide1_y = W * 0.5
guide2_x = (W - T.IMAGES['guide2'].get_width())/2
guide2_y = W * 0.2
gameover_x = (W - T.IMAGES['gameover'].get_width())/2
gameover_y = (floor_y - T.IMAGES['gameover'].get_height())/3
floor_gap = T.IMAGES['floor'].get_width() - W
end_x = (W-T.IMAGES['end'].get_width())/2
end_y = (H-T.IMAGES['end'].get_height())/2
new_x = W/1.75
new_y = H/1.95
start_x = (W-T.IMAGES['start'].get_width())/2
start_y = (H-T.IMAGES['start'].get_height())/1.2
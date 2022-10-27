import cv2
import numpy as np

WINDOW_NAME = "AlgoBlockDoku"

COLOR_BG = np.array([181, 228, 255])
COLOR_PIECES_PART = np.array([231, 248, 255])
COLOR_PIECE = np.array([19, 69, 139])
COLOR_BLACK = np.array([0, 0, 0])
COLOR_GRAY = np.array([153, 153, 192])

BLOCK_SIZE_PIXEL = 50
LINE_SIZE_PIXEL = 3
SEPARATOR_SIZE_PIXEL = 25
PIECES_PART_HEIGHT_PIXEL = 3 * BLOCK_SIZE_PIXEL

PIECE_BLOCK_SIZE_PIXEL = int(BLOCK_SIZE_PIXEL * 0.599)
PIECE_LINE_SIZE_PIXEL = int(LINE_SIZE_PIXEL - 1)


def color_mat_part(mat, i, j, h, w, c):
    mat[i: i + h, j: j + w, 0] = c[0]
    mat[i: i + h, j: j + w, 1] = c[1]
    mat[i: i + h, j: j + w, 2] = c[2]


def get_start_coords_of_cell( i, j):
    start_i = i * (BLOCK_SIZE_PIXEL + LINE_SIZE_PIXEL) + i // 3 * LINE_SIZE_PIXEL
    start_j = j * (BLOCK_SIZE_PIXEL + LINE_SIZE_PIXEL) + j // 3 * LINE_SIZE_PIXEL
    return start_i, start_j


def get_image_of_piece(piece):
    img = np.zeros((PIECES_PART_HEIGHT_PIXEL, PIECES_PART_HEIGHT_PIXEL, 3), np.uint8)
    color_mat_part(img, 0, 0, PIECES_PART_HEIGHT_PIXEL, PIECES_PART_HEIGHT_PIXEL, COLOR_PIECES_PART)
    offset_i = (5 - piece.shape[0]) // 2
    offset_j = (5 - piece.shape[1]) // 2
    for i in range(piece.shape[0]):
        for j in range(piece.shape[1]):
            if piece[i, j] == 0:
                continue
            start_i = (i + offset_i) * (PIECE_BLOCK_SIZE_PIXEL + PIECE_LINE_SIZE_PIXEL)
            start_j = (j + offset_j) * (PIECE_BLOCK_SIZE_PIXEL + PIECE_LINE_SIZE_PIXEL)
            c = COLOR_PIECE if piece[i, j] == 1 else COLOR_GRAY
            color_mat_part(img, start_i, start_j, PIECE_BLOCK_SIZE_PIXEL, PIECE_BLOCK_SIZE_PIXEL, c)
            if i != piece.shape[0] - 1 and abs(piece[i, j] + piece[i + 1, j]) == 2:
                color_mat_part(img, start_i + PIECE_BLOCK_SIZE_PIXEL, start_j, PIECE_LINE_SIZE_PIXEL, PIECE_BLOCK_SIZE_PIXEL, COLOR_BLACK)
            if j != piece.shape[1] - 1 and abs(piece[i, j] + piece[i, j + 1]) == 2:
                color_mat_part(img, start_i, start_j + PIECE_BLOCK_SIZE_PIXEL, PIECE_BLOCK_SIZE_PIXEL, PIECE_LINE_SIZE_PIXEL, COLOR_BLACK)
    return img


class Visualizer:
    def __init__(self):
        cv2.namedWindow(WINDOW_NAME)
        cv2.moveWindow(WINDOW_NAME, 0, 0)
        self.canvas = np.zeros((BLOCK_SIZE_PIXEL * 9 + LINE_SIZE_PIXEL * 10 + SEPARATOR_SIZE_PIXEL + PIECES_PART_HEIGHT_PIXEL,
                                BLOCK_SIZE_PIXEL * 9 + LINE_SIZE_PIXEL * 10,
                                3), np.uint8)

    def reset_canvas(self):
        self.canvas *= 0
        for i in range(9):
            for j in range(9):
                start_i, start_j = get_start_coords_of_cell(i, j)
                color_mat_part(self.canvas, start_i, start_j, BLOCK_SIZE_PIXEL, BLOCK_SIZE_PIXEL, COLOR_BG)
        color_mat_part(self.canvas, self.canvas.shape[0] - PIECES_PART_HEIGHT_PIXEL - 1, 0,
                       PIECES_PART_HEIGHT_PIXEL, self.canvas.shape[1] - 1, COLOR_PIECES_PART)

    def show_state(self, field, pieces, wait=0):
        self.reset_canvas()
        for i in range(9):
            for j in range(9):
                if field[i, j] != 0:
                    start_i, start_j = get_start_coords_of_cell(i, j)
                    c = COLOR_PIECE if field[i, j] == 1 else COLOR_GRAY
                    color_mat_part(self.canvas, start_i, start_j, BLOCK_SIZE_PIXEL, BLOCK_SIZE_PIXEL, c)
        for i in range(3):
            if pieces[i] is not None:
                img = get_image_of_piece(pieces[i])
                self.canvas[-1 * PIECES_PART_HEIGHT_PIXEL:,
                            i * PIECES_PART_HEIGHT_PIXEL: (i + 1) * PIECES_PART_HEIGHT_PIXEL] = img
        cv2.imshow(WINDOW_NAME, self.canvas)
        cv2.waitKey(wait)
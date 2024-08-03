import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time

# 初期設定
pygame.init()
display = (1600, 600)  # 幅を2倍にして、左右の画像を並べて表示する
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# 視点の設定
def setup_viewpoint(offset_x):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0] / 2) / display[1], 0.1, 50.0)  # 片側の視点のためにアスペクト比を調整
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(offset_x, 0.0, -20)  # 視点を左右にオフセット

# 棒の描画
def draw_cube(x, y, z):
    glBegin(GL_QUADS)
    glColor3fv((1, 0, 0))  # 赤色
    glVertex3f(x - 0.4, y - 4, z)
    glVertex3f(x + 0.4, y - 4, z)
    glVertex3f(x + 0.4, y + 4, z)
    glVertex3f(x - 0.4, y + 4, z)
    glEnd()

# メインループ
def main():
    start_time = time.time()
    central_pos = -10
    direction = 1  # 初期方向（前進）
    duration = 4.0  # 片道4秒で移動
    distance = 8.0  # 移動距離（-18から-2まで）
    speed = distance / duration  # 毎秒の移動距離
    clock = pygame.time.Clock()  # フレームレート制御用のクロックオブジェクト

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    elapsed_time = time.time() - start_time
                    accuracy = abs(central_pos + 10)  # 基準位置はz = -10
                    print(f"反応時間: {elapsed_time:.2f}秒, 精度: {accuracy:.2f}単位")
                    pygame.time.wait(2000)
                    running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 左目の視点
        setup_viewpoint(-0.1)
        # 左と右の棒
        draw_cube(-2, 0, -10)
        draw_cube(2, 0, -10)
        # 中央の棒
        draw_cube(0, 0, central_pos)
        glViewport(0, 0, display[0] // 2, display[1])

        # 右目の視点
        setup_viewpoint(0.1)
        # 左と右の棒
        draw_cube(-2, 0, -10)
        draw_cube(2, 0, -10)
        # 中央の棒
        draw_cube(0, 0, central_pos)
        glViewport(display[0] // 2, 0, display[0] // 2, display[1])

        pygame.display.flip()

        # 棒の位置を更新
        delta_time = clock.tick(60) / 1000.0  # 経過時間を秒単位で取得
        central_pos += speed * direction * delta_time

        # 棒の方向を変更
        if central_pos > -2 or central_pos < -18:
            direction *= -1

    pygame.quit()

if __name__ == "__main__":
    main()

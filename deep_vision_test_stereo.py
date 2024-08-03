import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time
import random  # ランダム関数をインポート

# 初期設定
pygame.init()
display = (1600, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL | RESIZABLE)  # RESIZABLEフラグを追加

# フォントの設定
font = pygame.font.Font(None, 36)  # サイズ36のデフォルトフォント

# 初期の棒の高さと幅
cube_height = 30
initial_cube_width = random.uniform(0.5, 1.5)  # 初期の棒の幅をランダムに設定
central_cube_width = 1.0  # 真ん中の棒の幅は一定
background_color = (0, 0, 0)  # 初期の背景色は黒
cube_color = (0.5, 0.5, 0.5)  # 初期の棒の色は灰色
g_key_pressed = False  # 'g' キーが押されているかどうかを追跡するフラグ

# テキストの描画
def draw_text(text, position):
    glColor3fv((1, 1, 1))  # テキストの色を白に設定
    text_surface = font.render(text, True, (255, 255, 255))  # 白色でテキストを描画
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    width, height = text_surface.get_size()
    glRasterPos2f(position[0], position[1])
    glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

# 視点の設定
def setup_viewpoint(offset_x, width, height):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (width / 2) / height, 0.1, 50.0)  # 片側の視点のためにアスペクト比を調整
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(offset_x, 0.0, -20)  # 視点を左右にオフセット

# 棒の描画
def draw_cube(x, y, z, height, width):
    glBegin(GL_QUADS)
    glColor3fv(cube_color)  # 棒の色を設定
    # 上面
    glVertex3f(x - width, y - height / 2, z)
    glVertex3f(x + width, y - height / 2, z)
    glVertex3f(x + width, y + height / 2, z)
    glVertex3f(x - width, y + height / 2, z)
    glEnd()

# メインループ
def main():
    global cube_height, background_color, cube_color, g_key_pressed, initial_cube_width
    start_time = time.time()
    central_pos = -10
    direction = 1  # 初期方向（前進）
    duration = 8.0  # 片道8秒で移動
    distance = 8.0  # 移動距離（-18から-10まで）
    speed = distance / duration  # 毎秒の移動距離
    clock = pygame.time.Clock()  # フレームレート制御用のクロックオブジェクト
    width, height = display

    # 視点のオフセット（視差）を設定
    offset_x = 0.6  # 左右の視点間のズレを設定

    # 初期の両端の棒の太さを設定
    edge_cube_width = initial_cube_width

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == VIDEORESIZE:
                width, height = event.w, event.h
                pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL | RESIZABLE)
                glViewport(0, 0, width, height)
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                gluPerspective(45, (width / 2) / height, 0.1, 50.0)  # ビューポートのアスペクト比も更新
                glMatrixMode(GL_MODELVIEW)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    elapsed_time = time.time() - start_time
                    accuracy = abs(central_pos + 10)  # 基準位置はz = -10
                    print(f"反応時間: {elapsed_time:.2f}秒, 精度: {accuracy:.2f}単位")
                    pygame.time.wait(2000)
                    running = False
                elif event.key == pygame.K_s:
                    cube_height *= 1.5  # 縦のサイズを1.5倍に
                    print(f"棒の高さが {cube_height:.2f} に増加しました")
                elif event.key == pygame.K_x:
                    cube_height /= 1.5  # 縦のサイズを1/1.5に
                    print(f"棒の高さが {cube_height:.2f} に減少しました")
                elif event.key == pygame.K_g:
                    g_key_pressed = True
                elif event.key == pygame.K_b:
                    # 任意の追加操作（例: gキーが押されている時の動作をリセットする）
                    g_key_pressed = False
                    background_color = (0, 0, 0)  # 背景色を黒に
                    cube_color = (0.5, 0.5, 0.5)  # 棒の色を灰色に

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_g:
                    g_key_pressed = False
                    background_color = (0, 0, 0)  # 背景色を黒に
                    cube_color = (0.5, 0.5, 0.5)  # 棒の色を灰色に

        if g_key_pressed:
            distance_from_center = abs(central_pos + 10)
            if distance_from_center < 0.5:  # 元の範囲の1/2以内
                background_color = (0, 1, 0)  # 緑色
            elif distance_from_center < 1.0:  # 元の範囲
                background_color = (1, 1, 0)  # 黄色
            else:
                background_color = (1, 0, 0)  # 赤色
        else:
            background_color = (0, 0, 0)  # 背景色を黒に
            cube_color = (0.5, 0.5, 0.5)  # 棒の色を灰色に

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(*background_color, 1)  # 背景色を設定

        # 左目の視点
        glViewport(0, 0, width // 2, height)
        setup_viewpoint(-offset_x, width, height)
        draw_cube(-4, 0, -10, cube_height, edge_cube_width)  # 左端の棒
        draw_cube(4, 0, -10, cube_height, edge_cube_width)  # 右端の棒
        draw_cube(0, 0, central_pos, cube_height, central_cube_width)  # 中央の棒

        # 右目の視点
        glViewport(width // 2, 0, width // 2, height)
        setup_viewpoint(offset_x, width, height)
        draw_cube(-4, 0, -10, cube_height, edge_cube_width)  # 左端の棒
        draw_cube(4, 0, -10, cube_height, edge_cube_width)  # 右端の棒
        draw_cube(0, 0, central_pos, cube_height, central_cube_width)  # 中央の棒

        pygame.display.flip()

        # 棒の位置を更新
        delta_time = clock.tick(60) / 1000.0  # 経過時間を秒単位で取得
        central_pos += speed * direction * delta_time

        # 棒の方向を変更
        if central_pos > -2 or central_pos < -18:
            direction *= -1

    pygame.quit()

if __name__ == "__main__":
    print("操作説明:")
    print("  SPACE: テストを終了し、反応時間と精度を表示")
    print("  S: 棒の高さを1.5倍に増加")
    print("  X: 棒の高さを1/1.5に減少")
    print("  G: 背景色と棒の色を変更（緑色範囲: 0.5単位以内、黄色範囲: 1.0単位以内、赤色範囲: それ以外）")
    print("  B: Gキーの影響をリセットし、背景色を黒にし、棒の色を灰色に")
    main()

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time
import random  # ランダムモジュールをインポート

# 初期設定
pygame.init()
display = (1600, 600)
pygame.display.gl_set_attribute(GL_MULTISAMPLEBUFFERS, 1)
pygame.display.gl_set_attribute(GL_MULTISAMPLESAMPLES, 4)  # サンプル数
pygame.display.set_mode(display, DOUBLEBUF | OPENGL | RESIZABLE)  # RESIZABLEフラグを追加

# フォントの設定
font = pygame.font.Font(None, 36)  # サイズ36のデフォルトフォント

# 初期の円柱の高さと太さ
cylinder_height = 30
cylinder_radius = 0.5  # 初期の円柱の半径
background_color = (0, 0, 0)  # 初期の背景色は黒
cylinder_color = (0.5, 0.5, 0.5)  # 初期の円柱の色は灰色
g_key_pressed = False  # 'g' キーが押されているかどうかを追跡するフラグ

# 外側の円柱の太さ（起動時にランダムに設定）
outer_cylinder_radius = random.uniform(0.7, 1.5) * cylinder_radius

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

# 照明の設定
def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [10, 10, 10, 1])  # 光源の位置
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])  # 環境光
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.7, 0.7, 0.7, 1.0])  # 拡散光
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])  # 鏡面反射光

# 円柱の描画
def draw_cylinder(x, y, z, height, radius):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(90, 1, 0, 0)  # x軸を中心に90度回転
    glColor3fv(cylinder_color)
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)  # スムーズシェーディングを有効にする
    gluCylinder(quadric, radius, radius, height, 32, 32)
    gluDeleteQuadric(quadric)
    glPopMatrix()

# メインループ
def main():
    global cylinder_height, cylinder_radius, background_color, cylinder_color, g_key_pressed, outer_cylinder_radius
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

    # 照明を設定
    glEnable(GL_DEPTH_TEST)
    setup_lighting()

    print("操作説明:")
    print("スペースキー: 実行を停止し、反応時間と精度を表示")
    print("sキー: 円柱の高さを1.1倍にする")
    print("xキー: 円柱の高さを1/1.1にする")
    print("gキー: 円柱の色と背景色を変化させる")
    print("bキー: 初期状態に戻す")

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
                    running = False
                elif event.key == pygame.K_s:
                    cylinder_height *= 1.1  # 縦のサイズを1.5倍に
                    print(f"円柱の高さが {cylinder_height:.2f} に増加しました")
                elif event.key == pygame.K_x:
                    cylinder_height /= 1.1  # 縦のサイズを1/1.5に
                    print(f"円柱の高さが {cylinder_height:.2f} に減少しました")
                elif event.key == pygame.K_g:
                    g_key_pressed = True
                elif event.key == pygame.K_b:
                    g_key_pressed = False
                    background_color = (0, 0, 0)  # 背景色を黒に
                    cylinder_color = (0.5, 0.5, 0.5)  # 円柱の色を灰色に

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_g:
                    g_key_pressed = False
                    background_color = (0, 0, 0)  # 背景色を黒に
                    cylinder_color = (0.5, 0.5, 0.5)  # 円柱の色を灰色に

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
            cylinder_color = (0.5, 0.5, 0.5)  # 円柱の色を灰色に

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(*background_color, 1)  # 背景色を設定

        # 左目の視点
        glViewport(0, 0, width // 2, height)
        setup_viewpoint(-offset_x, width, height)
        draw_cylinder(-3, 20, -10, cylinder_height, outer_cylinder_radius)
        draw_cylinder(0, 20, central_pos, cylinder_height, cylinder_radius)
        draw_cylinder(3, 20, -10, cylinder_height, outer_cylinder_radius)

        # 右目の視点
        glViewport(width // 2, 0, width // 2, height)
        setup_viewpoint(offset_x, width, height)
        draw_cylinder(-3, 20, -10, cylinder_height, outer_cylinder_radius)
        draw_cylinder(0, 20, central_pos, cylinder_height, cylinder_radius)
        draw_cylinder(3, 20, -10, cylinder_height, outer_cylinder_radius)

        pygame.display.flip()

        # 円柱の位置を更新
        delta_time = clock.tick(60) / 1000.0  # 経過時間を秒単位で取得
        central_pos += speed * direction * delta_time

        # 円柱の方向を変更
        if central_pos > -2 or central_pos < -18:
            direction *= -1

    pygame.quit()

if __name__ == "__main__":
    main()

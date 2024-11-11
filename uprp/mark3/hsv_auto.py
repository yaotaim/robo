import cv2
import numpy as np
import pyrealsense2 as rs

clicked_hsv_values = []
collecting_hsv = False
red_hsv_range = None
blue_hsv_range = None
yellow_hsv_range = None

h_range=3
s_range=30
v_range=30

def onMouse(event, x, y, flags, params):
    global clicked_hsv_values, collecting_hsv
    color_image = params['color_image']
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_color_bgr = color_image[y, x]
        clicked_color_hsv = cv2.cvtColor(np.uint8([[clicked_color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
        
        # 収集モード中のみHSV値を追加
        if collecting_hsv:
            clicked_hsv_values.append(clicked_color_hsv)
            print(f"追加されたHSV値: {clicked_color_hsv}")

def calculate_hsv_range_red():
    global clicked_hsv_values, red_hsv_range
    if clicked_hsv_values:
        # Hの値を抽出して0～90の範囲と91～180の範囲に分割
        h_values_0_90 = [hsv for hsv in clicked_hsv_values if 0 <= hsv[0] <= 90]
        h_values_91_180 = [hsv for hsv in clicked_hsv_values if 91 <= hsv[0] <= 180]
        
        # 0～90の範囲での平均と範囲設定
        if h_values_0_90:
            hsv_mean_0_90 = np.mean(h_values_0_90, axis=0).astype(int)
            lower1 = np.clip(hsv_mean_0_90 - [h_range, s_range, v_range], [0, 0, 0], [179, 255, 255])
            upper1 = np.clip(hsv_mean_0_90 + [h_range, s_range, v_range], [0, 0, 0], [179, 255, 255])
        else:
            lower1 = upper1 = np.array([0, 0, 0])

        # 91～180の範囲での平均と範囲設定
        if h_values_91_180:
            hsv_mean_91_180 = np.mean(h_values_91_180, axis=0).astype(int)
            lower2 = np.clip(hsv_mean_91_180 - [h_range, s_range, v_range], [0, 0, 0], [179, 255, 255])
            upper2 = np.clip(hsv_mean_91_180 + [h_range, s_range, v_range], [0, 0, 0], [179, 255, 255])
        else:
            lower2 = upper2 = np.array([0, 0, 0])

        # 赤色のHSV範囲を設定
        red_hsv_range = (lower1, upper1, lower2, upper2)
        print(f"赤のHSV範囲: lower1={lower1.tolist()}, upper1={upper1.tolist()}, lower2={lower2.tolist()}, upper2={upper2.tolist()}")
    else:
        print("記録されたHSV値がありません。")
    
    # クリックしたHSV値リストをクリア
    clicked_hsv_values.clear()

def calculate_hsv_range_blue():
    global clicked_hsv_values, blue_hsv_range
    if clicked_hsv_values:
        # 収集したHSV値の平均を計算
        hsv_mean = np.mean(clicked_hsv_values, axis=0).astype(int)
        
        # 平均を中心に範囲を設定（H, S, Vのそれぞれに±5, ±30, ±30のマージンを適用）
        lower = np.clip(hsv_mean - [h_range, s_range, v_range], [0, 0, 0], [179, 255, 255])
        upper = np.clip(hsv_mean + [h_range, s_range, v_range], [0, 0, 0], [179, 255, 255])
        
        # 青色のHSV範囲を保存
        blue_hsv_range = (lower, upper)
        print(f"青のHSV範囲: lower={lower.tolist()}, upper={upper.tolist()}")
    else:
        print("記録されたHSV値がありません。")
    
    # クリックしたHSV値リストをクリア
    clicked_hsv_values.clear()

def calculate_hsv_range_yellow():
    global clicked_hsv_values, yellow_hsv_range
    if clicked_hsv_values:
        # 収集したHSV値の平均を計算
        hsv_mean = np.mean(clicked_hsv_values, axis=0).astype(int)
        
        # 平均を中心に範囲を設定（H, S, Vのそれぞれに±5, ±30, ±30のマージンを適用）
        lower = np.clip(hsv_mean - [h_range, s_range, v_range], [0, 0, 0], [179, 255, 255])
        upper = np.clip(hsv_mean + [h_range, s_range, v_range], [0, 0, 0], [179, 255, 255])
        
        # 黄色のHSV範囲を保存
        yellow_hsv_range = (lower, upper)
        print(f"黄のHSV範囲: lower={lower.tolist()}, upper={upper.tolist()}")
    else:
        print("記録されたHSV値がありません。")
    
    # クリックしたHSV値リストをクリア
    clicked_hsv_values.clear()

def display_hsv_ranges():
    global red_hsv_range, blue_hsv_range, yellow_hsv_range
    if red_hsv_range and blue_hsv_range and yellow_hsv_range:
        print(f"                lower_red1 = np.array([{', '.join(map(str, red_hsv_range[0]))}])")
        print(f"                upper_red1 = np.array([{', '.join(map(str, red_hsv_range[1]))}])")
        print(f"                lower_red2 = np.array([{', '.join(map(str, red_hsv_range[2]))}])")
        print(f"                upper_red2 = np.array([{', '.join(map(str, red_hsv_range[3]))}])")
        print(f" ")
        print(f"                lower_blue = np.array([{', '.join(map(str, blue_hsv_range[0]))}])")
        print(f"                upper_blue = np.array([{', '.join(map(str, blue_hsv_range[1]))}])")
        print(f" ")
        print(f"                lower_yellow = np.array([{', '.join(map(str, yellow_hsv_range[0]))}])")
        print(f"                upper_yellow = np.array([{', '.join(map(str, yellow_hsv_range[1]))}])")

    if not (red_hsv_range or blue_hsv_range or yellow_hsv_range):
        print("まだHSV範囲が計算されていません。")

def main():
    global collecting_hsv
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    pipeline.start(config)

    try:
        while True:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue

            color_image = np.asanyarray(color_frame.get_data())
            cv2.imshow('RealSense Camera', color_image)
            cv2.setMouseCallback('RealSense Camera', onMouse, {'color_image': color_image})

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('w'):  # 赤色の収集開始
                collecting_hsv = True
                clicked_hsv_values.clear()
                print("赤のHSV値の収集を開始しました。")
            elif key == ord('e'):  # 赤色の収集停止
                collecting_hsv = False
                calculate_hsv_range_red()
            elif key == ord('r'):  # 青色の収集開始
                collecting_hsv = True
                clicked_hsv_values.clear()
                print("青のHSV値の収集を始しました。")
            elif key == ord('t'):  # 青色の収集停止
                collecting_hsv = False
                calculate_hsv_range_blue()
            elif key == ord('y'):  # 黄色の収集開始
                collecting_hsv = True
                clicked_hsv_values.clear()
                print("黄のHSV値の収集を開始しました。")
            elif key == ord('u'):  # 黄色の収集停止
                collecting_hsv = False
                calculate_hsv_range_yellow()
            elif key == ord('i'):  # HSV範囲の表示
                display_hsv_ranges()

    finally:
        pipeline.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
import cv2
import numpy as np
import pyrealsense2 as rs

# グローバル変数
clicked_hsv_values = []
collecting_hsv = False
red_hsv_range = None
blue_hsv_range = None
yellow_hsv_range = None

def onMouse(event, x, y, flags, params):
    """クリックしたピクセルのHSV値を保存"""
    global clicked_hsv_values, collecting_hsv
    color_image = params['color_image']
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_color_bgr = color_image[y, x]
        clicked_color_hsv = cv2.cvtColor(np.uint8([[clicked_color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
        if collecting_hsv:
            clicked_hsv_values.append(clicked_color_hsv)
            print(f"追加されたHSV値: {clicked_color_hsv}")

def calculate_hsv_range(color_name):
    """指定された色のHSV範囲を計算"""
    global clicked_hsv_values, red_hsv_range, blue_hsv_range, yellow_hsv_range

    if not clicked_hsv_values:
        print(f"{color_name}の記録されたHSV値がありません。")
        return

    # HSVの最小値・最大値を取得
    hsv_array = np.array(clicked_hsv_values)
    h_min, s_min, v_min = np.min(hsv_array, axis=0)
    h_max, s_max, v_max = np.max(hsv_array, axis=0)

    # 赤の場合、範囲を2分割
    if color_name == "赤":
        lower1 = np.array([h_min if h_min <= 10 else 0, s_min, v_min])
        upper1 = np.array([10, s_max, v_max]) if h_min <= 10 else np.array([0, 0, 0])
        lower2 = np.array([170, s_min, v_min]) if h_max >= 170 else np.array([0, 0, 0])
        upper2 = np.array([h_max, s_max, v_max]) if h_max >= 170 else np.array([0, 0, 0])
        red_hsv_range = (lower1, upper1, lower2, upper2)
        print(f"赤のHSV範囲: lower1={lower1.tolist()}, upper1={upper1.tolist()}, lower2={lower2.tolist()}, upper2={upper2.tolist()}")
    else:
        # 青や黄の場合、1つの連続範囲として計算
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        if color_name == "青":
            blue_hsv_range = (lower, upper)
            print(f"青のHSV範囲: lower={lower.tolist()}, upper={upper.tolist()}")
        elif color_name == "黄":
            yellow_hsv_range = (lower, upper)
            print(f"黄のHSV範囲: lower={lower.tolist()}, upper={upper.tolist()}")

    clicked_hsv_values.clear()

def display_hsv_ranges():
    """計算されたHSV範囲を表示"""
    if red_hsv_range:
        print(f"赤のHSV範囲: lower1={red_hsv_range[0].tolist()}, upper1={red_hsv_range[1].tolist()}, "
              f"lower2={red_hsv_range[2].tolist()}, upper2={red_hsv_range[3].tolist()}")
    if blue_hsv_range:
        print(f"青のHSV範囲: lower={blue_hsv_range[0].tolist()}, upper={blue_hsv_range[1].tolist()}")
    if yellow_hsv_range:
        print(f"黄のHSV範囲: lower={yellow_hsv_range[0].tolist()}, upper={yellow_hsv_range[1].tolist()}")
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
            elif key == ord('w'):  # 赤の収集開始
                collecting_hsv = True
                clicked_hsv_values.clear()
                print("赤のHSV値の収集を開始しました。")
            elif key == ord('e'):  # 赤の収集停止
                collecting_hsv = False
                calculate_hsv_range("赤")
            elif key == ord('r'):  # 青の収集開始
                collecting_hsv = True
                clicked_hsv_values.clear()
                print("青のHSV値の収集を開始しました。")
            elif key == ord('t'):  # 青の収集停止
                collecting_hsv = False
                calculate_hsv_range("青")
            elif key == ord('y'):  # 黄の収集開始
                collecting_hsv = True
                clicked_hsv_values.clear()
                print("黄のHSV値の収集を開始しました。")
            elif key == ord('u'):  # 黄の収集停止
                collecting_hsv = False
                calculate_hsv_range("黄")
            elif key == ord('i'):  # 範囲表示
                display_hsv_ranges()

    finally:
        pipeline.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

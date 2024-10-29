import cv2
import numpy as np
import pyrealsense2 as rs

# グローバル変数でクリックしたHSV値を格納
clicked_hsv_values = []
collecting_hsv = False  # 平均値収集モードのフラグ
red_hsv_range = None
blue_hsv_range = None

def onMouse(event, x, y, flags, params):
    global clicked_hsv_values, collecting_hsv
    color_image = params['color_image']
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_color_bgr = color_image[y, x]
        clicked_color_hsv = cv2.cvtColor(np.uint8([[clicked_color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
        
        # 収集モード中のみHSV値を追加
        if collecting_hsv:
            clicked_hsv_values.append(clicked_color_hsv)
            print(f"Added HSV value: {clicked_color_hsv}")
        
        # ウィンドウに表示
        text_clicked_hsv = f"Clicked HSV: {clicked_color_hsv}"
        cv2.imshow('RealSense Camera', color_image)

def calculate_hsv_range(color='red'):
    global clicked_hsv_values, red_hsv_range, blue_hsv_range
    if clicked_hsv_values:
        # 各チャンネルの平均値を計算
        hsv_mean = np.mean(clicked_hsv_values, axis=0).astype(int)
        
        # H値が0未満または180以上にならないように、SとVが0～255の範囲内になるように制限
        lower = np.clip(hsv_mean - [10, 70, 70], [0, 0, 0], [179, 255, 255])
        upper = np.clip(hsv_mean + [10, 70, 70], [0, 0, 0], [179, 255, 255])
        
        # Hチャンネルが180度をまたぐ場合の補正
        lower2 = lower.copy()
        upper2 = upper.copy()
        lower2[0] = (lower2[0] + 120) % 180
        upper2[0] = (upper2[0] + 120) % 180
        
        if color == 'red':
            red_hsv_range = (lower, upper, lower2, upper2)
            print(f"Red HSV Range: lower1={lower.tolist()}, upper1={upper.tolist()}, lower2={lower2.tolist()}, upper2={upper2.tolist()}")
        elif color == 'blue':
            blue_hsv_range = (lower, upper, lower2, upper2)
            print(f"Blue HSV Range: lower1={lower.tolist()}, upper1={upper.tolist()}, lower2={lower2.tolist()}, upper2={upper2.tolist()}")
    else:
        print("No HSV values recorded.")

def display_hsv_ranges():
    global red_hsv_range, blue_hsv_range
    if red_hsv_range and blue_hsv_range:
        print(f"            lower_red1 = np.array([{', '.join(map(str, red_hsv_range[0]))}])")
        print(f"            upper_red1 = np.array([{', '.join(map(str, red_hsv_range[1]))}])")
        print(f"            lower_red2 = np.array([{', '.join(map(str, red_hsv_range[2]))}])")
        print(f"            upper_red2 = np.array([{', '.join(map(str, red_hsv_range[3]))}])")
        print(f" ")
        print(f"            lower_blue1 = np.array([{', '.join(map(str, blue_hsv_range[0]))}])")
        print(f"            upper_blue1 = np.array([{', '.join(map(str, blue_hsv_range[1]))}])")
        print(f"            lower_blue2 = np.array([{', '.join(map(str, blue_hsv_range[2]))}])")
        print(f"            upper_blue2 = np.array([{', '.join(map(str, blue_hsv_range[3]))}])")
    else:
        print("No HSV ranges calculated yet.")

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
            height, width, _ = color_image.shape
            center_x, center_y = int(width / 2), int(height / 2)
            center_color_bgr = color_image[center_y, center_x]
            center_color_hsv = cv2.cvtColor(np.uint8([[center_color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]

            text_bgr = f"Center Color (BGR): {center_color_bgr}"
            text_hsv = f"Center Color (HSV): {center_color_hsv}"
            cv2.putText(color_image, text_bgr, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(color_image, text_hsv, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            cv2.imshow('RealSense Camera', color_image)
            cv2.setMouseCallback('RealSense Camera', onMouse, {'color_image': color_image})

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('u'):
                # 平均値の収集を開始
                collecting_hsv = True
                print("Started collecting red HSV values.")
            elif key == ord('i'):
                # 収集停止し、範囲計算と表示
                collecting_hsv = False
                print("Stopped collecting red HSV values.")
                calculate_hsv_range(color='red')
            elif key == ord('j'):
                # 平均値の収集を開始
                collecting_hsv = True
                print("Started collecting blue HSV values.")
            elif key == ord('k'):
                # 収集停止し、範囲計算と表示
                collecting_hsv = False
                print("Stopped collecting blue HSV values.")
                calculate_hsv_range(color='blue')
                clicked_hsv_values.clear()  # リストをクリア
            elif key == ord('l'):
                # 両方の色の範囲を表示
                display_hsv_ranges()

    finally:
        pipeline.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

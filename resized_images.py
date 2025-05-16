import os
from PIL import Image
import argparse


def resize_and_save_images(folder_path, save_dir):
    """ 引数で指定されたフォルダ内のすべての画像を、
        CSSのimg要素のobject-fit: coverのようにトリミングしてリサイズし、
        コピーを保存します。

    Args:
        folder_path (str): 画像が入っているフォルダのパス
        save_dir (str): リサイズ画像を保存するフォルダのパス
    """

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for filename in os.listdir(folder_path):
        if not filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff')):
            continue

        image_path = os.path.join(folder_path, filename)
        image = Image.open(image_path)

        # リサイズ後の画像サイズ
        new_width = 512
        new_height = 512

        # 画像のアスペクト比
        image_aspect_ratio = image.width / image.height

        # リサイズ後の画像のアスペクト比
        resize_aspect_ratio = new_width / new_height

        # トリミング領域を計算
        if image_aspect_ratio > resize_aspect_ratio:
            # 横長画像の場合：左右をトリミング
            trim_left = int((image.width - image.height * resize_aspect_ratio) / 2)
            trim_right = image.width - trim_left - int(image.height * resize_aspect_ratio)
            trim_top = 0
            trim_bottom = 0
        else:
            # 縦長画像の場合：上下をトリミング
            trim_left = 0
            trim_right = 0
            trim_top = int((image.height - image.width * resize_aspect_ratio) / 2)
            trim_bottom = image.height - trim_top - int(image.width * resize_aspect_ratio)

        # トリミング処理
        trimmed_image = image.crop((trim_left, trim_top, image.width - trim_right, image.height - trim_bottom))

        # リサイズ
        resized_image = trimmed_image.resize((new_width, new_height), Image.LANCZOS)

        # 保存
        save_path = os.path.join(save_dir, filename)
        if "exif" in image.info:
            resized_image.save(save_path, exif=image.info['exif'])


if __name__ == '__main__':
    # 引数を定義
    parser = argparse.ArgumentParser(description='画像をobject-fit: coverと同じようにトリミングしてリサイズして保存するスクリプト')
    parser.add_argument('folder_path', type=str, help='画像が入っているフォルダのパス')
    parser.add_argument('save_dir', type=str, help='リサイズ画像を保存するフォルダのパス')

    # 引数を解析
    args = parser.parse_args()

    # 引数で指定されたフォルダパスと保存先フォルダパスを取得
    folder_path = args.folder_path
    save_dir = args.save_dir

    resize_and_save_images(folder_path, save_dir)
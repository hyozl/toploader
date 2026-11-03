"""새 파츠 이미지의 ref 값(원본 몸통의 평균 밝기)을 알려 줘요.

사용법:
    pip install pillow numpy
    python3 tools/part_ref.py parts/heart.webp

알려 준 값을 index.html 의 STICKERS 목록에 ref:.85 처럼 넣으면 돼요.
"""
import sys

import numpy as np
from PIL import Image


def main():
    if len(sys.argv) < 2:
        print("사용법: python3 tools/part_ref.py parts/파일이름.webp")
        sys.exit(1)
    for path in sys.argv[1:]:
        im = Image.open(path).convert("RGBA")
        a = np.asarray(im).astype(float)
        body = a[..., 3] > 200
        if not body.any():
            print(f"{path}: 보이는 부분이 없어요. 배경이 투명한 이미지인지 확인해 주세요.")
            continue
        lum = (0.3 * a[..., 0] + 0.59 * a[..., 1] + 0.11 * a[..., 2]) / 255
        ref = float(np.median(lum[body]))
        see_through = float(((a[..., 3] > 10) & (a[..., 3] < 245)).sum() / max(1, (a[..., 3] > 10).sum()))
        tips = []
        if see_through > 0.1:
            tips.append("반투명한 부분이 많아요 → glass:true 를 함께 넣어 보세요")
        print(f"{path}: ref:{ref:.2f}  ({im.width}x{im.height})" + ("  · " + " / ".join(tips) if tips else ""))


if __name__ == "__main__":
    main()

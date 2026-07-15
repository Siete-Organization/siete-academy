"""Coloriza una foto en blanco y negro con el modelo DNN de Zhang et al. (OpenCV/Caffe).

Modelo en .tmp/models/colorize/ (prototxt + caffemodel + pts_in_hull.npy).
Corre en CPU. Pensado para dar color a los retratos B&N antes de usarlos como
foto fuente del Avatar IV de HeyGen.

Uso:
    python tools/colorize_photo.py --in ".tmp/Nicolas Cayo .jpg" --out .tmp/nico_color.jpg
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = REPO_ROOT / ".tmp" / "models" / "colorize"
PROTO = MODEL_DIR / "colorization_deploy_v2.prototxt"
WEIGHTS = MODEL_DIR / "colorization_release_v2.caffemodel"
PTS = MODEL_DIR / "pts_in_hull.npy"


def load_net() -> cv2.dnn_Net:
    net = cv2.dnn.readNetFromCaffe(str(PROTO), str(WEIGHTS))
    pts = np.load(str(PTS)).transpose().reshape(2, 313, 1, 1).astype(np.float32)
    net.getLayer(net.getLayerId("class8_ab")).blobs = [pts]
    net.getLayer(net.getLayerId("conv8_313_rh")).blobs = [np.full([1, 313], 2.606, np.float32)]
    return net


def colorize(net: cv2.dnn_Net, img_bgr: np.ndarray, sat: float = 1.0) -> np.ndarray:
    h, w = img_bgr.shape[:2]
    scaled = img_bgr.astype(np.float32) / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)
    L = lab[:, :, 0]

    L_rs = cv2.resize(L, (224, 224)) - 50  # mean-center
    net.setInput(cv2.dnn.blobFromImage(L_rs))
    ab = net.forward()[0].transpose((1, 2, 0))  # 224x224x2
    ab = cv2.resize(ab, (w, h)) * sat  # escala de saturación (mute el tinte del fondo)

    out_lab = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
    out_bgr = cv2.cvtColor(out_lab, cv2.COLOR_LAB2BGR)
    return (np.clip(out_bgr, 0, 1) * 255).astype(np.uint8)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="inp", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--sat", type=float, default=1.0, help="Escala de saturación (1.0=full, <1 mute el fondo)")
    args = p.parse_args()

    for f in (PROTO, WEIGHTS, PTS):
        if not f.exists():
            sys.exit(f"Falta el modelo: {f}")

    inp = Path(args.inp) if Path(args.inp).is_absolute() else REPO_ROOT / args.inp
    out = Path(args.out) if Path(args.out).is_absolute() else REPO_ROOT / args.out
    img = cv2.imread(str(inp))
    if img is None:
        sys.exit(f"No se pudo leer la imagen: {inp}")

    net = load_net()
    res = colorize(net, img, args.sat)
    out.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out), res)
    print(f"OK -> {out.relative_to(REPO_ROOT)} ({res.shape[1]}x{res.shape[0]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())


from datetime import datetime
from pathlib import Path, PurePosixPath
import io, os, base64
from PIL import Image

from . import views


def update_file(uustr, file):

    basewidth = 800
    f_time = datetime.now()

    save_path = f"./static/upload/chat/{uustr}/"
    os.makedirs(save_path, exist_ok=True)

    with Image.open(
        io.BytesIO(base64.decodebytes(bytes(file, "utf-8")))
    ) as fle:
        save_img = f"{save_path}" + f"{f_time.strftime('%Y-%m-%d-%H-%M-%S')}.{(fle.format).lower()}"
        fle.save(save_img)

    img = Image.open(save_img)
    # ..
    wpercent = basewidth / float(img.size[0])
    hsize = int((float(img.size[1]) * float(wpercent)))
    # ..
    img_resize = img.resize((basewidth, hsize), Image.Resampling.LANCZOS)
    img_resize.save(save_img)

    return save_img.replace(".", "", 1)

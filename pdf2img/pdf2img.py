from pdf2image import convert_from_path#, convert_from_bytes
from PIL import Image
import numpy as np
import os
import click

def image_resize(img, size=(1500, 1100)):
    """ 调整图片大小 """
    try:
        if img.mode not in ("L", "RGB"):
            img = img.convert("RGB")
        img = img.resize(size)
    except Exception as e:
        pass
    return img


def image_merge(
    images,
    output_dir="output",
    output_name="merge.png",
    imgtp="PNG",
    restriction_max_width=None,
    restriction_max_height=None,
):
    """垂直合并多张图片
    images - 要合并的图片路径或图片文件流列表
    ouput_dir - 输出路径
    output_name - 输出文件名
    restriction_max_width - 限制合并后的图片最大宽度，如果超过将等比缩小
    restriction_max_height - 限制合并后的图片最大高度，如果超过将等比缩小
    """
    max_width = 0
    total_height = 0
    # 计算合成后图片的宽度（以最宽的为准）和高度
    imgstreamarr = []
    for img_path in images:
        if (type(img_path) == type("")) and os.path.exists(img_path):
            with Image.open(img_path) as img:
                pic_array = np.array(img)
                imgstreamarr.append(Image.fromarray(pic_array))
        else:
            imgstreamarr.append(img_path)
    for img in imgstreamarr:
        print(img.size)
        width, height = img.size
        if width > max_width:
            max_width = width
        total_height += height
    print((max_width, total_height))
    # 产生一张空白图
    new_img = Image.new("RGB", (max_width, total_height), 255)
    # 合并
    x = y = 0
    for img in imgstreamarr:
        width, height = img.size
        new_img.paste(img, (x, y))
        y += height

    rst_width, rstheight = max_width, total_height
    if restriction_max_width and max_width > restriction_max_width:
        # 如果宽带超过限制 等比例缩小
        rst_width = restriction_max_width 
        ratio = restriction_max_width / float(max_width)
        rstheight = int(total_height * ratio)
    if restriction_max_height and total_height > restriction_max_height:
        # 如果高度超过限制 等比例缩小
        rstheight = restriction_max_height
        ratio = restriction_max_height / float(total_height)
        rst_width = int(max_width * ratio)
    print("rst_width, rstheight = ",rst_width, rstheight)
    new_img = image_resize(new_img, size=(rst_width, rstheight))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    save_path = "%s/%s" % (output_dir, output_name)
    new_img.save(save_path, imgtp)
    return save_path

@click.command()
@click.option('--fname', default="input.pdf", help='input pdf path.')
@click.option('--output_folder', default="./output", prompt='output folder', help='The output folder.')
@click.option('--output_name', default="output.png", prompt='output file name', help='The output filename.')
@click.option('--restriction_max_width', default=0, help='The max output width.')
def pdf2img(fname="input.pdf", output_folder="./output", output_name="output.png", restriction_max_width=None):
    images = convert_from_path(fname) #convert_from_bytes(open(fname, "rb").read())
    image_merge(images, output_dir=output_folder, output_name=output_name, restriction_max_width=restriction_max_width)
    # cnt=0
    # for img in images:
    #     print(type(img))
    #     print(img.size)
    #     img.save("dlsec{:0>3d}.png".format(cnt), 'PNG')
    #     cnt = cnt + 1
    # image_merge(images=['900-000-000-0501a_b.jpg',
    #  '900-000-000-0501b_b.JPG',
    #  '1216005237382a_b.jpg'])


if __name__ == "__main__":
    pdf2img()

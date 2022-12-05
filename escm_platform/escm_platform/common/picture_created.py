import io
import os
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from escm_platform.common.fdfs_util.fdfs_util import FastDfsUtil


class PictureCreated:
    def __init__(self):
        pass

    def black_background_created(self, width, height, text1=None, text2=None):
        """
        黑底图片创建
        param:
        width: int 待创建图片宽度
        height: int 待创建图片长度
        text1: dict 图片上的文字信息
        text2: dict 图片上的文字信息
        return:
        image
        """
        img = Image.new(mode='RGB', size=(width, height), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("simsun.ttc", 40, encoding="unic")  # 设置字体
        if text1:
            t_str = ''
            for t_key, t_value in text1.items():
                t_str = t_str + '{}:{} '.format(t_key, t_value)
            text1 = t_str
            print(text1)
            draw.text(xy=(0, 0), text=text1, fill='white', font=font)
        if text2:
            t_str = ''
            for t_key, t_value in text2.items():
                t_str = t_str + '{}:{} '.format(t_key, t_value)
            text2 = t_str
            print(text2)
            draw.text(xy=(0, 40), text=text2, fill='white', font=font)

        return img

    def picture_splicing(self, img1, img2, splicing='y'):
        """
        图片拼接
        param:
        img1: image 待拼接图片1
        img2: image 待拼接图片2
        splicing: dict 拼接的方向 'x' or 'y'
        return:
        image
        """
        size1, size2 = img1.size, img2.size
        if splicing == 'x':
            new_image = Image.new("RGB", (size1[0] + size2[0], size1[1]))
            loc1, loc2 = (0, 0), (size1[0], 0)
        else:
            new_image = Image.new("RGB", (size1[0], size2[1] + size1[1]))
            loc1, loc2 = (0, 0), (0, size1[1])
        new_image.paste(img1, loc1)
        new_image.paste(img2, loc2)

        return new_image

    def picture_resize(self, width, height, img):
        """
        图片大小修改
        param:
        width: 修改后宽
        height: 修改后长
        img: image 待修改图片
        return:
        image
        """
        reimg = img.resize((width, height), Image.ANTIALIAS)
        return reimg

    def picture_size_get(self, img):
        """
        获取image对象长宽
        """
        width = img.width
        height = img.height

        return width, height

    def picture_to_bytes(self, img):
        """
        生成image对象的二进制流
        """
        butter = BytesIO()
        img.save(butter, format='PNG')
        img_bytes = butter.getvalue()

        return img_bytes

    def picture_created_by_buffer(self, buffer):
        """
        通过二进制流创建image对象
        """

        return Image.open(io.BytesIO(buffer))

if __name__ == '__main__':

    pc = PictureCreated()
    fdfs = FastDfsUtil()
    # 'group1/M00/00/05/wKhkb2NbNqqAZHqIAAAAuivu7Hk16..png'
    # remote_id = 'group1/M00/00/05/wKhkb2NbNqqAZHqIAAAAuivu7Hk16..png'
    # img_buffer = fdfs.download_to_buffer(remote_id)['data']['Content']
    # width, height = pc.picture_size_get(img_buffer)
    # print('width:{}, height: {}'.format(width, height))
    buf = FastDfsUtil().download_to_buffer('group1/M00/00/08/wKhkb2NfepSAEldEAH6QAC0htys7818839')['data']['Content']
    print(buf)
    img_1 = pc.picture_created_by_buffer(buf)

    d_text = {
        '设备编号': '123',
        '道路代码': '123',
        '监视方向': '123',
        '违法地点': '123',
        '路段': '123',
        '拍摄地点': '123',
        '拍摄时间': '123'
    }
    # pc.black_background_created(100, 100, d_text)
    # print(fdfs.upload_by_buffer(pc.picture_to_bytes(pc.black_background_created(100, 100, '123'))))

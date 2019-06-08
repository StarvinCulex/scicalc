import base64
import os


def pic2py(picture_names, py_name):
    write_data = []
    for pn in picture_names:
        filename = pn.replace('.', '_')
        open_pic = open("%s" % pn, 'rb')
        b64 = base64.b64encode(open_pic.read())
        open_pic.close()
        write_data.append('%s = "%s"\n' % (filename, b64.decode()))
    f = open("%s.py" % py_name, 'w+')
    for data in write_data:
        f.write(data)
    f.close()


def generate_pic(pic_code, pic_name):
    image = open(pic_name, 'wb')
    image.write(base64.b64decode(pic_code))
    image.close()


def delete_pic(pic_name):
    os.remove(pic_name)


if __name__ == '__main__':
    pic2py(['kbs.gif', 'avatar.ico'],
           'pics')


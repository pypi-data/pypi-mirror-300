from setuptools import setup

# 配置
setup(
       # 名称必须匹配文件名 'vibpy'
        name="vibpy",
        version='0.0.2',
        author='ghostxy',
        author_email='<ghostxy1987@hotmail.com>',
        description='Python package for Vibration',
        py_modules=["vibpy.vib_cal", "vibpy.optic_clock"]
)

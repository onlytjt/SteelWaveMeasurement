#!/usr/bin/python
# -*- coding:utf-8 -*-

import Camera

def main():
    ci = Camera.CameraInterface()
    ci.initCamera()
    ci.initAttribute()


if __name__ == '__main__':
    main()
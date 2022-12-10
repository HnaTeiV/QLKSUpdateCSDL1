from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Text, Enum, DateTime,BigInteger
from sqlalchemy.orm import relationship, backref
from app import db, app
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin

class baseModel(db.Model):
    __abstract__ = True
    id=Column(Integer,primary_key=True,autoincrement=True)

class userRoleEnum(UserEnum):
    GUEST=1
    EMPLOYEE=2
    ADMIN=3

class loaiPhong(baseModel):
    tenLoaiPhong=Column(String(50),default=False)
    donGia=Column(BigInteger,default=True)
    lp_p=relationship('phong',backref='loaiPhong',lazy=False)


class phong(baseModel):
    tenPhong=Column(String(50),default=False)
    tinhTrang=Column(Boolean,default=True)
    ghiChu=Column(String(300))
    maLoaiPhong=Column(Integer,ForeignKey(loaiPhong.id))
    image = Column(String(100))
    lp_slptpd = relationship('soLuongPhongTrongPhieuDat', backref='phong', lazy=False)

class user(baseModel, UserMixin):
    name=Column(String(50),default=False)
    username=Column(String(50),default=False)
    password=Column(String(50),default=False)
    email=Column(String(50))
    diaChi=Column(String(100))
    cmnd=Column(String(20))
    avatar=Column(String(100))
    active=Column(Boolean,default=True)
    user_role = Column(Enum(userRoleEnum), default=userRoleEnum.GUEST)

class loaiKhach(baseModel):
    tenLoaiKhach=Column(String(50),default=False)
    lk_k=relationship('khachHang',backref='loaiKhach',lazy=False)
class khachHang(user):
    maLoaiKhach=Column(Integer,ForeignKey(loaiKhach.id))
    kh_pdp=relationship('phieuDatPhong',backref='khachHang',lazy=False)
class phieuDatPhong(baseModel):
    ngayNhanPhong=Column(DateTime,default=datetime.now())
    ngayTraPhong=Column(DateTime)
    pdp_slptpd=relationship('soLuongPhongTrongPhieuDat',backref='phieuDatPhong',lazy=False)
    pdp_hd=relationship('hoaDon',backref='phieuDatPhong',lazy=False)
    maKhachHang=Column(Integer,ForeignKey(khachHang.id))

class soLuongPhongTrongPhieuDat(baseModel):
    soLuongPhong=Column(Integer,default=False)
    malOaiPhong=Column(Integer,ForeignKey(phong.id))
    maPhieuDat=Column(Integer,ForeignKey(phieuDatPhong.id))






class hoaDon(baseModel):
    soNgayThue=Column(Integer,default=False)
    donGia=Column(BigInteger,default=False)
    tongTien=Column(BigInteger,default=False)
    maPhieuDat=Column(Integer,ForeignKey(phieuDatPhong.id),)
    ngayThanhToan=Column(DateTime)


if __name__ == '__main__':
    with app.app_context():
        # db.create_all()

        import hashlib

        password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        U = user(name='VA', email='dasdfjosa@gmail.com', username='admin', password=password,
                 diaChi='DFJSAFOIASJFOIAS',
                 cmnd='345345345',avatar='fdsfasfasfasfsafsa',
                 user_role=userRoleEnum.ADMIN, active=1)

        # db.session.add(U)
        # db.session.commit()


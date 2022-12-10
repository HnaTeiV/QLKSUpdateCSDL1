from flask import Flask,redirect
from flask_admin import Admin,expose,BaseView
from app import app,db
from flask_admin.contrib.sqla import ModelView
from app.models1 import phong, loaiPhong, khachHang, hoaDon,phieuDatPhong,userRoleEnum,soLuongPhongTrongPhieuDat
from flask_login import logout_user,current_user

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role== userRoleEnum.ADMIN
class AuthenticatedEmployeeModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class phongModelView(AuthenticatedModelView):
    column_searchable_list = ['tenPhong','ghiChu']
    column_filters = ['tenPhong']
    column_exclude_list = ['Image']
    column_labels = {
        'tenPhong':'Tên Phòng',
        'tinhTrang':'Tình Trạng',
        'Image':'Image',
        'ghiChu': 'Ghi Chú'
    }
class loaiPhongModelView(AuthenticatedModelView):
    column_searchable_list = ['tenLoaiPhong']

class EmployeeView(AuthenticatedEmployeeModelView):
        can_delete = False




class chiTietPhieuDatModelView(EmployeeView):
    column_searchable_list = ['id']

class chiTietHoaDonModelView(EmployeeView):
    column_searchable_list = ['id']
class logoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')



admin = Admin(app=app, name='Quản trị khách sạn', template_mode='bootstrap4')

admin.add_view(phongModelView(phong, db.session,name='Phòng'))
admin.add_view(loaiPhongModelView(loaiPhong,db.session,name='Loại Phòng'))
admin.add_view(EmployeeView(khachHang, db.session, name = "Khách hàng"))
admin.add_view(EmployeeView(phieuDatPhong, db.session, name = "Phiếu đặt phòng"))
admin.add_view(EmployeeView(hoaDon, db.session, name = "Hóa đơn"))
admin.add_view(EmployeeView(soLuongPhongTrongPhieuDat, db.session, name = "Số lượng phòng trong phiếu đặt"))
admin.add_view(logoutView(name='Đăng xuất'))


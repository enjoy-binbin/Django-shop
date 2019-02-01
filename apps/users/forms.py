# -*- coding: utf-8 -*-
from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile, UserAddress


class LoginForm(forms.Form):
    """ Login的Form对前台登陆页面进行验证 """
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=2)


class RegisterForm(forms.Form):
    """ 注册页面的Form """
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ForgetPwdForm(forms.Form):
    """ 忘记密码From, 通过发送邮件修改密码 """
    email = forms.EmailField(required=True, error_messages={'invalid': '邮箱错了'})
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ResetPwdForm(forms.Form):
    """ 忘记密码From, 通过发送邮件修改密码 """
    password = forms.CharField(required=True, min_length=6, error_messages={'min_length': '密码长度不能低于6位'})
    password2 = forms.CharField(required=True, min_length=6, error_messages={'min_length': '密码长度不能低于6位'})


class UserInfoForm(forms.ModelForm):
    """ 用户个人信息表单 """

    class Meta:
        model = UserProfile
        fields = ['nickname', 'gender', 'birthday', 'address', 'mobile']


class UploadImageForm(forms.ModelForm):
    """ 用户个人中心 上传图片表单 """

    class Meta:
        model = UserProfile
        fields = ['image']


class AddressForm(forms.Form):
    signer = forms.CharField(required=True, error_messages={'required': '收件人必须填写'})
    signer_mobile = forms.CharField(required=True, min_length=11, error_messages={'min_length': '手机号不能低于11位'})
    address = forms.CharField(required=True, error_messages={'required': '收货地址必须填写'})

function verifyDialogSubmit(array) {
    var i = 0,
        length = array.length,
        validata = true;
    for (i; i < length; i++) {
        var obj = array[i],
            _this = $(obj.id);
        validata = validate(obj, _this);
        if (!validata) {
            return validata;
        }
    }
    return validata;
}

function validate(obj, _this) {
    var tips = obj.tips,
        errorTips = obj.errorTips,
        regName = obj.regName,
        require = obj.require,
        repwd = obj.repwd,
        minlength = obj.minlength,
        strlength = obj.strlength,
        value = $.trim(_this.val());
    //为空验证
    if (require && (!value)) {
        return Dml.fun.showValidateError(_this, tips);
    }
    _this.parent().removeClass('errorput');
    _this.parent().siblings('.error').hide();
    return true;
}

$(function () {
    $('input[type=text]').focus(function () {
        $(this).parent().removeClass('errorput');
        $(this).parent().siblings('.error').hide();
    })
})

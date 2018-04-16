$.validate({
    form: '#reg_form, #form_torn_reg, #form_plr_add',
    modules: 'location, date, security, file',
    lang: 'ru'
});
$.formUtils.addValidator({
    name: 'compare',
    validatorFunction: function compareTime() {
        var time1 = $('#id_start').val();
        var time2 = $('#id_end').val();
        return time2 > time1;
    },
    errorMessage: 'Дата окончания должна быть больше даты начала турнира',
    errorMessageKey: 'неправильнаяДата'
});

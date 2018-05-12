$.validate({
    form: '#reg_form, #form_torn_reg, #form_plr_add',
    modules: 'location, date, security, file',
    lang: 'ru'
});
$.formUtils.addValidator({
    name: 'compare',
    validatorFunction: function compareTime() {
        var time1 = $('#id_start').val().split(".");
        var time2 = $('#id_end').val().split(".");

        if (time1.length > 1 && time2.length > 1) {
            time1 = new Date(time1[2], time1[1] - 1, time1[0]);
            time2 = new Date(time2[2], time2[1] - 1, time2[0]);
            return time2 >= time1;
        }
        return true;

    },
    errorMessage: 'Дата окончания не может быть раньше даты начала турнира',
    errorMessageKey: 'неправильнаяДата'
});

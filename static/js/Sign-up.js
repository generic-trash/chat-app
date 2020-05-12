$(function() {
    inputs = $('input').attr('class','')
    password = $('#password')
    username = $('#username')
    cpass = $('#cpassword')
    email = $('#email')
    errors = $('h6').text(null)
    pwerr = $('#pwh6')
    cperr = $('#cph6')
    emerr = $('#emh6')
    userr = $('#ush6')
    $('form').submit(function(e) {
            e.preventDefault();
            errors.text(null)
            inputs.attr('class','')
            var authxhr = new XMLHttpRequest()
            body = JSON.stringify({
            'email':email.val(),
            'username':username.val(),
            'password':password.val(),
            'confirm':cpass.val()
            })
            authxhr.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    resp = JSON.parse(this.responseText)
                    if (resp.status == 'success') {
                        window.location.href = '/'
                    } else {
                        userr.text(resp.errors.username)
                        pwerr.text(resp.errors.password)
                        cperr.text(resp.errors.confirm)
                        emerr.text(resp.errors.email)
                        if(userr.text()) username.addClass('invalid');
                        if(pwerr.text()) password.addClass('invalid');
                        if(emerr.text()) email.addClass('invalid');
                        if(cperr.text()) cpass.addClass('invalid');
                    }
                }
            }
            authxhr.open('POST','/register')
            authxhr.send(body);
        })
})
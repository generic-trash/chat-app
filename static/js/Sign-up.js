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
    body = JSON.stringify({
        'email':email.val(),
        'username':username.val(),
        'password':password.val(),
        'confirm':cpass.val()
    })
    fetch("/register", {
        "credentials": "include",
        "body": body,
        "method": "POST",
        "mode": "cors"
    }).then(function (response) {
        if (response.status == 200) {
            window.location = '/'
        } else if (response.status == 403) {
            response.json().then( function(data) {
                userr.text(data.username)
                pwerr.text(data.password)
                cperr.text(data.confirm)
                emerr.text(data.email)
                if(userr.text()) username.addClass('invalid');
                if(pwerr.text()) password.addClass('invalid');
                if(emerr.text()) email.addClass('invalid');
                if(cperr.text()) cpass.addClass('invalid');
            })
        }
    });
})
$("<meta name='jsid' value='signupjs'>").appendTo('head')
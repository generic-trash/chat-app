inputs =  $('input')
inputs.attr('class', '');
err = $('h6')
err.hide();
$('form').submit(async function(e) {
    e.preventDefault()
    inputs.attr('class','')
    err.hide()
    body = JSON.stringify({'username': $('#username').val(), 'password':$('#password').val()})
    await fetch("/login", {
        "credentials": "include",
        "body": body,
        "method": "POST",
        "mode": "cors"
    }).then(function(response) {
        if (response.status == 200) {
            window.location = '/'
        } else if (response.status == 403) {
            inputs.addClass('invalid')
            err.show()
        }
    });
})
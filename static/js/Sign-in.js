inputs =  $('input')
inputs.attr('class', '');
err = $('h6')
err.hide();
$('form').submit(function(e) {
    e.preventDefault()
    inputs.attr('class','')
    err.hide()
    var authreq = new XMLHttpRequest()
    body = JSON.stringify({'username': $('#username').val(), 'password':$('#password').val()})
    authreq.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            window.location = '/'
        } else if (this.readyState == 4 && this.status == 403) {
            inputs.addClass('invalid')
            err.show()
        }
    }
    authreq.open('POST', '/login')
    authreq.send(body)
})
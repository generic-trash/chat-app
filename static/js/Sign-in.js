$(function() {
inputs =  $('input')
err = $('h6')
inputs.attr('class','')
    err.hide()
$('form').submit(function(e) {
    e.preventDefault()
    inputs.attr('class','')
    err.hide()
    var authreq = new XMLHttpRequest()
    body = JSON.stringify({'username': $('#username').val(), 'password':$('#password').val()})
    authreq.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            data = JSON.parse(this.responseText)
            if (data.csrf) {
                reloadtoken()
            } else if (data.status == 'error') {
                inputs.addClass('invalid')
                err.show()
            } else {
                window.location = '/getuser'
            }
        }
    }
    authreq.open('POST', '/login')
    authreq.setRequestHeader('X-CSRF-Token', getcsrftok())
    authreq.send(body)
})
})
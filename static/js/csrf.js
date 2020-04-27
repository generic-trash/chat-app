function getcsrftok() {
    return Cookies.get('csrf_token')
}
function reloadtoken() {
var xhr = new XMLHttpRequest()
    xhr.open('GET','/csrf_token')
    xhr.send();
}
reloadtoken()

function getcsrftok() {
    return Cookies.get('csrf_token')
}
if (getcsrftok() == undefined) {
    var xhr = new XMLHttpRequest()
    xhr.open('GET','/csrf_token')
    xhr.send();
}
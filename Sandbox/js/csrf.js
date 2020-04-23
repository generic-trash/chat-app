function getcsrftok() {
    return Cookies.get('csrf_token')
}
var vertok = new XMLHttpRequest()
vertok.onreadystatechange = function() {
    if(this.readyState == 4 && this.status == 200) {
        if(!JSON.parse(this.responseText).valid) {
            var xhr = new XMLHttpRequest()
            xhr.open('GET','/csrf_token')
            xhr.send(getcsrftok());
        }
    }
}
vertok.open('GET','/verify_csrftok')
vertok.send(getcsrftok())
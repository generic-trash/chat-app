$('#sentinel-css').remove()
function darkmode_handle(isdark) {
    if(isdark) {
        $('#Convo-css').attr('href','/assets/css/Conversation-dark.css')
    } else {
        $('#Convo-css').attr('href','/assets/css/Conversation.css')
    }
}
var xhr = new XMLHttpRequest()
xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
            data = JSON.parse(this.responseText)
            darkmode_handle(data.darkmode)
    }
}
xhr.open('GET', '/darkmode')
xhr.send()
convolength = 0
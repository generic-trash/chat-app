if (!localStorage.getItem('Conversation')) window.location = '/';
user = ""
var xhr = new XMLHttpRequest()
xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        data = JSON.parse(this.responseText)
        user = data.username
    }
}
xhr.open('GET', '/getuserdata')
xhr.send()
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
function add_conversation_comments(comments) {
    for(var i = 0; i < comments.length; i++) {
        span = $("<span>")
        span.addClass('chat')
        if(comments[i].user == user) {
            span.addClass('u2')
        } else {
            span.addClass('u1')
        }
        span.text(comments[i].comment)
        $('.chats').append(span)
    }
}
function getnewcomments() {
    var xhrx = new XMLHttpRequest()
    xhrx.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
                data = JSON.parse(this.responseText)
                convolength += data.length
                add_conversation_comments(data)
        } else if (this.readyState == 4 && this.status == 500) {
                window.location.href = '/'
        }
    }
    xhrx.open('POLL','/conversations/'+window.location.search.trimLeft('?'))
    xhrx.send(JSON.stringify({"no_of_convos": convolength}))
}

$('form').submit(function(e) {
    e.preventDefault()
    if($('input').val().trim() != "") {
    var xhr3 = new XMLHttpRequest()
    xhr3.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
                data = JSON.parse(this.responseText)
                convolength += data.length
                add_conversation_comments(data)
        }
    }
    xhr3.open('POST','/conversations/'+window.location.search.trimLeft('?'))
    xhr3.send(JSON.stringify({"no_of_convos": convolength,'comment':$('input').val()}))
    $('input').val("")
    }
})
getnewcomments()
setInterval(getnewcomments, 5000)
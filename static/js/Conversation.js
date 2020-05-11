window.user = ""
var deferpoll = false;
function darkmode_handle(isdark) {
    if(isdark) {
        $('#Convo-css').attr('href','/assets/css/Conversation-dark.css')
    } else {
        $('#Convo-css').attr('href','/assets/css/Conversation.css')
    }
}
function add_conversation_comments(comments) {
    for(var i = 0; i < comments.length; i++) {
        span = $("<span>")
        span.addClass('chat')
        if(comments[i].user == window.user) {
            span.addClass('u2')
        } else {
            span.addClass('u1')
        }
        span.text(comments[i].comment)
        $('.chats').append(span)
    }
}

function getnewcomments() {
    if (!deferpoll) {
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
        xhrx.open('POLL','/conversations/'+window.location.search.slice(1))
        xhrx.send(JSON.stringify({"no_of_convos": convolength}))
    } else {
        deferpoll = false;
    }
}
async function initialize() {
        await fetch("/getuserdata", {
            "credentials": "include",
            "headers": {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.5"
            },
            "method": "GET",
            "mode": "cors"
        }).then(function (response) {
            if (response.status !== 200) {
                return;
            }

            response.json().then(function (data) {
                window.user = data.username
            })
        });
        await fetch("/darkmode", {
            "credentials": "include",
            "headers": {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.5"
            },
            "method": "GET",
            "mode": "cors"
        }).then(function (response) {
            if (response.status !== 200) {
                return;
            }

            response.json().then(function (data) {
                darkmode_handle(data.darkmode)
            })
        });
        getnewcomments()
}
$('#sentinel-css').remove()
initialize()
convolength = 0

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
        xhr3.open('POST','/conversations/'+window.location.search.slice(1))
        xhr3.send(JSON.stringify({"no_of_convos": convolength,'comment':$('input').val()}))
        $('input').val("")
        deferpoll = true;
    }
})
setInterval(getnewcomments, 5000)
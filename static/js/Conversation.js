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

async function getnewcomments() {
    if (!deferpoll) {
            await fetch('/conversations/'+window.location.search.slice(1), {
                "credentials": "include",
                "headers": {
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0",
                    "Accept": "*/*",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Content-Type": "text/plain;charset=UTF-8",
                    "Pragma": "no-cache",
                    "Cache-Control": "no-cache"
                },
                "body": JSON.stringify({"no_of_convos": convolength}),
                "method": "POLL",
                "mode": "cors"
            }).then(function (response) {
                if (response.status == 500) {
                    window.location.href = '/'
                } else if (response.status != 200) {
                    return
                }

                response.json().then(
                    function (data) {
                        convolength += data.length
                        add_conversation_comments(data)
                    }
                )
            });
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

$('form').submit(async function(e) {
    e.preventDefault()
    if($('input').val().trim() != "") {
          await fetch("http://localhost:5000/conversations/3VQPQM2ZPNAFGQEYPBEZDR3RWZCISX4NT52ECDNETMJS7XLHY2BK3DO7SULW42Q7CX7IFDIJJYEYQKAWHTHSM2LDP3K2YI4R5GEKYK5D", {
            "credentials": "include",
            "headers": {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.5",
                "Content-Type": "text/plain;charset=UTF-8"
            },
            "body": JSON.stringify({"no_of_convos": convolength,'comment':$('input').val()}),
            "method": "POST",
            "mode": "cors"
            }).then( function(response)  {
                if (response.status == 200) {
                    response.json().then(function (data) {
                        convolength += data.length
                        add_conversation_comments(data)
                    })
                }
            });
            deferpoll = true;
    }
    $('input').val("")
})
window.scrollTo(0, document.body.scrollHeight)
setInterval(getnewcomments, 5000)
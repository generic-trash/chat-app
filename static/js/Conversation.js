window.user = ""
window.blurred = false
window.lastuser = ""
window.poll = false
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

async function getnewcomments(init=false) {
        while (window.poll);
        window.poll = true
        await fetch('/conversations/'+window.location.search.slice(1), {
            "credentials": "include",
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
                    if( data.length > 0) {
                        convolength = data[data.length - 1].id
                        if (!init) window.lastuser = data[data.length - 1].user
                        add_conversation_comments(data)
                    }
                }
            )
        });
        window.poll = false
}
async function initialize() {
        await fetch("/getuserdata", {
            "credentials": "include",
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
        getnewcomments(true);
}
$('#sentinel-css').remove()
initialize()
convolength = 0

$('form').submit(async function(e) {
    e.preventDefault()
    while (window.poll);
    window.poll = true
    if($('input').val().trim() != "") {
          await fetch('/conversations/'+window.location.search.slice(1) , {
            "credentials": "include",
            "body": JSON.stringify({"no_of_convos": convolength,'comment':$('input').val()}),
            "method": "POST",
            "mode": "cors"
          }).then(function (response) {
            if (response.status != 200) {
                return
            }

            response.json().then(
                function (data) {
                    if( data.length > 0) {
                        convolength = data[data.length - 1].id
                        add_conversation_comments(data)
                    }
                    $('input').val("")
                    $("html, body").animate({
                    scrollTop: $(
                      'html, body').get(0).scrollHeight
                    }, 10);
                }
            )
        })
    }
    window.poll = false
})
setInterval(function() {
    if (window.blurred && window.lastuser) {
        document.title = document.title == "Conversation page" ? window.lastuser + " says" : "Conversation page";
    } else {
        document.title = "Conversation page"
    }
 }, 1000);
setInterval(getnewcomments, 5000)
$(window).on("blur",function() {
  window.blurred = true;
}).on("focus",function() {
  window.blurred = false
  window.lastuser = ""
});
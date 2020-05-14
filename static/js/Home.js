$('#sentinel-css').remove()
modal = $("#newconvopopup");
modal2 = $("#themepopup");
function hideModal() {
    modal.hide();
}
function hideModal2() {
    modal2.hide();
}
function showModal() {
    modal.show();
}
function showModal2() {
    modal2.show();
}
hideModal()
hideModal2()
$("#newconvo").click(showModal)
$("#themetrig").click(showModal2);
$("#close-theme").click(hideModal2);
$("#close-newconvo").click(hideModal);
window.onclick = function (event) {
    if (event.target == modal) {
      hideModal()
    }
    if (event.target == modal2) {
      hideModal2()
    }
};
function darkmode_handle(isdark) {
    if(isdark) {
        $("#path").attr("fill",'#ff6b00')
        $('#Home-css').attr('href','/assets/css/Home-dark.css')
    } else {
        $("#path").attr("fill",'#0094ff')
        $('#Home-css').attr('href','/assets/css/Home.css')
    }
}
async function deleteParent() {
    await fetch('/conversations/'+$(event.target).parent().attr('id'), {
        "credentials": "include",
        "method": "DELETE",
        "mode": "cors"
    }).then(function (response) {
        if(response.status == 200) {
            response.json().then(function(data) {
                update(data)
            })
        }
    });
}
function navigateTo() {
    if ($(event.target).attr('class') == 'conversation' || $(event.target).attr('class') == 'title') {
       window.location.href = '/Conversation.html?'+$(event.target).attr('id')
    }
}
function createConversationElement(id, name) {
    return "<div class='conversation' id='"+id+"' onclick='navigateTo()''> <h1 class='title'>" + name + "</h1> <button class=\"btn btn-secondary deleteconvo\" onclick='deleteParent()' deleteconvo>Delete conversation</button></div><div class='divider'></div> "
}
function update(data) {
    $('.conversation, .divider').remove()
    for(var key in data) {
        $('#Home-js').before(createConversationElement(key, data[key]))
    }
}
async function initialize() {
    await fetch("/Conversations/getall", {
        "credentials": "include",
        "method": "GET",
        "mode": "cors"
    }).then(function(response) {
        if (response.status == 200) {
            response.json().then(update)
        }
    });
    await fetch("/darkmode", {
        "credentials": "include",
        "method": "GET",
        "mode": "cors"
    }).then(function (response) {
        if (response.status == 200) {
            response.json().then(function (data) {
                 darkmode_handle(data.darkmode)
            })
        }
    });
    await fetch("/getuserdata", {
        "credentials": "include",
        "method": "GET",
        "mode": "cors"
    }).then(function (response) {
        if (response.status == 200) {
            response.json().then(function (data) {
                 $('.content p').text(data.email)
                 $('.content h2').text(data.username)
                 $('.user h1').text(data.username.toUpperCase()[0])
            })
        }
    });
}
initialize()
$('#newconvoform').submit(async function(e) {
    e.preventDefault()
    await fetch("/Conversations/new", {
        "credentials": "include",
        "referrer": "/Home.html",
        "body": JSON.stringify({"email":$('#convouser').val()}),
        "method": "POST",
        "mode": "cors"
    }).then(function (response) {
        if (response.status == 200) {
            response.json().then(function (data) {
                update(data)
                $('input').val("")
                hideModal()
            })
        } else if (response.status == 500) {
            $('input').val("")
        }
    });
})
async function toggledarkmode() {
    await fetch("/darkmode", {
        "credentials": "include",
        "method": "POST",
        "mode": "cors"
    }).then(function (response) {
        if (response.status == 200) {
            response.json().then(function (data) {
                 darkmode_handle(data.darkmode)
            })
        }
    });
}
$('#darkmodesvg').click(toggledarkmode)
$('#toggle').click(toggledarkmode)

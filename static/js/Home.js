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
    }).then(response => {
        if(response.status != 200) {
            return Promise.reject(response)
        }
        return response.json()
    }).then(update);
}
function navigateTo() {
    if ($(event.target).attr('class') == 'conversation' ) {
       window.location.href = '/Conversation.html?'+$(event.target).attr('id')
    } else if ($(event.target).attr('class') == 'title') {
        window.location.href = '/Conversation.html?'+$(event.target).parent().attr('id')
    }
}
function createConversationElement(id, name) {
    return "<div class='conversation' id='"+id+"' onclick='navigateTo()''> <h1 class='title'>" + name + "</h1> <button class=\"btn btn-secondary deleteconvo\" onclick='deleteParent()'>Delete conversation</button></div><div class='divider'></div> "
}
function update(data) {
    $('.conversation, .divider').remove()
    for(var key in data) {
        $('#Home-js').before(createConversationElement(key, data[key]))
    }
}
async function initialize() {
    fetch("/Conversations/getall", {
        "credentials": "include",
        "method": "GET",
        "mode": "cors"
    }).then(response => {
        if(response.status != 200) {
            return Promise.reject(response.status)
        }
        return response.json()
    }).then(update);
}
initialize()
$('#newconvoform').submit(async function(e) {
    e.preventDefault()
    await fetch("/Conversations/new", {
        "credentials": "include",
        "body": JSON.stringify({"email":$('#convouser').val()}),
        "method": "POST",
        "mode": "cors"
    }).then(response =>  {
        if (response.status != 200) {
            return Promise.reject(response)
        }
        return response.json()
    }).then(data => {
        update(data)
        $('input').val("")
        hideModal()
    }).catch(resp => {
        //Empty for now
    });
})
async function toggledarkmode() {
    await fetch("/darkmode", {
        "credentials": "include",
        "method": "POST",
        "mode": "cors"
    }).then(response => {
        if (response.status == 200) {
            return response.json()
        } else {
            return Promise.reject(response)
        }
    }).then(data => {
        darkmode_handle(data.darkmode)
    });
}
$('#darkmodesvg').click(toggledarkmode)
$('#toggle').click(toggledarkmode)
$("<meta name='jsid' value='homejs'>").appendTo('head')
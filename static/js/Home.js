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
function deleteParent() {
    var xhr2 = new XMLHttpRequest()
    xhr2.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            data = JSON.parse(this.responseText)
            update(data)
        }
    }
    xhr2.open('DELETE', '/conversations/'+$(event.target).parent().attr('id'))
    xhr2.send()
}
function navigateTo() {
    if ($(event.target).attr('class') == 'conversation' || $(event.target).attr('class') == 'title') {
       window.location.href = '/Conversation.html?'+$(event.target).attr(id)
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
var xhr = new XMLHttpRequest()
xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        data = JSON.parse(this.responseText)
        update(data)
    }
}
xhr.open('GET', '/Conversations/getall')
xhr.send()

var xhr = new XMLHttpRequest()
xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
            data = JSON.parse(this.responseText)
            darkmode_handle(data.darkmode)
    }
}
xhr.open('GET', '/darkmode')
xhr.send()

var xhr = new XMLHttpRequest()
xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        data = JSON.parse(this.responseText)
        $('.content p').text(data.email)
        $('.content h2').text(data.username)
        $('.user h1').text(data.username.toUpperCase()[0])
    }
}
xhr.open('GET', '/getuserdata')
xhr.send()
$('#newconvoform').submit(function(e) {
    e.preventDefault()
    var xhr3 = new XMLHttpRequest()
    xhr3.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            data = JSON.parse(this.responseText)
            update(data)
            $('input').val("")
            hideModal()
        } else if (this.readyState == 4 && this.status == 403) {
            reloadtoken()
        } else if (this.readyState == 4 && this.status == 500) {
            $('input').val("")
        }
    }
    xhr3.open('POST', '/Conversations/new')
    xhr3.setRequestHeader('X-CSRF-Token', getcsrftok())
    xhr3.send(JSON.stringify({"email":$('#convouser').val(),'name':$("#convoname").val()}))
})
function toggledarkmode() {
    var xhr4 = new XMLHttpRequest()
    xhr4.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            data = JSON.parse(this.responseText)
            darkmode_handle(data.darkmode)
        }
    }
    xhr4.open('POST', '/darkmode')
    xhr4.send()
}
$('#darkmodesvg').click(toggledarkmode)
$('#toggle').click(toggledarkmode)

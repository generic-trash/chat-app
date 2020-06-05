$('#change-password').submit(async function(e) {
    e.preventDefault()
    body = JSON.stringify({
        'old': $('#old-password').val(),
        'new': $('#new-password').val(),
        'conf': $('#confirm-password').val()
    })
    $('#change-password input').removeClass("invalid")
    $('#change-password h6').text("")
    await fetch("/changepassword", {
        "credentials": "include",
        "body": body,
        "method": "POST",
        "mode": "cors"
    }).then(response => {
        if (response.status == 403) {
            return response.json()
        }
        return Promise.reject(response.status)

    }).then(data => {
        if (data.old != null) {
            $('#old-password').addClass('invalid')
            $('#old-invalid').text(data.old)
        }
        if (data.new != null) {
            $('#new-password').addClass('invalid')
            $('#new-invalid').text(data.new)
        }
        if (data.conf != null) {
            $('#confirm-password').addClass('invalid')
            $('#conf-invalid').text(data.conf)
        }
    }).catch(err => {
        if (err == 200) {
            // Success Handler
        }
    })
})
$('#delete-account').submit(async function(e) {
    e.preventDefault();
    pwd = prompt("To delete your account, type your password")
    // TODO: Add popup made in HTML
    if (pwd) {
        body = JSON.stringify({'password': pwd })
        await fetch("/deluser" , {
            "credentials": "include",
            "body": body,
            "method": "POST",
            "mode": "cors"
        }).then(response => {
            if (response.ok) {
                window.location.href = '/'
            }
            return Promise.reject(response.status)
        });
    }
})
gen_blacklist_tr = user => "<tr><td class=\"user\">"+ user + "</td><td><button class=\"btn btn-primary btn-remove\" onclick=\"remove_user()\">Remove</button></td></tr>"
function blacklist_update(users) {
    $('.blacklist tbody tr').remove()
    for(var i = 0; i < users.length; i++) {
        $(gen_blacklist_tr(users[i])).appendTo(".blacklist tbody")
    }
}
function initialize() {
    fetch('/getblocked', {
        "credentials": "include"
    }).then(response => {
        if (!response.ok) {
            return Promise.reject(response)
        }
        return response.json()
    }).then(blacklist_update)
}
initialize();
$('#blacklist-form').submit(function (e) {
    e.preventDefault()
    fetch('/block', {
        "credentials": "include",
        "method": "POST",
        "body": JSON.stringify({'user': $('#blacklist-form input').val()})
    }).then(response => {
        if (!response.ok) {
            return Promise.reject(response)
        }
        return response.json()
    }).then(blacklist_update)
})
function darkmode_handle(isdark) {
    if(isdark) {
        $("#path").attr("fill",'#ff6b00')
        $('#Home-css').attr('href','/assets/css/Home-dark.css')
    } else {
        $("#path").attr("fill",'#0094ff')
        $('#Home-css').attr('href','/assets/css/Home.css')
    }
}
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
modal = $("#themepopup");
function hideModal() {
    modal.hide();
}
function showModal() {
    modal.show();
}
hideModal()
$("#themetrig").click(showModal);
$("#close-theme").click(hideModal);
$("<meta name='jsid' value='setjs'>").appendTo('head')
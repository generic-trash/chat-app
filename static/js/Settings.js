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
            if (!response.ok) {
                return Promise.reject(response.status)
            }
            return response.json()
        }).then(success => {
        console.log(success)
            if (success) window.location.href = '/'
        });
    }
})
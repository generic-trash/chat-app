/*var xhr = new XMLHttpRequest()
xhr.onreadystatechange = function () {
    if (this.readyState == 4 ) {
        if (this.status == 200) {

        } else {
            data = JSON.parse(responseText);
            if (data.old != null) {
                $('#old-password').addClass('invalid')
                $('#old-invalid').text(data.old)
            } else {
                $('#old-password').removeClass('invalid')

            }
        }
    }
}*/
$('#change-password').submit(
    await fetch("/changepassword", {
        "credentials": "include",
        "body": body,
        "method": "POST",
        "mode": "cors"
    }).then(response => {
        if (response.status == 200) {
            return response.text()
        }
        return Promise.reject(response)

    }).catch(error => {

    })
)
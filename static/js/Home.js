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

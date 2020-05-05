$(function() {
    modal2 = $("#themepopup");
      btn2 = $("#themetrig");
      closetheme = $("#close-theme");
      modal = $("#newconvopopup");
      btn = $("#newconvo");
      modal.hide();
      modal2.hide();
      closeconvo = $("#close-newconvo");
      btn.click(function () {
        modal.show();
      });
      btn2.click(function () {
        modal2.show();
      });
      closetheme.click(function () {
        modal2.hide();
      });
      closeconvo.click(function () {
        modal.hide();
      });
      window.onclick = function (event) {
        if (event.target == modal) {
          modal.hide();
        }
        if (event.target == modal2) {
          modal2.hide();
        }
      };
})
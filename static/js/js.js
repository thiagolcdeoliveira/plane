  $(document)
    .ready(function() {

      // fix menu when passed
      $('.masthead')
        .visibility({
          once: false,
          onBottomPassed: function() {
            $('.fixed.menu').transition('fade in');
          },
          onBottomPassedReverse: function() {
            $('.fixed.menu').transition('fade out');
          }
        })
      ;


      // create sidebar and attach to menu open
      $('.ui.sidebar')
        .sidebar('attach events', '.toc.item')
      ;

$('.special.cards .image').dimmer({
  on: 'hover'
});

    })
  ;

function abrir_modal(cod_produto,preco,multiplo,nome_produto){
  $("#nome_produto").text(nome_produto)
  $("#id_produto").val(cod_produto)
  $("#id_multiplo").val(multiplo)
  $("#id_preco_unit").val(preco)

//  $("#nome_produto").select(cod_produto)
  $('.tiny.modal')
  .modal('show');

}
//$('.special.cards .image').dimmer({
//  on: 'hover'
//});

$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-object").html("");
            },
            success: function (data) {
                console.log(data);
                $("#modal-object").html(data.html_form);
                $("#modal-object").modal("show");
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
//            console.log(data)
                if (data.form_is_valid) {

                    // ATUALIZAR LISTA
//                    $(data.id_list).append(data.new_option);

                    // SE A LISTA FOR UM SELECT DO SEMANTIC
//                    if (data.new_option_anchor) {
//                        $(data.id_list).next().after(data.new_option_anchor);
//                    }

                    // MENSAGEM DE SUCESSO NO MODAL
                    $("#modal-object").html(data.html_content_message);
                    $("#modal-object").modal("hide");

                } else {
                    $("#modal-object").modal("hide");
                    $("#modal-object").html(data.html_form);
                    $("#modal-object").modal("show");
                }
            }
        });
        return false;
    };

    /* Binding */

    // Create object
    $(".js-create-object").click(loadForm);
    $("#modal-object").on("submit", ".js-object-create-form", saveForm);

    // Update object
    $("#object-table").on("click", ".js-update-object", loadForm);
    $("#modal-object").on("submit", ".js-object-update-form", saveForm);

    // Delete object
    $("#object-table").on("click", ".js-delete-object", loadForm);
    $("#modal-object").on("submit", ".js-object-delete-form", saveForm);

});

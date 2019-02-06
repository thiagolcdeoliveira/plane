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

  $('.tiny.modal')
  .modal('show');

}


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

                if (data.form_is_valid) {

                    $("#modal-object").modal("hide");


                    $("#mensagem").html(data.html_mensagem);
                    if (data.editado){
                        $("#pedido_"+data.pedido+"_quantidade").text(data.quantidade);
                        $("#pedido_"+data.pedido+"_preco_produto").text(data.preco);
                        $("#pedido_"+data.pedido+"_valor_por_produto").text(data.preco*data.quantidade);
                        $("#valor_total").html(data.total);

                    }
                   if(data.carrinho){

                    $("#carrinho").text(data.carrinho)
                    }
                } else {
                    $("#modal-object").modal("hide");
                    $("#modal-object").html(data.html_form);
                    $("#modal-object").modal("show");
                }
            }
        });
        return false;
    };


    $(".js-create-object").click(loadForm);
    $("#modal-object").on("submit", ".js-object-create-form", saveForm);



});

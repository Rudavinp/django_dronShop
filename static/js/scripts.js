$(document).ready(function() {

    var form = $('#form_buying_product');
    var form1 = $('#form_buying_product1');
    form.on('submit', function(e) {
        e.preventDefault();
        var nmb = $('#number').val();
        var submit_btn = $('#submit_btn');
        var product_id = submit_btn.data("product_id")
        var product_name = submit_btn.data('name')
        var product_price = submit_btn.data('price')

        var data = {};
        data.product_id = product_id;
        data.nmb = nmb;
        data.lol = 'lil'
        var csrf_token = $('#form_buying_product [name = "csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token
        var url = form.attr('action');
        console.log('url', url)
        console.log(data)

        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cash: true,
            success: function(data) {
                if (data.product_total_nmb){
                /* Я остановился здесь. Ищу как выводится product_total_nmb*/
                    $('#cart_total_nmb').text('('+data.product_total_nmb+')')
                    console.log('data.products_total_nmb', data.product_total_nmb)
                    $('.cart-item ul').html("");
                    $.each(data.products, function(k, v) {
                        $('.cart-item ul').append('<li>'+ v.name+', ' + v.nmb + 'шт. ' + 'по ' + v.total_price + 'грн  ' +
                            '<a class="delete-item" href="" data-product_id="'+v.id+'">x</a>'+
                            '</li>');
                    })
                }
            },
            error: function() {
                console.log('error')
            }
        })
        })

    function showCart() {
        $('.cart-item').removeClass('d-none');
    }

    $('.cart-container').on('click', function(e) {
        e.preventDefault();
        showCart();
        })
    $('.cart-container').mouseover(function() {
        showCart();
        })
//    $('.cart-container').mouseout(function() {
//        showCart();
//        })

    $(document).on('click', '.delete-item', function(e) {
        e.preventDefault();
        $(this).closest('li').remove()})


    function calculateCartAmount() {
        var total_order_amount = 0;
        $('.total-product-in-cart-amount').each(function() {
            total_order_amount += parseInt($(this).text());
            })
        $('#total_order_amount').text(total_order_amount);
    };

    $(document).on('change', '.product-in-cart-nmb', function() {
        var current_nmb = $(this).val();
        var current_tr = $(this).closest('tr');
        var current_price = parseInt(current_tr.find('.product-price').text());
        var total_amount = current_nmb*current_price
        current_tr.find('.total-product-in-cart-amount').text(total_amount);

        calculateCartAmount()
    })

    $('.button-cat').onmouseover(function() { $(this).css("background-color", "lightblue");}

    calculateCartAmount()

$('#exampleModal').on('shown.bs.modal', function () {
  $('#myInput').trigger('focus')
})

})

$('#exampleModal').on('shown.bs.modal', function () {
  $('#myInput').trigger('focus')
})
//console.log('kek')
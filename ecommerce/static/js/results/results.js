    var categories ;

    function get_categories(){
    $.ajax({
        type: "POST",
        url: '/get_categories',
        success: function (response) {
            categories = response
            put_categories();

            }})};


function show_products()
{
    $('#products').empty()
    product_list.forEach(product => {
        product_parent = $("<li></li>").addClass('row text-center item align-items-center').attr('id' ,'product num: ' + product[0]).attr('data-pid' ,product[0] ).appendTo($('#products'));
        photo_col = $("<div></div>").attr("id" ,"product_pic" + product[0]).addClass('col').appendTo(product_parent);
        photo = $('<img>').attr("src" , product[8] ).addClass('pic').appendTo(photo_col);
        name_desc_col = $("<div></div>").addClass('col-6 pnt').attr('id' ,product[0]).appendTo(product_parent);
        name_row =$("<div></div>").text(product[1]).addClass('row').appendTo(name_desc_col);
        desc_row =$("<div></div>").text(product[2]).addClass('row').appendTo(name_desc_col);
        supplier_name_row =$("<div></div>").text(product[10]["supplier_name"]).addClass('row text-black-50 text-monospace').appendTo(name_desc_col);
        price_col = $("<div></div>").addClass('col font-weight-bold').appendTo(product_parent);
        price_row = $("<div></div>").text(product[7] + "$").addClass('row').appendTo(price_col);
        stars_row = $("<div></div>").addClass('row').appendTo(price_col);
        order_count_row = $("<div></div>").text(product[10]["order_count"]+ " Sold").addClass('row').appendTo(price_col);
        if ( product [10]['review_count'] > 0 )
        {
            $(stars_row).append(product[10]["avg_stars"] + " ");
            $(stars_row).append("<div class='icon'><i class='far fa-star' aria-hidden='true'></i></div>");
            $(stars_row).append("  , " + product[10]["review_count"] + " reviews" );
        }
        $(product_parent).click(function (e) { 
            e.preventDefault();
            console.log(e.currentTarget.dataset.pid);
            pid = e.currentTarget.dataset.pid
            location.href =  '/product2/' + pid;
            
        });
    });
};

$(document).ready(function () {


    if ( product_list )
    {
        show_products();
        
    }




    setTimeout(do_stuff , 1500);

    function do_stuff()
    {
        put_categories();
    }

    function put_categories(){
        console.log('put cat runing');
        if (categories)
        {
        categories.forEach(category => {
            category_li = $("<li></li>").addClass('filter_category').css('cursor' , 'pointer').attr('data-category' , category[0]).text(category[0]).appendTo($('#sidebar_categories'));
            category_items= $("<span></span>").addClass('close text-black-50').text(category[1]).appendTo(category_li);
        })
        make_categories_clickable();
        }};


    function make_categories_clickable(){
    $('.filter_category').click(function (e) { 
        e.preventDefault();
        filter_product_type = e.currentTarget.dataset.category;
        console.log(filter_product_type);
        $('#current_cat').html(filter_product_type);
        $('#current_cat_view , #sidebar_categories').toggle();
        update_view();

        });
    };

    $('#go_back_cat').click(function (e) { 
        e.preventDefault();
        $('#current_cat').html('all');
        $('#current_cat_view , #sidebar_categories').toggle();
        update_view();
    });
/*
    $('#min , #max').click(function (e) { 
        e.preventDefault();
        filter_product_type = "";
        min_price = $('#min').val()
        max_price = $('#max').val()
        console.log('min' + min_price)
        console.log('max' + max_price)
    });*/


    $("input[type='radio'] , #min , #max").change(function (e) { 
        e.preventDefault();
        console.log('change');
        update_view();

    });

    function update_view()
    {
        min_stars = $("input[type='radio']:checked").val();
        min_price = $('#min').val();
        max_price = $('#max').val();
        product_type = $('#current_cat').html();
        data = [];
        data['product_type'] = product_type;
        data['min_price'] = min_price;
        data['max_price'] = max_price;
        data['max_price'] = min_stars;
        console.log('update_view_run');
        console.log(data);

        $.ajax({
            type: "POST",
            url: "/get_results",
            data: {'product_type' : product_type , 'min_price' :min_price , 'max_price': max_price ,'min_stars' : min_stars },
            success: function (response) {
                console.log(response);
                b = 555;
                product_list = response
                show_products();
            }
        });
    };
    
/*
    function update_view()
    {
        
    }*/
/*
    setTimeout(handle_click , 1500);

    function handle_click(){
    $(".item").click(function (e) { 
        e.preventDefault();
        console.log(e.currentTarget.dataset.pid);
        pid = e.currentTarget.dataset.pid
        location.href =  '/product2/' + pid;
    });
};
*/
});
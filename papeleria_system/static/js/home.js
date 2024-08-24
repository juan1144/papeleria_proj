$(document).ready(function() {
    // Manejo de navegación
    $('.menu a[data-menu]').on('click', function() {
        var menu = $(this).data('menu');
        $('.menu a.active').removeClass('active');
        $(this).addClass('active');
        $('.active[data-page]').removeClass('active');
        $('[data-page="' + menu + '"]').addClass('active');
    });

    // Manejo de diálogo (logout)
    $('body').on('click', '[data-dialog]', function() {
        var action = $(this).data('dialog');
        if (action === 'logout') {
            $('.dialog').toggleClass('active');
        }
    });

    $('body').on('click', '[data-dialog-action]', function() {
        var action = $(this).data('dialog-action');
        if (action === 'cancel') {
            $(this).closest('.dialog.active').toggleClass('active');
        }
    });

    // Manejo del submenú
    $('.submenu > .menu-item').on('click', function(e) {
        e.preventDefault();
        $(this).next('.submenu-items').toggle();
    });

    $(document).on('click', function(e) {
        if (!$(e.target).closest('.submenu').length) {
            $('.submenu-items').hide();
        }
    });
});

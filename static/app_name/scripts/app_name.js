(function ($) {

    var settings = {};

    $.fn.{{ app_name }} = function (options) {
        var element;
        settings = $.extend(settings, options);
        element = $(this);
        return this;
    };

})(jQuery);

$(function () {
    if (typeof(time_tooltip) == "undefined"){
        $(function () {
            $('[data-toggle="tooltip"]').tooltip();
        });
    }
    else {
        function render_time() {
            return moment($(this).data('timestamp'), locale=true).format('lll');
        }
        $('[data-toggle="tooltip"]').tooltip(
            {title: render_time}
        );
    }
});

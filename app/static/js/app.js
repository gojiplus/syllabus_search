$(document).ready(function() {
    var selected_course = 0;

    var course_table = $('#course_table').DataTable({
        bInfo: false,
        responsive: true,
        lengthMenu: [5, 10, 25, 50, 100],
        select: {
            style: 'single'
        }
    });

    function showTable(name) {
        var table = $('#' + name + '_table');
        var link = $('#' + name + '_btn');
        if (table.hasClass('d-none') && selected_course !== 0) {
            table.removeClass('d-none');
            table.DataTable({
                bInfo: false,
                searching: false,
                lengthChange: false,
                pageLength: 5,
                ajax: name.charAt(0) + '/' + selected_course,
                responsive: true
            });
            if (link.text() === 'show') {
                link.text('hide');
            }
            return true;
        }
        return false;
    }

    function hideTable(name) {
        var table = $('#' + name + '_table');
        var link = $('#' + name + '_btn');
        if (!table.hasClass('d-none')) {
            table.DataTable().destroy();
            table.addClass('d-none');
            if (link.text() === 'hide') {
                link.text('show');
            }
            return true;
        }
        return false;
    }

    $('#session_btn').on('click', function (e) {
        e.preventDefault();
        var link = $(this);
        if (link.text() === 'show') {
            showTable('session');
        } else if (link.text() === 'hide') {
            hideTable('session');
        }
    });

    $('#assess_btn').on('click', function (e) {
        e.preventDefault();
        var link = $(this);
        if (link.text() === 'show') {
            showTable('assess');
        } else if (link.text() === 'hide') {
            hideTable('assess');
        }
    });

    $('#outcome_btn').on('click', function (e) {
        e.preventDefault();
        var link = $(this);
        if (link.text() === 'show') {
            showTable('outcome');
        } else if (link.text() === 'hide') {
            hideTable('outcome');
        }
    });

    function showWrap(name) {
        var wrap = $('#' + name + '_wrap');
        if (wrap.hasClass('d-none')) {
            wrap.removeClass('d-none');
        }
        hideTable(name);
    }

    function hideWrap(name) {
        var wrap = $('#' + name + '_wrap');
        hideTable(name);
        if (!wrap.hasClass('d-none')) {
            wrap.addClass('d-none');
        }
    }

    course_table.on( 'page.dt', function () {
        selected_course = 0;
        hideWrap('session');
        hideWrap('assess');
        hideWrap('outcome');
    });

    course_table.on( 'click', 'tr', function () {
        var row = $(this);
        if (row.hasClass('selected')) {
            selected_course = 0;
            hideWrap('session');
            hideWrap('assess');
            hideWrap('outcome');
        } else {
            selected_course = row.data('id');
            showWrap('session');
            showWrap('assess');
            showWrap('outcome');
        }
    });
});

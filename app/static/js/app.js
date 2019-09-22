$(document).ready(function() {
    var selected_course = 0;

    var course_table = $('#course_table').DataTable({
        dom: 'Bftpl',
        bInfo: false,
        responsive: true,
        lengthChange: false,
        pageLength: 5,
        select: {
            style: 'single'
        },
        buttons: [
            {
                extend: 'csv',
                text: 'Download CSV',
                filename: 'courses'
            }
        ]
    });

    function showTable(name) {
        var table = $('#' + name + '_table');
        var link = $('#' + name + '_btn');
        var kw = $('#keyword').val();
        var url = name.charAt(0) + '/' + selected_course;
        if (selected_course === 0) {
            url += '?' + $('#search').serialize();
        } else if (kw) {
            url += '?keyword=' + encodeURIComponent(kw);
        }
        if (table.hasClass('d-none')) {
            table.removeClass('d-none');
            table.DataTable({
                dom: 'Bftp',
                bInfo: false,
                lengthChange: false,
                pageLength: 5,
                ajax: url,
                responsive: true,
                buttons: [
                    {
                        extend: 'csv',
                        text: 'Download CSV',
                        filename: (name == 'assess') ? 'assessments' : name + 's'
                    }
                ]
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

    course_table.on( 'page.dt', function () {
        selected_course = 0;
        hideTable('session');
        hideTable('assess');
        hideTable('outcome');
    });

    course_table.on( 'click', 'tr', function () {
        var row = $(this);
        hideTable('session');
        hideTable('assess');
        hideTable('outcome');
        if (row.hasClass('selected')) {
            selected_course = 0;
        } else {
            selected_course = row.data('id');
        }
    });
});

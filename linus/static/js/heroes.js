$(document).ready(function() {
    $.fn.dataTable.ext.search.push(
        function( settings, data, dataIndex ) {
            var filters = [
                ['weapon-type', 11],
                ['movement-type', 12],
                ['f2p', 13],
                ['book', 14],
                ['generation', 15],
            ];
            for (var i = 0; i < filters.length; ++i) {
              var alltypes = new Set();
              var classname = filters[i][0];

              $('button.active.' + classname + '-btn').each(function(index) {
                  alltypes.add($(this).attr('data-id'));
              });

              if (alltypes.size && !alltypes.has(data[filters[i][1]])) {
                  return false;
              }
            }
            return true;
        }
    );

    var table = $('#heroes-table').DataTable({
        pageLength: 50,
        columnDefs: [ 
            {
                "targets": [ 11, 12, 13, 14, 15 ],
                "visible": false,
            },
        ]
    });
    $('.btn-choose-one button').click(function() {
        if (!($(this).hasClass("active"))) {
            // Deactivate everyone
            $('.btn-choose-one button').removeClass("active");
        }
        $(this).toggleClass("active");
        table.draw();
    });

    $('.btn-choose-any button').click(function() {
        $(this).toggleClass("active");
        table.draw();
    });

} );

$(document).ready(function() {
    $.fn.dataTable.ext.search.push(
        function( settings, data, dataIndex ) {
            var filters = [
                ['weapon-type', 17],
                ['movement-type', 18],
                ['f2p', 19],
                ['book', 20],
                ['generation', 21],
                ['availability', 22],
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
                "targets": [ 9, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21, 22],
                "visible": false,
            },
        ]
    });
    $('.btn-choose-one button').click(function() {
        if (!($(this).hasClass("active"))) {
            // Deactivate everyone
            $(this).siblings().removeClass("active");
        }
        $(this).toggleClass("active");
        table.draw();
    });

    $('.btn-choose-any button').click(function() {
        $(this).toggleClass("active");
        table.draw();
    });

    $('.btn-exactly-one button').click(function() {
        // Deactivate everyone
        $(this).siblings().removeClass('active');
        $(this).toggleClass("active");
        table.draw();
    });

    $('button.statdisplay-btn').click(function() {
      var all_columns = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14];
      for (var i = 0; i < all_columns.length; ++i) {
        var column = table.column(all_columns[i]);
        column.visible(false);
      }

      var column_visibility = {};
      column_visibility.normal = [3, 4, 5, 6, 7, 8];
      column_visibility.max = [9, 10, 11, 12, 13, 14];
      var mytype = $(this).attr('data-id');
      for (var i = 0; i < column_visibility[mytype].length; ++i) {
        var column = table.column(all_columns[i]);
        column.visible(true);
      }
      table.columns.adjust().draw();
    });
} );

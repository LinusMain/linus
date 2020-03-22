$(document).ready(function() {
    $.fn.dataTable.ext.search.push(
        function( settings, data, dataIndex ) {
            var filters = [
                ['weapon-type', 11],
                ['movement-type', 12],
                ['f2p', 13],
                ['book', 14],
                ['generation', 15],
                ['availability', 16],
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

    $('.statdisplay').hide();
    $('.statdisplay-normal').show();
    var table = $('#heroes-table').DataTable({
        pageLength: 50,
        columnDefs: [ 
            {
                "targets": [ 11, 12, 13, 14, 15, 16],
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
        $(this).addClass("active");
    });

    $('button.statdisplay-btn').click(function() {
      $('.statdisplay').hide();
      $('.statdisplay.statdisplay-' + $(this).attr('data-id')).show();
      console.log($(this).attr('data-id'));
      table.draw();
    });
    $('button.statdisplay-btn[data-id="normal"]').addClass('active');
} );

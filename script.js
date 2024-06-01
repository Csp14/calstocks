$(document).ready(function() {
    $('#stockForm').submit(function(e) {
        e.preventDefault();
        var tickerSymbol = $('#tickerSymbol').val();
        
        $.ajax({
            type: 'POST',
            url: '/analyze',
            data: { tickerSymbol: tickerSymbol },
            success: function(data) {
                $('#results').show();
                $('#signal').text('Signal: ' + data.signal);
                $('#ema5').text('EMA 5-day: ' + data.ema5);
                $('#ema10').text('EMA 10-day: ' + data.ema10);
                $('#ema20').text('EMA 20-day: ' + data.ema20);
            },
            error: function(error) {
                $('#results').show();
                $('#signal').text('');
                $('#ema5').text('');
                $('#ema10').text('');
                $('#ema20').text('');
                alert('Error fetching data: ' + error.responseJSON.error);
            }
        });
    });

    // Get the percentage values from HTML data attributes
    var percentageHighTarget = parseFloat(document.getElementById('percentage_high_target').dataset.value);
    var percentageLowTarget = parseFloat(document.getElementById('percentage_low_target').dataset.value);

    // Select the elements
    var highTargetElement = document.getElementById('percentage_high_target');
    var lowTargetElement = document.getElementById('percentage_low_target');

    // Set color based on the sign of the percentage
    highTargetElement.style.color = percentageHighTarget >= 0 ? 'green' : 'red';
    lowTargetElement.style.color = percentageLowTarget >= 0 ? 'green' : 'red';
});

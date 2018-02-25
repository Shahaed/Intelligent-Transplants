var page = require('webpage').create();
var fs = require('fs');

for(i = 1; i <= 6; i++) {
    for(j = 1; j <= 24; j++) {
        for(k = 1; k <= 29; k++) {
            page.open('https://optn.transplant.hrsa.gov/data/view-data-reports/build-advanced/', function(status) {
                console.log("Status: " + status);
                if(status === "success") {
                    handler(i, j, k);
                }
                page.close();
            }); 
        }
    } 
}


page.onConsoleMessage = function(msg) {
    console.log(msg);
}



function handler(i, j, k) {
    page.evaluate(function() {
        var cat = document.getElementById('category');
        var col1 = document.getElementById('col1');
        var row1 = document.getElementById('row1');

        console.log('cat: ', cat.length);
        console.log('col1: ', col1.length);
        console.log('row1: ', row1.length);
        cat.selectedIndex = i;
        var evt = document.createEvent("HTMLEvents");
        evt.initEvent("change", true, true);
        cat.dispatchEvent(evt);

        col1.selectedIndex = j;
        evt = document.createEvent("HTMLEvents");
        evt.initEvent("change", true, true);
        col1.dispatchEvent(evt);

        row1.selectedIndex = k;
        var evt = document.createEvent("HTMLEvents");
        evt.initEvent("change", true, true);
        row1.dispatchEvent(evt);

        console.log('here');
        
        document.getElementById("DataAdvancedSubmit").click();
    });
}

function waitFor ($config) {
    $config._start = $config._start || new Date();

    if ($config.timeout && new Date - $config._start > $config.timeout) {
        if ($config.error) $config.error();
        if ($config.debug) console.log('timedout ' + (new Date - $config._start) + 'ms');
        return;
    }

    if ($config.check()) {
        if ($config.debug) console.log('success ' + (new Date - $config._start) + 'ms');
        return $config.success();
    }

    setTimeout(waitFor, $config.interval || 0, $config);
}

page.onLoadFinished = function() {
    waitFor({
        debug: true,  // optional
        interval: 0,  // optional
        timeout: 1000,  // optional
        check: function () {
            return page.evaluate(function() {
                return document.getElementById('dataGrid').is(':visible');
            });
        },
        success: function () {
            // we have what we want
            page.evaluate(function() {
                fs.writeFile('./data/' + i * j * k + '.json', JSON.stringify(document.getElementById('#dataGrid')), (err) => {
                    if (err) throw err;
                    console.log("The file was succesfully saved!");
                });

            });
        },
        error: function () {} // optional
    });
};
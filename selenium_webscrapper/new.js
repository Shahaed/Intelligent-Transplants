var page = new WebPage(), testindex = 0, loadInProgress = false;
var fs = require('fs');
var system = require('system');
var variable = [system.args[1], system.args[2], system.args[3]];
console.log(variable);
var variable_limit = [5, 20, 20];

page.onInitialized = function() {
    console.log("page.onInitialized");
    printArgs.apply(this, arguments);
};
page.onLoadStarted = function() {
    console.log("page.onLoadStarted");
    printArgs.apply(this, arguments);
};
page.onLoadFinished = function() {
    console.log("page.onLoadFinished");
    printArgs.apply(this, arguments);
};
page.onUrlChanged = function() {
    console.log("page.onUrlChanged");
    printArgs.apply(this, arguments);
};
page.onNavigationRequested = function() {
    console.log("page.onNavigationRequested");
    printArgs.apply(this, arguments);
};
page.onClosing = function() {
    console.log("page.onClosing");
    printArgs.apply(this, arguments);
};

// window.console.log(msg);
page.onConsoleMessage = function(msg) {
    console.log(msg);
    printArgs.apply(this, arguments);
};

// window.alert(msg);
page.onAlert = function(msg) {
    console.log('alert: ', msg);
    printArgs.apply(this, arguments);
};
// var confirmed = window.confirm(msg);
page.onConfirm = function() {
    console.log("page.onConfirm");
    printArgs.apply(this, arguments);
};
// var user_value = window.prompt(msg, default_value);
page.onPrompt = function() {
    console.log("page.onPrompt");
    printArgs.apply(this, arguments);
};

/*
 * This function wraps WebPage.evaluate, and offers the possibility to pass
 * parameters into the webpage function. The PhantomJS issue is here:
 * 
 *   http://code.google.com/p/phantomjs/issues/detail?id=132
 * 
 * This is from comment #43.
 */
function evaluate(page, func) {
    var args = [].slice.call(arguments, 2);
    var fn = "function() { return (" + func.toString() + ").apply(this, " + JSON.stringify(args) + ");}";
    return page.evaluate(fn);
}

var steps = [
  function() {
    //Load Login Page
    page.open("https://optn.transplant.hrsa.gov/data/view-data-reports/build-advanced/");
  },
  function() {
    //Enter Credentials
    page.evaluate(function(variable) {
        var sel = document.querySelector('select#category');
        sel.selectedIndex = variable[0];
        var evt = document.createEvent("HTMLEvents");
        evt.initEvent("change", false, true);
        sel.dispatchEvent(evt);
    }, variable);
    page.render('first.png');
  },
  function() {
    //Enter Credentials
    variable_limit = page.evaluate(function(variable) {
        var col1 = document.querySelector('select#col1');

        col1.selectedIndex = variable[1];

        var row1 = document.querySelector('select#row1');

        evt = document.createEvent("HTMLEvents");
        evt.initEvent("change", false, true);
        col1.dispatchEvent(evt);

        return [6, col1.length, row1.length];
    }, variable);

    page.render('second.png');
  },
  function() {

    //Enter Credentials
    page.evaluate(function(variable) {
        var row1 = document.querySelector('select#row1');
        console.log('row1: ', row1.length);
        row1.selectedIndex = variable[2];
        evt = document.createEvent("HTMLEvents");
        evt.initEvent("change", true, true);
        row1.dispatchEvent(evt);

        console.log('done inputing');
    }, variable);

    page.render('three.png');
  },
  function() {
    //Login
    page.evaluate(function() {
      document.getElementById("DataAdvancedSubmit").click();
    });
  },
  function() {
    page.render('final.png');

    var head = evaluate(page, function() {
        // this code has now has access to foo
        // console.log(document.getElementsByClassName('dataGrid')[0].innerHTML);
        var data = document.getElementsByClassName('dataGrid')[1].innerHTML;
        var head = '<table class="dataGrid" cellspacing="0" cellpadding="1" border="0">';
        head += data;
        head += '</table>';
        return head;
    });

    var name = './data/data' + variable[0] + '/';
    name += variable[0] + '-';
    name += variable[1] + '-';
    name += variable[2];
    name += '.html';
    fs.write(name, head, 'w'); 
   }
];

// 
interval = setInterval(function() {
    if(testindex < 5) {
        console.log("step " + (testindex + 1));
        steps[testindex]();
        testindex++;
    } else if(testindex === 5){
        console.log("step " + (testindex + 1));
        steps[testindex]();
        testindex = 0;

        if(variable[2] < variable_limit[2]) {
            variable[2]++;
        } else if(variable[2] === variable_limit[2]) {
            variable[2] = 1;

            if(variable[1] < variable_limit[1]) {
                variable[1]++;
            } else if(variable[1] === variable_limit[1]) {
                variable[1] = 1;

                if(variable[0] < variable_limit[0]) {
                    variable[0]++;
                } else if(variable[0] === variable_limit[0]) {
                    console.log("test complete!");
                    phantom.exit();
                }
            }
        }
    }

    // if(typeof steps[testindex] === "function") {
    //     console.log("step " + (testindex + 1));
    //     steps[testindex]();
    //     testindex++;
    // }

    // if (typeof steps[testindex] != "function" ) {
    //     console.log("test complete!");
    //     phantom.exit();
    // }

}, 3000);